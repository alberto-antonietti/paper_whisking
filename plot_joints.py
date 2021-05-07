import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv) < 2:
    sys.exit(1)


folder = sys.argv[1]

if folder[-1] != "/":
    folder = folder + "/"
    
file_name = folder + "joints_positions.csv"

with open(file_name) as f:
    reader = csv.reader(f)
    rows = [r for r in reader][1:]

joints = {}

for r in rows:
    name = r[0]
    t = float(r[1])
    pos = float(r[2])

    if name not in joints.keys():
        joints[name] = [], []

    if pos != 0.0:
        joints[name][0].append(t)
        joints[name][1].append(pos)


# L0 R0 L1 R1
joint_names = ['whisker_' + side + str(i) + '_joint'
               for i in range(2) for side in 'LR']

fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
ax = ax.ravel()
for i, joint_name in enumerate(joint_names):
    joint = joints[joint_name]
    plt.tight_layout()

    ax[i].set_title(joint_name)
    ax[i].set_xlabel('$t$ (s)')
    ax[i].set_ylabel('$angle$ (rad)')

    ax[i].plot(joint[0], joint[1])

plt.show()
