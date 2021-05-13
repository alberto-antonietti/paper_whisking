import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv) < 2:
    sys.exit(1)


folder = sys.argv[1]

if folder[-1] != "/":
    folder = folder + "/"

with open(folder + "spikes.csv") as f:
    reader = csv.reader(f)
    rows = [r for r in reader][1:]

events = {}  # {id: spike times}

for row in rows:
    n_id, t = row
    n_id = int(float(n_id))
    t = float(t)
    
    try:
    	events[n_id].append(t)
    except:
    	events[n_id] = []


n_ids = np.array(list(events.keys()), dtype=int)
n_ids.sort()

go_x = np.array([0.0])
go_y = np.array([0.0])
with open(folder + "gonogo_events.csv") as f:
    reader = csv.reader(f)
    rows = [r for r in reader][1:]
    for row in rows:
        if row[0] == "GO":
    	    go_x = np.concatenate((go_x, np.array([1000.0 * float(row[1]), 1000.0 * float(row[1])])))
    	    go_y = np.concatenate((go_y, np.array([0.0, 1.0])))
        elif row[0] == "NOGO":
    	    go_x = np.concatenate((go_x, np.array([1000.0 * float(row[1]), 1000.0 * float(row[1])])))
    	    go_y = np.concatenate((go_y, np.array([1.0, 0.0])))


#MF: 3, 102
#GR: 105, 2104
#PC: 2107, 2178
#IO: 2181, 2252
#DCN: 2255, 2290

#tg_pr: 2493, 2572
#tg_ct: 2575, 2654
#tg_dt: 2657, 2736
#tg_ht: 2739, 2818
#tg_ws: 2821, 2900


#TG: 2493, 2900
#FN: 2369, 2490


mf_range = range(3, 103)
gr_range = range(105, 2105)
pc_range = range(2107, 2178)
io_range = range(2181, 2253)
dcn_range = range(2255, 2291)
tg_range = range(2493, 2901)
fn_range = range(2369, 2491)


def plot_spikes(color, pop_range, label, ax):
    global n_ids
    label_done = False
    for i in n_ids:
        if i in pop_range:
            spikes = events[i]
            if not label_done:
                ax.plot(spikes, np.full_like(spikes, i), marker=".", label=label, color=color, linestyle="None")
                label_done = True
            else:
                ax.plot(spikes, np.full_like(spikes, i), marker=".", color=color, linestyle="None")

fig_handle = plt.figure()

ax = fig_handle.add_subplot(121)
ax.set_xlabel('$t$ (ms)')

plot_spikes('orange', fn_range, 'Facial Nuclei', ax)
plot_spikes('grey', tg_range, 'Trigeminal Ganglion', ax)
ax.plot(go_x, 2369 + go_y*550, "k")
plt.legend()


ax = fig_handle.add_subplot(122)
ax.set_xlabel('$t$ (ms)')
plot_spikes('blue', mf_range, 'Mossy', ax)
plot_spikes('red', gr_range, 'Granule', ax)
plot_spikes('green', pc_range, 'Purkinje', ax)
plot_spikes('magenta', io_range, 'Inferior Olive', ax)
plot_spikes('black', dcn_range, 'Deep Cerebellar Nuclei', ax)
ax.plot(go_x, go_y*2290, "k")
plt.legend()



#FN: 2369, 2490
#TG: 2493, 2900
#tg_pr: 2493, 2572
#tg_ct: 2575, 2654
#tg_dt: 2657, 2736
#tg_ht: 2739, 2818
#tg_ws: 2821, 2900
#tn_ct: 2903, 2906
#tn_phase: 2909, 2988



tgpr_range = range(2493, 2573)
tgct_range = range(2575, 2655)
tgdt_range = range(2657, 2737)
tght_range = range(2739, 2819)
tgws_range = range(2821, 2901)
tnct_range = range(2903, 2907)
tnph_range = range(2909, 2989)

fig_handle = plt.figure()
ax = fig_handle.add_subplot(111)
ax.set_xlabel('$t$ (ms)')

plot_spikes('orange', tgpr_range, 'TG Pression', ax)
plot_spikes('grey', tgct_range, 'TG Contact', ax)
plot_spikes('blue', tgdt_range, 'TG Detach', ax)
plot_spikes('red', tght_range, 'TG High Threshold', ax)
plot_spikes('green', tgws_range, 'TG Whisking', ax)
plot_spikes('black', tnct_range, 'TN Contact', ax)
plot_spikes('purple', tnph_range, 'TN Phase', ax)

ax.plot(go_x, 2492 + go_y*620, "k")

plt.legend()
plt.show()
