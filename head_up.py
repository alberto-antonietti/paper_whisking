import hbp_nrp_cle.tf_framework as nrp
from hbp_nrp_cle.robotsim.RobotInterface import Topic
import std_msgs.msg
# import numpy as np
from hbp_nrp_excontrol.logs import clientLogger
from sensor_msgs.msg import JointState


@nrp.MapCSVRecorder("recorder", filename="events.csv",
                    headers=["type", "time", "event"])
@nrp.MapVariable('state', initial_value='rest')
@nrp.MapRobotSubscriber("joint_states",
                        Topic("/mouse/joint_states", JointState))
@nrp.MapSpikeSink("dcn", nrp.brain.dcn, nrp.population_rate)
@nrp.MapSpikeSink("rise_head", nrp.brain.rise_head, nrp.population_rate)
@nrp.MapSpikeSink("head_contact", nrp.brain.head_contact, nrp.population_rate)
@nrp.Neuron2Robot(Topic('/mouse/neck_joint/cmd_pos', std_msgs.msg.Float64))
def head_up(t, recorder, state, joint_states, dcn, rise_head, head_contact):
    cmd_pos = 0.0

    neck_pos = 0.0
    if joint_states.value:
        states = joint_states.value
        for i in range(len(states.name)):
            if states.name[i] == 'neck_joint':
                neck_pos = states.position[i]
                # clientLogger.info('Neck position', neck_pos)

    # if dcn.rate > 0.0:
    #     clientLogger.info('dcn rate:', dcn.rate)

    if state.value == 'rest':
        if rise_head.rate > 0.1:
            clientLogger.info('rise_head rate', rise_head.rate)
        # if dcn.rate > 100.0:
        if rise_head.rate > 50.0:
            state.value = 'up'
            recorder.record_entry('head', t, 'up')

            clientLogger.info('DCN rate', dcn.rate)
            clientLogger.info('STATE:', state.value)

    if state.value == 'up':
        if head_contact.rate > 0.1:  # TODO: verificare
            state.value = 'down'

            clientLogger.info('head rate:', head_contact.rate)
            clientLogger.info('STATE:', state.value)

        # elif neck_pos > 0.46:
        #     clientLogger.info('Head raised', neck_pos)
        #     state.value = 'down'
        else:
            cmd_pos = 100.0

    if state.value == 'down':
        # clientLogger.info('Going down')
        cmd_pos = -100.0
        if neck_pos <= 0.1:  # Head lowered
            state.value = 'rest'

            clientLogger.info('STATE:', state.value)

    # cmd_pos = -0.3 + 0.15*np.sin(t)
    return std_msgs.msg.Float64(cmd_pos)