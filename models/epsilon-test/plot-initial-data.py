#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def get_nextgen_ke(line): 
  return float(line.split()[2])

def get_classic_ke(line):
  return 98.0 * float(line.split()[2])

def get_te(line):
  return float(line.split()[3])

initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

for data_type in ('classic', 'nextgen'):
  plt.title("Initial MW Kinetic Energy, initial KE = {:.4f} eV".format(initial_ke[0]))
  fname = '{}/model1-initial.data.txt'.format(data_type)
  lines =  open(fname, 'r').readlines()
  if data_type == 'classic':
    ke = map(get_classic_ke, lines)
  else:
    ke = map(get_nextgen_ke, lines)
  plt.ylim(2, 12)
  plt.ylabel("Kinetic Energy (eV)")
  plt.xlabel("time step")
  plt.plot(ke, label = data_type)
  plt.legend()
  
plt.savefig('lj-initial-data', dpi=300)