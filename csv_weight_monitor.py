import hbp_nrp_cle.tf_framework as nrp
from cle_ros_msgs.msg import SpikeEvent
from hbp_nrp_cle.robotsim.RobotInterface import Topic

@nrp.MapCSVRecorder("recorder", filename="weights.csv", headers=["name", "t", "mean", "std"])

@nrp.Robot2Neuron()
def csv_weight_monitor(t, recorder):
        from hbp_nrp_cle.brainsim import simulator as sim
        import numpy as np

        if np.mod(int(t*1000.0), 1000) == 0:
            PFPC_conn = nrp.config.brain_root.PFPC_conn
            PFPC_w = sim.nest.GetStatus(PFPC_conn, keys="weight")

            recorder.record_entry('PFPC', t, np.mean(PFPC_w), np.std(PFPC_w))
