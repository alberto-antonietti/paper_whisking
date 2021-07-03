import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv) < 2:
    sys.exit(1)


folder = sys.argv[1]

if folder[-1] != "/":
    folder = folder + "/"

file_name = folder + "events.csv"

with open(file_name) as f:
    reader = csv.reader(f)
    events = [r for r in reader][1:]
    
file_name = folder + "gonogo_events.csv"

with open(file_name) as f:
    reader = csv.reader(f)
    gonogo = [r for r in reader][1:]
    
N_trial = int(float(gonogo[-1][1])) // 2

go_matrix = np.zeros(N_trial, dtype=int)
counter = 0
go_matrix[counter] = (gonogo[counter][0] == "GO")
counter += 1
next_change = int(float(gonogo[counter][1])) // 2
for n in range(1, N_trial):
    if n < next_change:
        go_matrix[n] = go_matrix[n - 1]
    elif n == next_change:
        go_matrix[n] = not(go_matrix[n - 1])
        counter += 1
        next_change = int(float(gonogo[counter][1])) // 2
        
hits = np.zeros(N_trial, dtype=int)
good_response = np.zeros(N_trial, dtype=int)
false_alarm = np.zeros(N_trial, dtype=int)

for e in events:
    if e[0] == "contact":
        trial_of_event = int(float(e[1])) // 2
        if int(float(e[1]) - 0.02) // 2 != int(float(e[1])) // 2:
            print(e[1])
        if trial_of_event < N_trial:
            
            hits[trial_of_event] = 1
        
            if e[2] == "no_reward":
                false_alarm[trial_of_event] = 1
            else:
                good_response[trial_of_event] = 1
                
            
plt.figure()
plt.plot(hits, "k", label="hits", linestyle="", marker='o')
plt.plot(false_alarm, "r", label="false alarm", linestyle="", marker='x', markersize=10)
plt.ylim([0.5, 1.55])
plt.legend()

N_sess = N_trial // 10

true_rate =  np.zeros(N_sess, dtype=float)
false_rate =  np.zeros(N_sess, dtype=float)
for s in range(N_sess):
    true_rate[s] = np.sum(good_response[s * 10: (s + 1) * 10]) * 20
    false_rate[s] = np.sum(false_alarm[s * 10: (s + 1) * 10]) * 20
print(true_rate)
plt.figure()
plt.plot(range(1, N_sess + 1),true_rate, "k", label="true rate", marker='o')
plt.plot(range(1, N_sess + 1),false_rate, "r", label="false rate", marker='x', markersize=10)
plt.ylim([-5, 105])
plt.legend()
plt.savefig(folder + "rates.png")
plt.show()
