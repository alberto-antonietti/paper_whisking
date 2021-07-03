import hbp_nrp_cle.tf_framework as nrp
from sensor_msgs.msg import JointState
from hbp_nrp_cle.robotsim.RobotInterface import Topic

@nrp.MapRobotSubscriber("joint_states", Topic('/mouse/joint_states', JointState))
@nrp.MapCSVRecorder("recorder",
                    filename="joints_positions.csv",
                    headers=["Name", "time", "Position"])

@nrp.Robot2Neuron()
def csv_joint_state_monitor(t, joint_states, recorder):
    nw = 2  # whiskers per side

    if joint_states.value:
        states = joint_states.value
        for i in range(len(states.name)):
            for side in ['L', 'R']:
                for w_i in range(nw):
                    joint_name = 'whisker_' + side + str(w_i) + '_joint'
                    if states.name[i] == joint_name:
                        position = states.position[i]
                        recorder.record_entry(joint_name, t, position)