from hbp_nrp_cle.brainsim import simulator as sim
from pyNN.random import RandomDistribution

import logging

__author__ = 'Alberto Antonietti, Edoardo Negri'

logger = logging.getLogger(__name__)

try:
    sim.nest.Install("cerebmodule")
    logger.info("cerebmodule installed correctly")
except Exception as e:  # DynamicModuleManagementError
    logger.info(e)
    logger.info("cerebmodule already installed")
    
CORES = 4
sim.nest.ResetKernel()
sim.nest.SetKernelStatus({'local_num_threads' : CORES,
                      'total_num_virtual_procs' : CORES,
                      'resolution' : 1.0,
                      'overwrite_files' : True})

# CEREBELLUM
PLAST1 = True   # PF-PC ex

#LTP1 = 0.005
LTP1 = 0.0
LTD1 = -0.03


Init_PFPC = {'distribution': 'uniform',
             'low': 1.0, 'high': 2.0}
# Init_PFPC = 1.0
Init_MFDCN = 0.4  # 0.3 troopo poco, 0.5 troppo?
Init_PCDCN = {'distribution': 'uniform',
             'low': -2.0, 'high': -1.0}
RECORDING_CELLS = True


def create_cereb():
    sim.nest.CopyModel('iaf_cond_exp', 'granular_neuron')
    sim.nest.CopyModel('iaf_cond_exp', 'purkinje_neuron')
    sim.nest.CopyModel('iaf_cond_exp', 'olivary_neuron')
    sim.nest.CopyModel('iaf_cond_exp', 'nuclear_neuron')

    sim.nest.SetDefaults('granular_neuron', {'t_ref': 1.0,
                                             'C_m': 2.0,
                                             'V_th': -40.0,
                                             'V_reset': -70.0,
                                             'g_L': 0.2,
                                             'tau_syn_ex': 0.5,
                                             'tau_syn_in': 10.0})

    sim.nest.SetDefaults('purkinje_neuron', {'t_ref': 2.0,
                                             'C_m': 400.0,
                                             'V_th': -52.0,
                                             'V_reset': -70.0,
                                             'g_L': 16.0,
                                             'tau_syn_ex': 0.5,
                                             'tau_syn_in': 1.6})

    sim.nest.SetDefaults('olivary_neuron', {'t_ref': 1.0,
                                            'C_m': 2.0,
                                            'V_th': -40.0,
                                            'V_reset': -70.0,
                                            'g_L': 0.2,
                                            'tau_syn_ex': 0.5,
                                            'tau_syn_in': 10.0})

    sim.nest.SetDefaults('nuclear_neuron', {'t_ref': 1.0,
                                            'C_m': 2.0,
                                            'V_th': -40.0,
                                            'V_reset': -70.0,
                                            'g_L': 0.2,
                                            'tau_syn_ex': 0.5,
                                            'tau_syn_in': 10.0})

    # Cell numbers
    MF_num = 100
    GR_num = MF_num*20
    PC_num = 72
    IO_num = PC_num
    DCN_num = int(PC_num/2)

    MF_pop = sim.create(sim.native_cell_type("parrot_neuron"), {}, MF_num)
    GR_pop = sim.create(sim.native_cell_type("granular_neuron"), {}, GR_num)
    PC_pop = sim.create(sim.native_cell_type("purkinje_neuron"), {}, PC_num)
    IO_pop = sim.create(sim.native_cell_type("olivary_neuron"), {}, IO_num)
    DCN_pop = sim.create(sim.native_cell_type("nuclear_neuron"), {}, DCN_num)

    MF = tuple(MF_pop.all_cells)
    GR = tuple(GR_pop.all_cells)
    PC = tuple(PC_pop.all_cells)
    IO = tuple(IO_pop.all_cells)
    DCN = tuple(DCN_pop.all_cells)

    logger.info(f"MF: {min(MF)}, {max(MF)}")
    logger.info(f"GR: {min(GR)}, {max(GR)}")
    logger.info(f"PC: {min(PC)}, {max(PC)}")
    logger.info(f"IO: {min(IO)}, {max(IO)}")
    logger.info(f"DCN: {min(DCN)}, {max(DCN)}")

    if PLAST1:
        vt = sim.nest.Create("volume_transmitter_alberto", PC_num)
        for n, vti in enumerate(vt):
            sim.nest.SetStatus([vti], {"vt_num": n})

    recdict2 = {"to_memory": False,
                "to_file":    True,
                "label":     "PFPC_",
                "senders":    GR,
                "targets":    PC}

    WeightPFPC = sim.nest.Create('weight_recorder', params=recdict2)

    MFGR_conn_param = {"model": "static_synapse",
                       "weight": {'distribution': 'uniform',
                                  # -> 0.75 GR fire at 7 Hz
                                  'low': 0.6, 'high': 1.2},
                       "delay": 1.0}

    PCDCN_conn_param = {"model": "static_synapse",
		         "weight": Init_PCDCN,
		         "delay": 1.0}

    # MF-GR excitatory fixed connections
    # each GR receives 4 connections from 4 random granule cells
    sim.nest.Connect(MF[:50], GR[:1000], {'rule': 'fixed_indegree',
                               'indegree': 4,
                               "multapses": False}, MFGR_conn_param)
                               
    sim.nest.Connect(MF[50:], GR[1000:], {'rule': 'fixed_indegree',
                              'indegree': 4,
                              "multapses": False}, MFGR_conn_param)

                              
                  
    # A_minus - Amplitude of weight change for depression
    # A_plus - Amplitude of weight change for facilitation
    # Wmin - Minimal synaptic weight
    # Wmax - Maximal synaptic weight

    if PLAST1:
        sim.nest.SetDefaults('stdp_synapse_sinexp',
                             {"A_minus":   LTD1,
                              "A_plus":    LTP1,
                              "Wmin":      0.0,
                              "Wmax":      4.0,
                              "vt":        vt[0],
                              "weight_recorder": WeightPFPC[0]})

        PFPC_conn_param = {"model":  'stdp_synapse_sinexp',
                           "weight": Init_PFPC,
                           "delay":  1.0}

        # PF-PC excitatory plastic connections
        # each PC receives the random 80% of the GR
        for i, PCi in enumerate(PC):
            sim.nest.Connect(GR, [PCi],
                             {'rule': 'fixed_indegree',
                              'indegree': int(0.8*GR_num),
                              "multapses": False},
                             PFPC_conn_param)
            A = sim.nest.GetConnections(GR, [PCi])
            sim.nest.SetStatus(A, {'vt_num': float(i)})
    else:
        PFPC_conn_param = {"model":  "static_synapse",
                           "weight": Init_PFPC,
                           "delay":  1.0}
        sim.nest.Connect(GR, PC,
                         {'rule': 'fixed_indegree',
                          'indegree': int(0.8*GR_num),
                          "multapses": False},
                         PFPC_conn_param)

    PFPC_conn = sim.nest.GetConnections(GR, PC)

    if PLAST1:
        # IO-PC teaching connections
        # Each IO is one-to-one connected with each PC
        sim.nest.Connect(IO, vt, {'rule': 'one_to_one'},
                         {"model": "static_synapse",
                          "weight": 1.0, "delay": 1.0})
        sim.nest.GetConnections(IO, vt)  # IOPC_conn


    MFDCN_conn_param = {"model":  "static_synapse",
                        "weight": Init_MFDCN,
                        "delay":  15.0}
    sim.nest.Connect(MF, DCN, 'all_to_all', MFDCN_conn_param)

    # PC-DCN inhibitory connections
    # each DCN receives 2 connections from 2 contiguous PC
    count_DCN = 0
    for P in range(PC_num):
        sim.nest.Connect([PC[P]], [DCN[count_DCN]],
                         'one_to_one', PCDCN_conn_param)

        if P % 2 == 1:
            count_DCN += 1

    # circuit = MF_pop + PC_pop + IO_pop + DCN_pop
    # return circuit
    return MF_pop, GR_pop, PC_pop, IO_pop, DCN_pop, PFPC_conn


