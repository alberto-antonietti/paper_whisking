import sys
import csv
import matplotlib.pyplot as plt


if len(sys.argv) < 2:
    sys.exit(1)

file_name = sys.argv[1]

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

for i, joint_name in enumerate(joint_names):
    joint = joints[joint_name]
    plt.subplot(2, 2, i+1)
    plt.tight_layout()

    plt.title(joint_name)
    plt.xlabel('$t$ (s)')
    plt.ylabel('$angle$ (rad)')

    plt.plot(joint[0], joint[1])

plt.show()
