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

index = open('index.txt').readlines()[1:]

for index_line in index:
  if len(index_line) > 0:
    (model_num, epsilon, initial_ke, final_ke) = index_line .split('\t')

    fname = 'nextgen/model{}.data.txt'.format(model_num)
    lines =  open(fname, 'r').readlines()

    time = map(get_time, lines)
    start = bisect.bisect_left(time, 20000)
    end = bisect.bisect_left(time, 40000)

    time = time[start:end+1]
    ke = map(get_ke, lines[start:end+1])
    
    plt.xlabel("time (fs)")
    plt.ylabel("Energy (eV)")
    plt.ylim(-2, 10)

    plt.plot(time, ke, label = "Kinetic Energy")

    plt.title("Time series of Next Gen MW kinetic energy")

plt.savefig('lj-extended-data.png', dpi=300)