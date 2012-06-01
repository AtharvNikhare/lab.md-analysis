#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import bisect 
import sys

start_time = 100100
end_time   = 150000

def get_column(line, col):
  return float(line.split()[col])

def extract_nextgen_data(line):
  return (get_column(line, 0), get_column(line, 1))

def extract_classic_data(line):
  return (get_column(line, 1), 100*get_column(line, 2))

def get_data(fname, extract_data):
  (time, ke) = zip(*map(extract_data, open(fname, 'r').readlines()))
  
  start = bisect.bisect_left(time, start_time)
  end   = bisect.bisect_left(time, end_time)
  time  = time[start:end+1]
  ke    = ke[start:end+1]

  return (time, ke)

# Ahh, thrown-together one-liners. Reads "initial ke" column from index.txt.
initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

classic_time = []
classic_timeseries = []
nextgen_time = []
nextgen_timeseries = []
nextgen_control_time = []
nextgen_control_timeseries = []

classic_ke = []
classic_sd = []
nextgen_ke = []
nextgen_sd = []
nextgen_control_ke = []
nextgen_control_sd = []

print "Initial KE (eV)\tClassic KE (eV)\tsd\tNext Gen KE (eV)\tsd\tControl KE (eV)\tsd\n" 

for i in range(0, 5):
  classic_fname = "classic/model{}.data.txt".format(i+1)
  nextgen_fname = "nextgen/model{}.data.txt".format(i+1)
  nextgen_control_fname = "nextgen/model{}-control.data.txt".format(i+1)

  time, ke = get_data(classic_fname, extract_classic_data)
  classic_time.append(time)
  classic_timeseries.append(ke)

  time, ke = get_data(nextgen_fname, extract_nextgen_data)
  assert time == classic_time[i], "Expected  Next Gen data set to have same time values as Classic"
  nextgen_timeseries.append(ke)
  nextgen_time.append(time)

  time, ke = get_data(nextgen_control_fname, extract_nextgen_data)
  assert time == classic_time[i], "Expected Next Gen data set (modified epsilon) to have same time values as Classic"
  nextgen_control_timeseries.append(ke)
  nextgen_control_time.append(time)

  classic_ke.append( np.mean(classic_timeseries[i]) )
  classic_sd.append( np.std(classic_timeseries[i]) )
  nextgen_ke.append( np.mean(nextgen_timeseries[i]) )
  nextgen_sd.append( np.std(nextgen_timeseries[i]) )
  nextgen_control_ke.append( np.mean(nextgen_control_timeseries[i]) )
  nextgen_control_sd.append( np.std(nextgen_control_timeseries[i]) )

  print "{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t".format(
    initial_ke[i],
    classic_ke[i],
    classic_sd[i],
    nextgen_ke[i],
    nextgen_sd[i],
    nextgen_control_ke[i],
    nextgen_control_sd[i]
  )

# actually plot stuff

plt.xlim(-0.5, 3.0)

plt.errorbar(initial_ke, classic_ke, yerr=classic_sd, label='Classic MW')
plt.errorbar(initial_ke, nextgen_ke, yerr=nextgen_sd, label='Next Gen MW')
plt.errorbar(initial_ke, nextgen_control_ke, yerr=nextgen_control_sd, label=r'Next Gen MW, incorrect $\epsilon$')


plt.title("KE at equilibrium vs. initial KE (total energy held constant)\nFor Next Gen MW as of 5-29-2012");
plt.ylim(0, 10)
plt.xlabel(r'Initial KE of model (eV)')
plt.ylabel(r'Steady-state KE of model (eV)')
plt.legend(loc='lower center')
plt.savefig('lj-epsilon-test', dpi=300)

plt.clf()

def plot_one_series(time, ke, name, row):
  for i in range(0, 5):
    plt.subplot(3, 5, 5*(row-1) + i+1)
    plt.ylim(0,10)
    plt.plot(time[i], ke[i])

plot_one_series(classic_time, classic_timeseries, "Classic MW", 1)
plot_one_series(nextgen_time, nextgen_timeseries, "Next Gen MW", 2)
plot_one_series(nextgen_control_time, nextgen_control_timeseries, r'Next Gen MW, incorrect $\epsilon$', 3)

plt.savefig('lj-raw-data', dpi=300)