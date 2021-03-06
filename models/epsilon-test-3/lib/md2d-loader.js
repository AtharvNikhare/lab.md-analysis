md2d = require('../../../../src/md-engine/md2d'),

// Adapted from modeler.js in lab project. Refactoring opportunity!
createNewCoreModel = function(width, height, elements, config) {
  var coreModel, elemsArray, element, i, ii;

  // get a fresh model
  coreModel = md2d.makeModel();
  coreModel.setSize([width,height]);

  // convert from easily-readble json format to simplified array format
  // FIXME obviously would be good to have a helper method do this 
  // here & in modeler.js
  elemsArray = [];
  for (i=0, ii=elements.length; i<ii; i++){
    element = elements[i];
    elemsArray[element.id] = [element.mass, element.epsilon, element.sigma];
  }

  coreModel.setElements(elemsArray);
  coreModel.createAtoms({ num: config.X.length });

  coreModel.useLennardJonesInteraction(true);
  coreModel.useCoulombInteraction(false);
  coreModel.useThermostat(false);

  // coreModel.setTargetTemperature(T);

  coreModel.initializeAtomsFromProperties(config);

  return coreModel;
};


exports.fromHash = function(hash) {
  var atoms    = hash.atoms,
      elements = hash.elements,
      width    = hash.width,
      height   = hash.height;

  return createNewCoreModel(width, height, elements, atoms);
};
