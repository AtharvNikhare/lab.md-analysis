#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def get_nextgen_ke(line): 
  return float(line.split()[2])

def get_classic_ke(line):
  return 98.0 * float(line.split()[2])

# Ahh, thrown-together one-liners. Reads "initial ke" column from index.txt.
initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

classic_data = []
nextgen_data = []
nextgen_control_data = []

classic_ke = []
classic_sd = []
nextgen_ke = []
nextgen_sd = []
nextgen_control_ke = []
nextgen_control_sd = []

print "Initial KE (eV)\tClassic KE (eV)\tsd\tNext Gen KE (eV)\tsd\tControl KE (eV)\tsd\n" 

for i in range(0, 7):
  classic_fname = "classic/model{}.data.txt".format(i)
  nextgen_fname = "nextgen/model{}.data.txt".format(i)
  nextgen_control_fname = "nextgen/model{}-control.data.txt".format(i)

  classic_data.append( map(get_classic_ke, open(classic_fname, 'r').readlines()) )
  nextgen_data.append( map(get_nextgen_ke, open(nextgen_fname, 'r').readlines()) )
  nextgen_control_data.append( map(get_nextgen_ke, open(nextgen_control_fname, 'r').readlines()) )

  classic_ke.append( np.mean(classic_data[i]) )
  classic_sd.append( np.std(classic_data[i]) )
  nextgen_ke.append( np.mean(nextgen_data[i]) )
  nextgen_sd.append( np.std(nextgen_data[i]) )
  nextgen_control_ke.append( np.mean(nextgen_control_data[i]) )
  nextgen_control_sd.append( np.std(nextgen_control_data[i]) )

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
plt.ylim(0, 8)
plt.xlabel(r'Initial KE of model (eV)')
plt.ylabel(r'Steady-state KE of model (eV)')
plt.legend(loc='lower center')
plt.savefig('lj-epsilon-test', dpi=300)

plt.clf()



def plot_one_series(data, name, row):
  for i in range(0, 7):
    plt.subplot(3, 7, i + (row - 1) * 7);
    plt.ylim(0,8)
    plt.plot(data[i-1])

plt.title("Time series of KE values")

plot_one_series(classic_data, "Classic MW", 1)
plot_one_series(nextgen_data, "Next Gen MW", 2)
plot_one_series(nextgen_control_data, r'Next Gen MW, incorrect $\epsilon$', 3)

plt.savefig('lj-raw-data', dpi=300)