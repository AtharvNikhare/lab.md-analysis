this folder contains various radial bond tests. Data was manualy collected from both Next Gen MW and Legacy MW from different test circumstances and graphed on both the time and frequency domain. each image(in figures folder) shows two plots. the top plot is the time energy data for both Legacy MW and next gen MW. It displays the total energy (te) potential energy (pe) and the kinetic energy (ke). 
to collect data from java MW open the desired model options->toolbox->view time series of energy click on the icon furthest to the left,double click whichever data you would like to see the full table of.
to manualy collect data from the javascript MW begin with opening the web console and typing model.tick(99) wait for it to proceed and then type controller.energy[x] where x is one two or three for ke pe or te (this only works when operating a model using the complex model controller)