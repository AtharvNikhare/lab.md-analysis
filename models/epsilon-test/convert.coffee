#!/usr/bin/env coffee

parseMML = require '../../../src/mw-helpers/mml-parser'
fs       = require 'fs'
mkdirp   = require 'mkdirp'

inFile = process.argv[2]
outFile = process.argv[3]

mml = fs.readFileSync(inFile).toString()
conversion = parseMML.parseMML(mml)

if conversion.json
  mkdirp.sync 'nextgen'
  fs.writeFileSync outFile, conversion.json
else
  console.error "Error converting file #{inFile}:\n#{conversion.error}"
  process.exit(1)
