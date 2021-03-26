@nrp.Robot2Neuron()
def csv_rate_monitor(t, mossy, granule, purkinje, recorder, dcn):
        recorder.record_entry('mossy', t, mossy.rate)
        recorder.record_entry('granule', t, granule.rate)
        recorder.record_entry('purkinje', t, purkinje.rate)
        recorder.record_entry('dcn', t, dcn.rate)