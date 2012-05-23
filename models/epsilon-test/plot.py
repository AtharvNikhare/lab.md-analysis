#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def get_ke(line): 
  return float(line.split()[2])

# Ahh, thrown-together one-liners. Reads "initial ke" column from index.txt.
initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

print "Initial KE (eV)\tClassic KE (eV)\tsd\tNext Gen KE (eV)\tsd\tControl KE (eV)\tsd\n" 

for i in range(1, 6):
  classic_fname = "classic/model{}.data.txt".format(i)
  nextgen_fname = "nextgen/model{}.data.txt".format(i)
  nextgen_control_fname = "nextgen/model{}-control.data.txt".format(i)

  classic_data         = map(get_ke, open(classic_fname, 'r').readlines())
  nextgen_data         = map(get_ke, open(nextgen_fname, 'r').readlines())
  nextgen_control_data = map(get_ke, open(nextgen_control_fname, 'r').readlines())

  classic_ke = np.mean(classic_data)
  classic_sd = np.std(classic_data)
  nextgen_ke = np.mean(nextgen_data)
  nextgen_sd = np.std(nextgen_data)
  nextgen_control_ke = np.mean(nextgen_control_data)
  nextgen_control_sd = np.std(nextgen_control_data)

  print "{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t".format(
    initial_ke[i-1],
    classic_ke,
    classic_sd,
    nextgen_ke,
    nextgen_sd,
    nextgen_control_ke,
    nextgen_control_sd
  )
