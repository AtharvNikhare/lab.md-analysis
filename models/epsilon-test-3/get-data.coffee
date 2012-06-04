#!/usr/bin/env coffee

potentials = require '../../../src/md-engine/potentials'
md2dLoader = require './lib/md2d-loader'
fs         = require 'fs'

totalTime = 200000


# FIXME: LJ calculator in md-engine should be simplified so it can just be reused here
modifiedEpsilon = -0.12
sigma = 0.07

constants = require '../../../src/md-engine/constants'
unit      = constants.unit

NANOMETERS_PER_METER = constants.ratio( unit.NANOMETER, { per: unit.METER })
MW_FORCE_UNITS_PER_NEWTON = constants.ratio( unit.MW_FORCE_UNIT, { per: unit.NEWTON })

alpha_Potential = 4 * modifiedEpsilon * Math.pow(sigma, 12)
beta_Potential  = 4 * modifiedEpsilon * Math.pow(sigma, 6)
alpha_Force = 12 * constants.convert(alpha_Potential, { from: unit.EV, to: unit.JOULE }) * NANOMETERS_PER_METER * MW_FORCE_UNITS_PER_NEWTON
beta_Force =  6  * constants.convert(beta_Potential,  { from: unit.EV, to: unit.JOULE }) * NANOMETERS_PER_METER * MW_FORCE_UNITS_PER_NEWTON

modifiedForceOverDistanceFromSquaredDistance = (r_sq, el0, el1) ->
  r_minus2nd  = 1 / r_sq
  r_minus6th  = r_minus2nd * r_minus2nd * r_minus2nd
  r_minus8th  = r_minus6th * r_minus2nd
  r_minus14th = r_minus8th * r_minus6th

  alpha_Force*r_minus14th - beta_Force*r_minus8th

modifiedPotentialFromSquaredDistance = (r_sq, el0, el1) ->
  alpha_Potential*Math.pow(r_sq, -6) - beta_Potential*Math.pow(r_sq, -3)


runModel = (inFileName, outFileName, modifyModel) ->
  hash  = JSON.parse fs.readFileSync(inFileName).toString()
  model = md2dLoader.fromHash hash

  modifyModel?(model)
  state = model.outputState
  model.setTime 0

  console.log "\n\n#{inFileName}:\n\n"

  out = fs.openSync outFileName, 'w'
  while (state.time <= totalTime)
    str = "#{state.time}\t#{state.KE}\t#{state.KE + state.PE}"
    fs.writeSync out, str+"\n"
    console.log str
    model.integrate()
  fs.closeSync out


# begin script

files = ("nextgen/#{f}" for f in fs.readdirSync 'nextgen' when f.match /model[\d]+.json/)

for inFileName in files
  prefix = inFileName.match(/(model[\d+]).json$/)[1]
  runModel inFileName, "nextgen/#{prefix}.data.txt"

  runModel inFileName, "nextgen/#{prefix}-control.data.txt", (model) ->
    model.getLJCalculator().potentialFromSquaredDistance = modifiedPotentialFromSquaredDistance
    model.getLJCalculator().forceOverDistanceFromSquaredDistance = modifiedForceOverDistanceFromSquaredDistance
