#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import bisect
import sys

def get_time(line):
  return float(line.split()[0])  

def get_ke(line): 
  return float(line.split()[1])

def get_te(line):
  return float(line.split()[2])

initial_ke = map(lambda (x): float(x.split()[1]), open('index.txt').readlines()[4:])

for dataset in ('unmodified', 'modified'):
  plt.clf()
  suffix = '' if dataset == 'unmodified' else '-control'

  for i in range(1,6):
    # plt.subplot(2, 1, 1 + i/5, title="Next Gen MW Kinetic Energy, initial KE = {:.4f} eV".format(initial_ke[i-1]))
    fname = 'nextgen/model{}{}.data.txt'.format(i, suffix)
    lines =  open(fname, 'r').readlines()

    time = map(get_time, lines)
    start = bisect.bisect_left(time, 100000)

    time = time[start:] 
    ke = map(get_ke, lines[start:])
    te = map(get_te, lines[start:])
    
    plt.xlabel("time (fs)")
    plt.ylabel("Energy (eV)")
    plt.ylim(2, 8)

    plt.plot(time, ke, label = "Kinetic Energy")
    plt.plot(time, te, label = "Total Energy")

    plt.title("Time series of {} Next Gen MW kinetic and total energy".format(dataset))
    
  plt.savefig('lj-extended-data{}'.format(suffix), dpi=300)