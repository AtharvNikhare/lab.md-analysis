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

# Boltzmann constant
kB = 8.6173423e-5   # eV/K

# Lennard-Jones potential for squared pairwise separation rsq
def lj(rsq, epsilon = epsilon, sigma = sigma):
  alpha = 4 * epsilon * sigma ** 12
  beta  = 4 * epsilon * sigma ** 6
  return alpha * rsq ** -6 - beta * rsq ** -3

# Organize particles into grid of nx x ny particles
nx = 10
ny = 10
N = nx * ny

# x, y grid position of atom i (0 <= i < N)
def grid_pos(i):   
  return (i % nx, i / nx)

# total energy if nx * ny particles are arranged in a rectangular grid with cell length r
def pe(l):
  # calculate pe from LJ formula
  pe = 0

  for i in range(0, N-1):
    for j in range(i+1, N):
      (xi, yi) = grid_pos(i)
      (xj, yj) = grid_pos(j)
      rsq = l * l * (abs(xi-xj) ** 2 + abs(yi-yj) ** 2)
      pe += lj(rsq)

  return pe


def separation(initial_pe):
  f = lambda r: pe(r) - initial_pe
  [r] = fsolve(f, sigma)
  return r

  # print "\nTarget initial PE of cold atoms = {:.4f}. At r = {:.6f} nm, PE = {:.4f} eV\n".format(initial_pe, r, pe(r))


def positions(r):

  X = []
  Y = []

  leftx = (width  - r * (nx - 1)) / 2
  topy  = (height - r * (ny - 1)) / 2

  for i in range(0, nx):
    for j in range(0, ny):
      X.append(leftx + r * (i+1))
      Y.append(topy  + r * (j+1))

  return (X, Y)


def velocities(initial_ke_in_ev):

  VX = []
  VY = []

  ke_per_atom_in_joules = initial_ke_in_ev * JOULES_PER_EV / N

  mass_in_kg = mass * KILOGRAMS_PER_DALTON
  v_per_atom_in_mks = math.sqrt(2 * ke_per_atom_in_joules / mass_in_kg)
  v = v_per_atom_in_mks * MW_VELOCITY_UNITS_PER_METER_PER_SECOND

  for i in range(0, nx):
    for j in range(0, ny):
      angle = np.random.uniform() * math.pi

      VX.append(v * math.sin(angle))
      VY.append(v * math.cos(angle))

  return (VX, VY)


def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
        pass
    else: raise


def generate_mw_files(num, X, Y, VX, VY):
  
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
  subprocess.call([
    './convert.coffee', 
    'classic/model{}$0.mml'.format(num), 
    'nextgen/model{}.json'.format(num),
    'revised-epsilon-test-model{}'.format(num)
  ])

if __name__ == "__main__":

  mkdir_p('classic')
  mkdir_p('nextgen')

  # Choose an initial energy so the final temperature is some reasonable number.
  # Note the equilibrium temperature will settle above T because the equilibrium
  # value of the potential energy will be less that zero.
  te = N * kB * T     # eV

  print "target energy = {:.4f} eV\n".format(te)

  f = open('index.txt', 'w')
  f.write("number of particles = {}\n".format(N))
  f.write("total energy = {:.4f}\n\n".format(te))
  f.write("model #\tinitial KE\n")

  model_num = 1

  print "#\tsep (nm)\tPE (eV)\tKE (eV)\tTE (eV)"

  for ke in np.linspace(0, te, 5):

    r = separation(te - ke)
    calculated_pe = pe(r)

    print "{}\t{:.6f}\t{:.4f}\t{:.4f}\t{:.4f}".format(model_num, r, calculated_pe, ke, ke + calculated_pe)

    (X, Y) = positions(r)
    (VX, VY) = velocities(ke)

    generate_mw_files(model_num, X, Y, VX, VY)
    convert_mml_file(model_num)
    f.write("{}\t{:.4f}\n".format(model_num, ke))
    model_num += 1
