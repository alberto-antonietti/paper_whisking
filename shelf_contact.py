import hbp_nrp_cle.tf_framework as nrp
from hbp_nrp_excontrol.logs import clientLogger
from gazebo_msgs.msg import ContactsState
from hbp_nrp_cle.robotsim.RobotInterface import Topic


@nrp.MapCSVRecorder("recorder", filename="events.csv",
                    headers=["type", "time", "event"])
@nrp.MapRobotSubscriber("contact_point_data",
                        Topic("/gazebo/contact_point_data", ContactsState))
@nrp.MapSpikeSource("reward", nrp.brain.reward, nrp.poisson, delay=1.0)
@nrp.Robot2Neuron()
def shelf_contact(t, recorder, contact_point_data, reward):
    reward.rate = 0.0

    if contact_point_data.value:
        for state in contact_point_data.value.states:
            contact_names = state.collision1_name, state.collision2_name
            # clientLogger.info(contact_names)
            contact_go = 'shelf_go::shelf_go::collision' in contact_names
            contact_nogo = 'shelf_nogo::shelf_nogo::collision' in contact_names

            if contact_go:
                reward.rate = 100.0
                clientLogger.info('Sending reward')
                recorder.record_entry('contact', t, 'reward')
                break

            if contact_nogo:
                clientLogger.info('Shelf contact')
                recorder.record_entry('contact', t, 'no_reward')
                break