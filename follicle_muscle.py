@nrp.Neuron2Robot()
def follicle_muscle(t, proxy, fn_moto):
    from rospy import Duration

    n_whisks = 4

    fn_pro = fn_moto[:n_whisks*20]
    fn_ret = fn_moto[-40:]

    # L0 L1 R0 R1
    joint_names = ['whisker_' + side + str(i) + '_joint'
                   for side in 'LR' for i in range(2)]

    pro_f = 15.0
    ret_f = -10.0

    pro_d = Duration.from_sec(0.1)
    ret_d = Duration.from_sec(0.2)

    for i in range(n_whisks):
        # Protraction
        begin = i*20
        end = (i+1)*20
        spikes = sum(fn_pro[begin:end].spiked)
        pro_force = spikes*pro_f/20

        # Retraction
        side_i = 0 if i < n_whisks//2 else 1
        begin = side_i*20
        end = (side_i+1)*20
        spikes = sum(fn_ret[begin:end].spiked)
        ret_force = spikes*ret_f/20

        if pro_force:
            proxy.value.call(joint_names[i], pro_force,  None, pro_d)
        elif ret_force:
            proxy.value.call(joint_names[i], ret_force,  None, ret_d)