def create_brain():
    """
    Initializes PyNN with the neuronal network that has to be simulated
    """
    #sim.setup(timestep=0.1, min_delay=0.1, max_delay=100.0,
    #          threads=1, rng_seeds=[1234])

    # Parameters were taken from the husky braitenberg brain experiment

    SENSORPARAMS = {'cm': 0.025,
                    'v_rest': -60.5,
                    'tau_m': 10.0,
                    'e_rev_E': 0.0,
                    'e_rev_I': -75.0,
                    'v_reset': -60.5,
                    'v_thresh': -60.0,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 2.5,
                    'tau_syn_I': 2.5}

    # SYNAPSE_PARAMS = {"weight": 0.5e-4,
    #                   "delay": 20.0,
    #                   'U': 1.0,
    #                   'tau_rec': 1.0,
    #                   'tau_facil': 1.0}

    cell_class = sim.IF_cond_alpha(**SENSORPARAMS)
    #bigcell_class = sim.IF_cond_alpha(**BIGCELPARAMS)

    # ~100 neurons per follicle (McElvain 2018)
    n_whisks = 4

    #
    # Populations
    #
    MF_pop, GR_pop, PC_pop, IO_pop, DCN_pop, PFPC_conn = create_cereb()
    

    def population(size, cell_class=cell_class):
        return sim.Population(size=size, cellclass=cell_class)

    # CPG
    cpg = population(1)

    # Facial Nucleus motor neurons
    fn_pro = population(n_whisks*20)
    fn_ret = population(2*20)

    # Trigeminal Ganglion sensory afferents
    tg_pop_size = n_whisks*20
    tg_pr = population(tg_pop_size)
    tg_ct = population(tg_pop_size)
    tg_dt = population(tg_pop_size)
    tg_ht = population(tg_pop_size)
    tg_ws = population(tg_pop_size)

    
    logger.info(f"tg_pr: {min(tg_pr)}, {max(tg_pr)}")
    logger.info(f"tg_ct: {min(tg_ct)}, {max(tg_ct)}")
    logger.info(f"tg_dt: {min(tg_dt)}, {max(tg_dt)}")
    logger.info(f"tg_ht: {min(tg_ht)}, {max(tg_ht)}")
    logger.info(f"tg_ws: {min(tg_ws)}, {max(tg_ws)}")

    # Trigeminal Nucleus interneurons
    tn_ct = population(n_whisks)
    tn_phase = population(tg_pop_size)
    
    logger.info(f"tn_ct: {min(tn_ct)}, {max(tn_ct)}")
    logger.info(f"tn_phase: {min(tn_phase)}, {max(tn_phase)}")

    # Head movement in-out neurons
    reward = population(1)

    #
    # Projections
    #
    all_to_all = sim.AllToAllConnector()
    one_to_one = sim.OneToOneConnector()

    def static_syn(w, delay=1.0):
        return sim.StaticSynapse(weight=w, delay=delay)

    # CPG ---------> protractors
    # CPG -[delay]-> retractors
    random_weights = RandomDistribution('uniform', low=0.0, high=0.0001)
    sim.Projection(cpg, fn_pro, all_to_all, static_syn(random_weights))
    sim.Projection(cpg, fn_ret, all_to_all, static_syn(random_weights, 50.0))

    # Disynaptic reflex: tg_ct --> tn_ct --> fn_moto
    # tg_ct --> tn_ct
    syn = sim.StaticSynapse(weight=10.0)
    for i in range(n_whisks):
        begin = i*20
        end = (i+1)*20
        sim.Projection(tg_ct[begin:end], tn_ct[i:i+1], all_to_all, syn)

    fan_out = sim.FixedNumberPostConnector(n=4)
    to_one = sim.FixedNumberPostConnector(n=1)  # like ont_to_one but random
    sim.Projection(tg_pr, MF_pop[10:90], one_to_one, static_syn(50.0))
    sim.Projection(tn_phase, MF_pop[10:90], one_to_one, static_syn(50.0))

    # Protractors activation
    random_weights = RandomDistribution('uniform', low=0.0, high=0.00001)
    syn = sim.StaticSynapse(weight=random_weights, delay=7.5)
    for i in range(n_whisks):
        begin = i*20
        end = (i+1)*20
        sim.Projection(tn_ct[i:i+1], fn_pro[begin:end], all_to_all, syn)

    # Retractors inhibition
    random_weights = RandomDistribution('uniform', low=-0.00001, high=0.0)
    syn = sim.StaticSynapse(weight=random_weights, delay=7.5)
    sim.Projection(tn_ct[:2], fn_ret[:20], all_to_all, syn)
    sim.Projection(tn_ct[2:], fn_ret[20:], all_to_all, syn)
    #

    # Reward
    sim.Projection(reward, IO_pop, all_to_all, static_syn(10.0))
    #

    #
    # Assemblies
    #
    tg_ganglion = sim.Assembly(tg_pr, tg_ct, tg_dt, tg_ht, tg_ws)
    fn_moto = sim.Assembly(fn_pro, fn_ret)
    # cereb = sim.Assembly(MF_pop, PC_pop, IO_pop, DCN_pop)

    logger.info(f"TG: {min(tg_ganglion)}, {max(tg_ganglion)}")
    logger.info(f"FN: {min(fn_moto)}, {max(fn_moto)}")

    #
    # Views
    #
    # fn_pro_view = sim.PopulationView(fn_pro, slice(0, None, 5))
    # fn_ret_view = sim.PopulationView(fn_ret, slice(0, None, 5))
    # MF_view = sim.PopulationView(MF_pop, slice(0, None, 3))   # 300/3
    # GR_view = sim.PopulationView(GR_pop, slice(0, None, 60))  # (300*20)/60

    cells = sim.Assembly(cpg, fn_pro, fn_ret,
                         tg_pr, tg_ct, tg_dt, tg_ht, tg_ws,
                         tn_phase,
                         MF_pop, GR_pop, PC_pop, IO_pop, DCN_pop)

    populations = (
        cpg, fn_moto,
        tg_ganglion, tg_pr, tg_ws, tn_phase,
        MF_pop, GR_pop, PC_pop, DCN_pop,
        reward
    )
    return cells, populations, PFPC_conn


circuit, populations, PFPC_conn = create_brain()
(
    cpg, fn_moto,
    tg_ganglion, tg_pr, tg_ws, tn_phase,
    mossy, granule, purkinje, dcn,
    reward
) = populations
