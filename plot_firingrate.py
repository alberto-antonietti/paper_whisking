import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv) < 3:
    sys.exit(1)


folder = sys.argv[1]
binw = int(sys.argv[2])  # ms

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

tmax = int(max(events.values())[0])

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


def plot_firingrate(color, pop_range, label, ax):
    global binw
    global n_ids
    spikes = []
    for i in n_ids:
        if i in pop_range:
            spikes.append(events[i])
    if len(spikes) == 0:
        return
    spikes = np.concatenate(spikes)
    
    frequency = []
    for t in range(0, tmax, binw):
        frequency.append(len(np.where(np.logical_and(spikes > t, spikes <= t + binw))[0]))
    
    frequency = np.array(frequency, dtype=float) * (1000.0 / binw) / len(pop_range)
    ax.bar(range(0, tmax, binw), frequency, width=binw, color=color)
    ax.set_title(label)
    
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
plot_firingrate('orange', fn_range, 'Facial Nuclei', ax1)
#ax1.plot(go_x, go_y, "k")

plot_firingrate('grey', tg_range, 'Trigeminal Ganglion', ax2)
ax2.plot(go_x, go_y, "k")
#ax2.set_xlabel('$t$ (ms)')

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, sharex=True)
plot_firingrate('blue', mf_range, 'Mossy', ax1)
#ax1.plot(go_x, go_y, "k")

plot_firingrate('red', gr_range, 'Granule', ax2)
#ax2.plot(go_x, go_y, "k")

plot_firingrate('green', pc_range, 'Purkinje', ax3)
#ax3.plot(go_x, go_y, "k")

plot_firingrate('magenta', io_range, 'Inferior Olive', ax4)
#ax4.plot(go_x, go_y, "k")

plot_firingrate('black', dcn_range, 'Deep Cerebellar Nuclei', ax5)
#ax5.plot(go_x, go_y, "k")
ax5.set_xlabel('$t$ (ms)')


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


fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(nrows=7, sharex=True)

plot_firingrate('orange', tgpr_range, 'TG Pression', ax1)
#ax1.plot(go_x, + go_y, "k")

plot_firingrate('grey', tgct_range, 'TG Contact', ax2)
#ax2.plot(go_x, + go_y, "k")

plot_firingrate('blue', tgdt_range, 'TG Detach', ax3)
#ax3.plot(go_x, + go_y, "k")

plot_firingrate('red', tght_range, 'TG High Threshold', ax4)
#ax4.plot(go_x, + go_y, "k")

plot_firingrate('green', tgws_range, 'TG Whisking', ax5)
#ax5.plot(go_x, + go_y, "k")

plot_firingrate('black', tnct_range, 'TN Contact', ax6)
#ax6.plot(go_x, + go_y, "k")

#ax7.set_xlabel('$t$ (ms)')
plot_firingrate('purple', tnph_range, 'TN Phase', ax7)
#ax7.plot(go_x, + go_y, "k")
plt.show()
