import hbp_nrp_cle.tf_framework as nrp

@nrp.MapSpikeSource("cpg", nrp.brain.cpg, nrp.fixed_frequency)
@nrp.Robot2Neuron()
def pattern_generator(t, cpg):
    f = 4.0
    cpg.rate = f