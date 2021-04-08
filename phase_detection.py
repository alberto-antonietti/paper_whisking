import hbp_nrp_cle.tf_framework as nrp
# import numpy as np


@nrp.MapSpikeSink("tg_pr",
                  nrp.map_neurons(range(4*20),
                                  lambda i: nrp.brain.tg_pr[i]),
                  nrp.spike_recorder)
@nrp.MapSpikeSink("tg_ws",
                  nrp.map_neurons(range(4*20),
                                  lambda i: nrp.brain.tg_ws[i]),
                  nrp.population_rate)
@nrp.MapSpikeSource("tn_phase",
                    nrp.map_neurons(range(4*20),
                                    lambda i: nrp.brain.tn_phase[i]),
                    nrp.poisson, delay=1.0)
@nrp.Robot2Neuron()
def phase_detection(t, tg_pr, tg_ws, tn_phase):
    for i in range(4*20):
        if tg_pr[i].spiked:
            tn_phase[i].rate = tg_ws[i].rate
        else:
            tn_phase[i].rate = 0.0