#!/usr/bin/env python

import math
import numpy as np
import scipy

from scipy.optimize import fsolve

import pystache
import os
import errno
import subprocess

# some conversion constants for later
JOULES_PER_EV = 1.6021770000000003e-19
KILOGRAMS_PER_DALTON = 1.66054e-27
MW_VELOCITY_UNITS_PER_METER_PER_SECOND = 1e-6

# Define the elements
epsilon = 0.1   # eV
sigma = 0.07    # nm
mass = 39.95    # g/mol (amu, Dalton)

# dimensions of container
height = 5.0      # nm
width  = 5.0      # nm

# initial temperature 
T = 300.0        # K

# Organize particles into "hot" grid of nx x ny particles
# and an equally-sized "cold" grid
nx = 7
ny = 7

# Boltzmann constant
kB = 8.6173423e-5   # eV/K

# Lennard-Jones potential for squared pairwise separation rsq
def lj(rsq, epsilon = epsilon, sigma = sigma):
  alpha = 4 * epsilon * sigma ** 12
  beta  = 4 * epsilon * sigma ** 6
  return alpha * rsq ** -6 - beta * rsq ** -3


# x, y grid position of atom i (0 <= i < N/2)
def grid_pos(i):   
  return (i % nx, i / nx)


# total energy if nx * ny particles are arranged in a rectangular grid with cell length r
def pe(l):
  # calculate pe from LJ formula
  pe = 0
  n = nx * ny

  for i in range(0, n-1):
    for j in range(i+1, n):
      (xi, yi) = grid_pos(i)
      (xj, yj) = grid_pos(j)
      rsq = l * l * (abs(xi-xj) ** 2 + abs(yi-yj) ** 2)
      pe += lj(rsq)

  return pe


def generate_cold_atoms(initial_pe):

  f = lambda r: pe(r) - initial_pe
  [r] = fsolve(f, sigma)

  print "\nTarget initial PE of cold atoms = {:.4f}. At r = {:.4f} nm, PE = {:.4f} eV\n".format(initial_pe, r, pe(r))

  X = []
  Y = []

  for i in range(0, nx):
    for j in range(0, ny):
      X.append(r * (i+1))
      Y.append(r * (j+1))

  VX = [0.] * (nx*ny)
  VY = [0.] * (nx*ny)

  return (X, Y, VX, VY)


def generate_hot_atoms(ke):

  X = []
  Y = []
  VX = []
  VY = []

  ke = ke * JOULES_PER_EV
  ke_per_atom = ke / (nx * ny)

  m = mass * KILOGRAMS_PER_DALTON
  v = math.sqrt(2 * ke_per_atom / m)
  v = v * MW_VELOCITY_UNITS_PER_METER_PER_SECOND

  rx = width / (nx + 1)
  ry = height/2 / (ny + 1)

  for i in range(0, nx):
    for j in range(0, ny):
      angle = np.random.uniform() * math.pi

      X.append(rx * (i+1))
      Y.append(height/2 + ry * (j+1))
      VX.append(v * math.sin(angle))
      VY.append(v * math.cos(angle))

  return (X, Y, VX, VY)


def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
        pass
    else: raise


def generate_mw_files(num, X, Y, VX, VY):
  
  mkdir_p('classic')
  renderer = pystache.Renderer()

  cml = renderer.render_path('model.cml.mustache', { 'model_number': num })
  f = open('classic/model{}.cml'.format(num), 'w')
  f.write(cml)
  f.close()

  atoms = [{
    'rx': 100*x, 
    'ry': 100*y, 
    'vx': 100*vx, 
    'vy': 100*vy
    } for (x, y, vx, vy) in zip(X, Y, VX, VY)]

  mml = renderer.render_path('model$0.mml.mustache', {
    'number_of_particles': len(atoms),
    'epsilon': epsilon,
    'sigma':   100 * sigma,
    'mass':    mass / 120,
    'width':   width * 100,
    'height':  height * 100,
    'atoms':   atoms
  })
  f = open('classic/model{}$0.mml'.format(num), 'w')
  f.write(mml)
  f.close()

def convert_mml_file(num):
  subprocess.call(['./convert.coffee', 'classic/model{}$0.mml'.format(num), 'nextgen/model{}.json'.format(num)])

# Choose an initial energy so the final temperature is some reasonable number.
# Note the equilibrium temperature will settle above T because the equilibrium
# value of the potential energy will be less that zero.
te = 2 * nx * ny * kB * T     # eV

print "target energy = {:.4f} eV\n".format(te)

f = open('index.txt', 'w')
f.write("number of particles = {}\n".format(nx*ny*2))
f.write("total energy = {:.4f}\n\n".format(te))
f.write("model #\tinitial KE\n")

model_num = 1
for ke_to_pe_ratio in np.logspace(-2, 2, 5, base=3):
  ke_fraction = ke_to_pe_ratio / (ke_to_pe_ratio + 1)

  (coldX, coldY, coldVX, coldVY) = generate_cold_atoms(te - ke_fraction*te)
  (hotX, hotY, hotVX, hotVY)     = generate_hot_atoms(ke_fraction * te)
  
  generate_mw_files(model_num, coldX + hotX, coldY + hotY, coldVX + hotVX, coldVY + hotVY)
  convert_mml_file(model_num)
  f.write("{}\t{:.4f}\n".format(model_num, ke_fraction*te))
  model_num += 1

# also generate a model with 100% KE. Handle this as a special case
(X, Y, VX, VY) = generate_hot_atoms(te/2)   # will add 2 sets of 'hot' atoms together
topY = map(lambda y: y - height/2, Y)
generate_mw_files(model_num, X + X, Y + topY, VX + VX, VY + VY)
convert_mml_file(model_num)
f.write("{}\t{:.4f}\n".format(model_num, te))
model_num += 1
