import hbp_nrp_cle.tf_framework as nrp
from std_msgs.msg import String
import logging
logger = logging.getLogger()

@nrp.MapVariable("go_nogo_variable", scope=nrp.GLOBAL)


@nrp.MapCSVRecorder("recorder", filename="gonogo_events.csv",
                    headers=["event", "time"])
@nrp.MapRobotSubscriber("go_nogo", Topic("/go_nogo_state", String))

@nrp.Robot2Neuron()
def csv_event_monitor(t, recorder, go_nogo, go_nogo_variable):
    if go_nogo.value:
        data = go_nogo.value.data
        current_state = data.split(" ")[0]
        if go_nogo_variable.value != current_state:
            logger.info(current_state)
            go_nogo_variable.value = current_state
    
            if go_nogo_variable.value == "GO":
                recorder.record_entry('GO', t)
            elif go_nogo_variable.value == "NOGO":
                recorder.record_entry('NOGO', t)
