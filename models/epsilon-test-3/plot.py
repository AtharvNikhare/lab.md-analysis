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
initial_pes = np.array([])
initial_kes = np.array([])
final_kes = np.array([])


index = open('index.txt').readlines()[1:]

i = -1

for index_line in index:
  if len(index_line) > 0:
    i += 1

    model_num = int(index_line.split('\t')[0])
    (epsilon, initial_pe, initial_ke, final_ke) = map(float, index_line.split('\t')[1:])

    epsilons = np.append(epsilons, epsilon)
    initial_pes = np.append(initial_pes, initial_pe)
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
plt.ylim(0, 0.13)

# the experimental condition: all indices for which final KE > 0
exp = final_kes > 0

def est_epsilon(measured_final_ke, final_ke_sd, initial_ke, epsilons, initial_pes):
  """
  Estimate epsilon from final KE, initial KE, and initial total energy for "correct" epsilon 
  Vectorized form. Returns (epsilons, standard deviations)
  """
  epsilon_over_te = epsilons / -initial_pes
  return ( (initial_ke - measured_final_ke) * epsilon_over_te, final_ke_sd * epsilon_over_te )

(classic_est_epsilon, classic_est_sd) = est_epsilon(classic_ke[exp], classic_sd[exp], initial_kes[exp], epsilons[exp], initial_pes[exp])
(nextgen_est_epsilon, nextgen_est_sd) = est_epsilon(nextgen_ke[exp], nextgen_sd[exp], initial_kes[exp], epsilons[exp], initial_pes[exp])

# Note, for what it's worth, that the error bars aren't very meaningful .. we're not doing the
# "correct" error analysis (not least because we're not accounting at all for the correlations
# in the timeseries data)

plt.errorbar(epsilons[exp], classic_est_epsilon, yerr=classic_est_sd, label='Classic MW')
plt.errorbar(epsilons[exp], nextgen_est_epsilon, yerr=nextgen_est_sd, label='Next Gen MW')
plt.plot(epsilons[exp], epsilons[exp], label='Expected value')

plt.title("Experimental estimates of actual LJ epsilon from heat of fusion\n(note: these estimates are biased slightly low as epsilon increases)")
plt.xlabel(r'epsilon (eV)')
plt.ylabel(r'Measured value of epsilon (eV)')
plt.legend(loc='lower center')
plt.savefig('lj-epsilon-test', dpi=300)
