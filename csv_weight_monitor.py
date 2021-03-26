@nrp.Robot2Neuron()
def csv_weight_monitor(t, recorder):
        from hbp_nrp_cle.brainsim import simulator as sim
        import numpy as np

        PFPC_conn = nrp.config.brain_root.PFPC_conn
        PFPC_w = sim.nest.GetStatus(PFPC_conn, keys="weight")

        recorder.record_entry('PFPC', t, np.mean(PFPC_w), np.std(PFPC_w))