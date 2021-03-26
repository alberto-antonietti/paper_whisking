@nrp.Robot2Neuron()
def follicle_sensors(t,
                     w_data, joint_states, link_states, contact_point_data,
                     tg_ganglion):
    w_per_side = 2  # whiskers per side

    from copy import deepcopy
    w_data = w_data.value
    w_data_old = deepcopy(w_data)

    if joint_states.value:
        states = joint_states.value
        for i in range(len(states.name)):
            for side in ['L', 'R']:
                for w_i in range(w_per_side):
                    # clientLogger.info(states.name[i])
                    joint_name = 'whisker_' + side + str(w_i) + '_joint'
                    if states.name[i] == joint_name:
                        w = w_data[side][w_i]
                        w['ang'] = abs(joint_states.value.position[i])
                        w['vel'] = abs(joint_states.value.velocity[i])

    def p_to_array(p):
        return np.array([p.x, p.y, p.z])

    def get_link_positions():
        if link_states.value:
            states = link_states.value
            n_links = len(states.name)

            def get_link_name(i):
                return states.name[i].split("::")[-1]

            def is_whisker_name(link_name):
                return link_name in ["whisker_" + side + str(w_i)
                                     for side in 'LR'
                                     for w_i in range(w_per_side)]

            link_positions = {get_link_name(i):
                              p_to_array(states.pose[i].position)
                              for i in range(n_links)
                              if is_whisker_name(get_link_name(i))}
        else:
            link_positions = {}

        return link_positions

    for w_i in range(w_per_side):
        w_data['L'][w_i]['contact'] = False
        w_data['R'][w_i]['contact'] = False

    link_positions = get_link_positions()

    if contact_point_data.value and link_positions:
        def distance(p1, p2):
            return np.sqrt(sum((p1 - p2)**2))

        def avg_pos(positions):
            pts = [p_to_array(p) for p in positions]
            avg = [sum(xis)/len(pts) for xis in np.transpose(pts)]
            return np.array(avg)

        def detect_contact(state, whisker_name):
            contact_names = state.collision1_name, state.collision2_name
            w_contact_name = "mouse::{0}::{0}_collision".format(whisker_name)
            return w_contact_name in contact_names

        for c_state in contact_point_data.value.states:
            for side in ['L', 'R']:
                for w_i in range(w_per_side):
                    w_name = 'whisker_' + side + str(w_i)

                    if detect_contact(c_state, w_name):
                        d = distance(avg_pos(c_state.contact_positions),
                                     link_positions[w_name])

                        w_data[side][w_i]['contact'] = True
                        w_data[side][w_i]['dist'] = d

    # Set TG neurons rates
    tg_ganglion.rate = 0.0

    for side_i, side in enumerate(['L', 'R']):
        for w_i in range(w_per_side):
            w = w_data[side][w_i]
            w_old = w_data_old[side][w_i]

            contact_now = w['contact']
            contact_before = w_old['contact']

            n_whisks = 2*w_per_side  # sides * whiskers per side
            pop_size = 20  # neurons per population per whisker

            def get_pop(pop_index):
                # tg[ [ L[ w0, w1, ...], R[...] ], ...]

                def get_slice(size, index):
                    begin = size * index
                    end = begin + size
                    return slice(begin, end)

                tg_pop = tg_ganglion[get_slice(n_whisks*pop_size, pop_index)]
                tg_pop_side = tg_pop[get_slice(w_per_side*pop_size, side_i)]

                return tg_pop_side[get_slice(pop_size, w_i)]

            tg_pr, tg_ct, tg_dt, tg_ht, tg_ws = [get_pop(i) for i in range(5)]

            if contact_now:
                rate = 2*103.0*abs(1.0 - w['dist'])
                for pr in tg_pr:
                    pr.rate = rate
                # clientLogger.info(rate)

                if w['dist'] < 0.002:
                    tg_ht.rate = 100.0

            if contact_now and not contact_before:
                tg_ct.rate = 10.0

            if contact_before and not contact_now:
                tg_dt.rate = 10.0

            ang = w['ang']
            # clientLogger.info("%2.2f" % ang)

            def gaussian(x, mu, sig):
                pw = np.power
                return np.exp(-pw(x - mu, 2.) / (2 * pw(sig, 2.)))

            # time-locked to whisk phase
            bands = len(tg_ws)
            for ang_i in range(bands):
                step = 1.0/bands
                rbf_mu = ang_i * step + step/2
                rbf_sig = step/2
                rate = 100. * gaussian(ang, rbf_mu, rbf_sig)

                tg_ws[ang_i].rate = rate

                # clientLogger.info(side_i, ang_i, "%2.2f" % rate)