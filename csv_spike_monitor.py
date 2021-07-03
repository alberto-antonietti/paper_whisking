import hbp_nrp_cle.tf_framework as nrp
from cle_ros_msgs.msg import SpikeEvent
from hbp_nrp_cle.robotsim.RobotInterface import Topic

@nrp.MapCSVRecorder("recorder", filename="spikes.csv", headers=["id", "time"])
@nrp.MapSpikeSink("record_neurons", nrp.brain.circuit, nrp.spike_recorder)
@nrp.Neuron2Robot(Topic('/monitor/spike_recorder', SpikeEvent))
def csv_spike_monitor(t, recorder, record_neurons):
    for i in range(0, len(record_neurons.times)):
        recorder.record_entry(
            record_neurons.times[i][0],
            record_neurons.times[i][1]
        )