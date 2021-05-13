import hbp_nrp_cle.tf_framework as nrp
from hbp_nrp_cle.robotsim.RobotInterface import Topic
import std_msgs.msg
# import numpy as np
from hbp_nrp_excontrol.logs import clientLogger
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelState
from std_msgs.msg import String

@nrp.MapSpikeSource("reward", nrp.brain.reward, nrp.poisson, delay=1.0)
@nrp.MapCSVRecorder("recorder", filename="events.csv",
                    headers=["type", "time", "event"])
@nrp.MapVariable('state', initial_value='rest')
@nrp.MapVariable('go_trial', initial_value=False)
@nrp.MapRobotSubscriber("joint_states",
                        Topic("/mouse/joint_states", JointState))
@nrp.MapRobotSubscriber("gonogo",
                        Topic("/go_nogo_state", String))
@nrp.MapSpikeSink("dcn", nrp.brain.dcn, nrp.population_rate)
@nrp.Neuron2Robot(Topic('/mouse/neck_joint/cmd_pos', std_msgs.msg.Float64))
def head_up(t, reward, recorder, state, joint_states, go_trial, gonogo, dcn):
    cmd_pos = 0.0
    neck_pos = 0.0
    reward.rate = 0.0
    
    go = gonogo.value
    if go:
        if go.data[:2] == "GO":
            go_trial = True
        else:
            go_trial = False
    
    if joint_states.value:
        states = joint_states.value
        for i in range(len(states.name)):
            if states.name[i] == 'neck_joint':
                neck_pos = states.position[i]
                #clientLogger.info('neck_pos', neck_pos)
                
    if state.value == 'rest':
        if dcn.rate > 0.1:
            clientLogger.info('dcn rate', dcn.rate)

        if dcn.rate > 50.0:
            state.value = 'up'
            recorder.record_entry('head', t, 'up')
            clientLogger.info('STATE:', state.value)
            
        cmd_pos = 0.0

    if state.value == 'up':
        #clientLogger.info('neck_pos', neck_pos)
        
        if neck_pos < -0.25:
            clientLogger.info('Head raised', neck_pos)
            if go_trial:
                reward.rate = 100.0
                clientLogger.info('Sending reward')
                recorder.record_entry('contact', t, 'reward')
            else:
                clientLogger.info('NO reward')
                recorder.record_entry('contact', t, 'no_reward')
            state.value = 'down'
        cmd_pos = -0.5

    if state.value == 'down':

        cmd_pos = 0.5
        if neck_pos >= -0.05:  # Head lowered
            state.value = 'rest'
            clientLogger.info('STATE:', state.value)
            cmd_pos = 0.0

    return std_msgs.msg.Float64(cmd_pos)
