#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def get_ke(line): 
  return float(line.split()[2])

def get_te(line):
  return float(line.split()[3])

initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

for i in (1, 5):
  plt.subplot(2, 1, 1 + i/5, title="Next Gen MW Kinetic Energy, initial KE = {:.4f} eV".format(initial_ke[i]))
  fname = 'nextgen/model{}-extended.data.txt'.format(i)
  lines =  open(fname, 'r').readlines()
  ke = map(get_ke, lines)
  te = map(get_te, lines)
  plt.ylim(2, 8)
  plt.ylabel("Energy (eV)")
  plt.plot(ke, label = "Kinetic Energy")
  plt.plot(te, label = "Total Energy")
  plt.legend()
  
plt.savefig('lj-extended-data', dpi=300)