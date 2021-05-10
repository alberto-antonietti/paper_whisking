import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit(1)

folder = sys.argv[1]

if folder[-1] != "/":
    folder = folder + "/"
    
file_name = folder + "weights.csv"



with open(file_name) as f:
    lines = f.readlines()[1:]


times = []
weights = []
for line in lines:
    _, t, w_line, _ = line.split(',')

    t = float(t)
    ws = [float(w) for w in w_line.split()]

    times.append(t)
    weights.append(ws)


plt.figure()
h = plt.plot(times, weights, 'b')
h[0].set_alpha(0.5)

plt.show()
