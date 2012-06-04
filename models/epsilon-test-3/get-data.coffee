#!/usr/bin/env coffee

potentials = require '../../../src/md-engine/potentials'
md2dLoader = require './lib/md2d-loader'
fs         = require 'fs'

totalTime = 100000

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

index = fs.readFileSync('index.txt').toString().split('\n')
for line in index[1..index.length]
  continue unless line
  [modelNum, epsilon, initialKE, finalKE] = line.split('\t')
  runModel "nextgen/model#{modelNum}.json", "nextgen/model#{modelNum}.data.txt"
