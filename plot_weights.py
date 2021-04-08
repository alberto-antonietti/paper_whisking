import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit(1)

file_name = sys.argv[1]


with open(file_name) as f:
    lines = f.readlines()[1:]


times = []
weights = []
for line in lines:
    t, w_line = line.split(',')

    t = float(t)
    ws = [float(w) for w in w_line.split()]

    times.append(t)
    weights.append(ws)

# each line is weights at give time -> each line is a synapse
syn_w = zip(*weights)

# print(times[0])
# print(weights[0])
# print(syn_w[0])

for syn in syn_w[::10]:
    h = plt.plot(times, syn, 'b')
    h[0].set_alpha(0.5)

plt.show()
