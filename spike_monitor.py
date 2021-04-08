import hbp_nrp_cle.tf_framework as nrp

@nrp.NeuronMonitor(nrp.brain.circuit, nrp.spike_recorder)
def spike_monitor(t):
    return True
