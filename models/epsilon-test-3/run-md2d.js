#!/usr/bin/env node

md2dLoader = require('./lib/md2d-loader');
fs         = require('fs');

inFile  = process.argv[2];
if (typeof inFile === 'undefined') {
  console.log();
  console.log("    usage: run-md2d.js filename [duration]");
  console.log(); 
  console.log("    filename should point to a Lab json model definition");
  console.log("    duration is a length of time in fs (default 1000)");
  console.log();  
  console.log("    tab-separated output format is:");
  console.log();
  console.log("    time (fs)\tKE (eV)\tTE (eV)");
  console.log();  
  process.exit(1);
}

totalTime = parseInt(process.argv[3], 10);
if (typeof totalTime !== 'number' || isNaN(totalTime)) {
  totalTime = 1000;
}

modelHash = JSON.parse(fs.readFileSync(inFile).toString());

md2dModel = md2dLoader.fromHash(modelHash);

md2dModel.setTime(0);
state = md2dModel.outputState;

while (state.time <= totalTime) {
  console.log(state.time + "\t" + state.KE + "\t" + (state.KE + state.PE));
  md2dModel.integrate();  
}
