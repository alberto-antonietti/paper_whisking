@nrp.MapSpikeSource("head_contact", nrp.brain.head_contact, nrp.poisson)
@nrp.MapSpikeSource("reward", nrp.brain.reward, nrp.poisson)
@nrp.Robot2Neuron()
def shelf_contact(t, recorder, contact_point_data, head_contact, reward):
    reward.rate = 0.0
    head_contact.rate = 0.0

    if contact_point_data.value:
        for state in contact_point_data.value.states:
            contact_names = state.collision1_name, state.collision2_name
            # clientLogger.info(contact_names)
            contact_go = 'shelf_go::shelf_go::collision' in contact_names
            contact_nogo = 'shelf_nogo::shelf_nogo::collision' in contact_names

            if contact_go:
                reward.rate = 100.0
                head_contact.rate = 100.0
                clientLogger.info('Sending reward')
                recorder.record_entry('contact', t, 'reward')
                break

            if contact_nogo:
                head_contact.rate = 100.0
                clientLogger.info('Shelf contact')
                recorder.record_entry('contact', t, 'no_reward')
                break