#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import bisect 
import sys


def get_column(line, col):
  return float(line.split()[col])

def extract_nextgen_data(line):
  return (get_column(line, 0), get_column(line, 1))

def extract_classic_data(line):
  return (get_column(line, 1), 100*get_column(line, 2))

def get_data(fname, extract_data):
  return zip(*map(extract_data, open(fname, 'r').readlines()))

classic_time = []
classic_timeseries = []
classic_ke = np.array([])
classic_sd = np.array([])

nextgen_time = []
nextgen_timeseries = []
nextgen_ke = np.array([])
nextgen_sd = np.array([])

epsilons = np.array([])
initial_kes = np.array([])
final_kes = np.array([])

index = open('index.txt').readlines()[1:]

i = -1

for index_line in index:
  if len(index_line) > 0:
    i += 1

    model_num = int(index_line.split('\t')[0])
    (epsilon, initial_ke, final_ke) = map(float, index_line.split('\t')[1:])

    epsilons = np.append(epsilons, epsilon)
    initial_kes = np.append(initial_kes, initial_ke)
    final_kes = np.append(final_kes, final_ke)

    classic_fname = "classic/model{}.data.txt".format(model_num)
    nextgen_fname = "nextgen/model{}.data.txt".format(model_num)

    (time, ke) = get_data(classic_fname, extract_classic_data)
    classic_time.append(time)
    classic_timeseries.append(ke)

    start_time = time[0]
    end_time = time[-1]

    (time, ke) = get_data(nextgen_fname, extract_nextgen_data)

    start = bisect.bisect_left(time, start_time)
    end = 1 + bisect.bisect_left(time, end_time)
    time = time[start:end]
    ke = ke[start:end]

    assert time[0] == start_time, "Expected NextGen start time to match Classic start time"
    assert time[-1] == end_time, "Expected NextGen end time to match Classic end time"

    nextgen_time.append(time)
    nextgen_timeseries.append(ke)

    classic_ke = np.append( classic_ke, np.mean(classic_timeseries[i]) )
    classic_sd = np.append( classic_sd, np.std(classic_timeseries[i]) )
    nextgen_ke = np.append( nextgen_ke, np.mean(nextgen_timeseries[i]) )
    nextgen_sd = np.append( nextgen_sd, np.std(nextgen_timeseries[i]) )

    print "{:.3f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(epsilons[i], classic_ke[i], classic_sd[i], nextgen_ke[i], nextgen_sd[i])

# actually plot stuff

plt.xlim(0, 0.13)
plt.ylim(0, 15)

# the experimental condition: all indices for which final KE > 0
exp = final_kes > 0

plt.errorbar(epsilons[exp], classic_ke[exp], yerr=classic_sd[exp], label='Classic MW')
plt.errorbar(epsilons[exp], nextgen_ke[exp], yerr=nextgen_sd[exp], label='Next Gen MW')
plt.errorbar(epsilons[exp], final_kes[exp], label=r'Approx expected value')

plt.title("Comparison of Classic vs. Next Gen MW KE after melting solid")
plt.xlabel(r'Epsilon (eV)')
plt.ylabel(r'Steady-state KE of model (eV)')
plt.legend(loc='lower center')
plt.savefig('lj-epsilon-test', dpi=300)
