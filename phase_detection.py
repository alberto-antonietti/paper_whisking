@nrp.Robot2Neuron()
def phase_detection(t, tg_pr, tg_ws, tn_phase):
    for i in range(4*20):
        if tg_pr[i].spiked:
            tn_phase[i].rate = tg_ws[i].rate
        else:
            tn_phase[i].rate = 0.0