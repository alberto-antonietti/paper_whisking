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
@nrp.Neuron2Robot(Topic('/mouse/neck_joint/cmd_pos', std_msgs.msg.Float64))
def head_up(t, recorder, state, joint_states, dcn):
    cmd_pos = 0.0
    neck_pos = 0.0
    target = 0.0
    
    if joint_states.value:
        states = joint_states.value
        for i in range(len(states.name)):
            if states.name[i] == 'neck_joint':
                neck_pos = states.position[i]
                clientLogger.info('neck_pos', neck_pos)
                
    if neck_pos > target:
        cmd_pos = 5.0
    elif neck_pos < target:
        cmd_pos = -5.0

    '''
    if state.value == 'rest':
        if dcn.rate > 0.1:
            clientLogger.info('dcn rate', dcn.rate)

        if dcn.rate > 50.0:
            state.value = 'up'
            recorder.record_entry('head', t, 'up')
            clientLogger.info('STATE:', state.value)

    if state.value == 'up':
        clientLogger.info('neck_pos', neck_pos)
        
        if neck_pos > 0.46:
            clientLogger.info('Head raised', neck_pos)
            state.value = 'down'
        cmd_pos = 1.0

    if state.value == 'down':

        cmd_pos = 0.1
        if neck_pos <= 0.1:  # Head lowered
            state.value = 'rest'
            clientLogger.info('STATE:', state.value)
    '''
    return std_msgs.msg.Float64(cmd_pos)
