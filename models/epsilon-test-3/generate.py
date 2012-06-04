#!/usr/bin/env python

import math
import numpy as np

import pystache
import os
import errno
import subprocess

# some conversion constants for later
JOULES_PER_EV = 1.6021770000000003e-19
KILOGRAMS_PER_DALTON = 1.66054e-27
MW_VELOCITY_UNITS_PER_METER_PER_SECOND = 1e-6

# x, y grid position of atom i (0 <= i < nx*ny)
SQRT_3_OVER_2 = math.sqrt(3)/2

# Boltzmann constant
kB = 8.6173423e-5   # eV/K

# Define the elements
sigma = 0.07    # nm
mass = 39.95    # g/mol (amu, Dalton)

# dimensions of container
height = 5.0      # nm
width  = 5.0      # nm

# Organize particles into grid of nx x ny particles
nx = 7
ny = 7
N = 2 * nx * ny


def lj(rsq, epsilon, sigma = sigma):
  """
  Lennard-Jones potential for squared pairwise separation = rsq
  """
  alpha = 4 * epsilon * sigma ** 12
  beta  = 4 * epsilon * sigma ** 6
  return alpha * rsq ** -6 - beta * rsq ** -3


def grid_pos(i):
  """
  Location on the unit-length hexagonal lattice of the ith particle
  """

  x = i % nx
  y = i / nx

  if y % 2 == 0:
    x += 0.5
  y *= SQRT_3_OVER_2

  return (x, y)


def pe(r, epsilon):
  """
  potential energy of nx * ny particles arranged in a hexagonal lattice
  with interparticle distance r
  """
  # calculate pe from LJ formula
  pe = 0

  n = nx * ny
  for i in range(0, n - 1):
    for j in range(i+1, n):
      (xi, yi) = grid_pos(i)
      (xj, yj) = grid_pos(j)
      rsq = r * r * (abs(xi-xj) ** 2 + abs(yi-yj) ** 2)
      pe += lj(rsq, epsilon)

  return pe


def positions(r):
  """ 
  returns (X,Y) vectors for nx*ny particles arranged in a hexagonal lattice
  with separation r
  """

  X = []
  Y = []

  leftx = -r*(nx - 1) / 2
  topy  = -SQRT_3_OVER_2 * r * (ny - 1) / 2

  for i in range(0, nx*ny):
    (x, y) = grid_pos(i)
    X.append(leftx + r*x)
    Y.append(topy + r*y)

  return (X, Y)


def velocities(initial_ke_in_ev, n, angle):
  """
  VX, VY angles for n particles which should have total KE, in Joules,
  'initial_ke_in_ev'. All particles will translate in direction 'angle'
  """
  VX = []
  VY = []

  ke_per_atom_in_joules = initial_ke_in_ev * JOULES_PER_EV / n

  mass_in_kg = mass * KILOGRAMS_PER_DALTON
  v_per_atom_in_mks = math.sqrt(2 * ke_per_atom_in_joules / mass_in_kg)
  v = v_per_atom_in_mks * MW_VELOCITY_UNITS_PER_METER_PER_SECOND

  for i in range(0, n):
    VX.append(v * math.cos(angle))
    VY.append(v * math.sin(angle))

  return (VX, VY)


def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST:
        pass
    else: raise


def generate_mw_files(num, epsilon, X, Y, VX, VY):
  
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
    'epsilon-test-3-model{}'.format(num)
  ])

if __name__ == "__main__":

  mkdir_p('classic')
  mkdir_p('nextgen') 

  model_num = 1
  rmin = 2 ** (1./6) * sigma
  
  f = open("index.txt", "w")
  f.write("model\tepsilon\tinitial KE\tapprox. final KE\n")

  for state in ('solid', 'gas'):
    for epsilon in np.linspace(0.01, 0.1, 5):
      
      if state == 'gas':
        final_ke = N * kB * 1000
        initial_pe = 2*pe(rmin, epsilon)
        initial_ke = final_ke - initial_pe
      elif state == 'solid':
        initial_ke = 0
        final_ke = 0

      f.write("{}\t{:.3f}\t{:.3f}\t{:.3f}\n".format(model_num, epsilon, initial_ke, final_ke))

      (X, Y) = positions(rmin)

      # some atoms headed down
      topX = map( lambda x: x + width/2, X )
      topY = map( lambda y: y + height/4, Y )
      (topVX, topVY) = velocities(initial_ke/2, N/2, math.pi/2)

      # and some atoms headed up
      bottomX = map( lambda x: x + width/2, X )
      bottomY = map( lambda y: y + 3 * height/4, Y )
      (bottomVX, bottomVY) = velocities(initial_ke/2, N/2, -math.pi/2)

      generate_mw_files(model_num, epsilon, topX+bottomX, topY+bottomY, topVX+bottomVX, topVY+bottomVY)
      convert_mml_file(model_num)
      model_num += 1
