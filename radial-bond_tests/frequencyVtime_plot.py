from pylab import plot, show, title, xlabel, ylabel, subplot, legend,subplots_adjust,pi,fft,arange,savefig,close
class timeVSfreq_plot():
	def __init__(self,next_gen_data,classic_data,title):
		self.sample_rate = 10.0;  # sampling rate per pico second
		self.next_time = next_gen_data['time']
		self.classic_time = classic_data['time']
		del next_gen_data['time']
		del classic_data['time']

		self.time_plot('time domain',next_gen_data,classic_data)
		self.freq_plot(next_gen_data,classic_data)
		self.output_plots(title,False)

	def plotSpectrum(self,data,color,label):
		data_length = len(data) # length of the signal
		data_len_array = arange(data_length)
		time = data_length/self.sample_rate
		frq = data_len_array/time # two sides frequency range
		frq = frq[range(data_length/2)] # one side frequency range
		dataFreq = fft(data)/data_length # compute the forier transform and normalize the data
		dataFreq = dataFreq[range(data_length/2)]
		plot(frq[1:-1],abs(dataFreq)[1:-1],color = color,label = label) # plots the forier transform
		xlabel('Freq (THz)')
		ylabel('energy in the waves(eV)')

	def graph(self,time,data,color,label):
		plot(time,data,color = color,label = label)
		xlabel('Time (ps)')
		ylabel('energy (eV)')

	#top plot
	def time_plot(self,name,next_gen_data,classic_data):
		subplot(2,1,1)
		title(name)
		if next_gen_data.values() !=[]:
			plot(0,next_gen_data.values()[0][1],'white',label = 'next gen')
			for i in range(len(next_gen_data.keys())):
				if i==0: color = 'red' 
				if i==1: color = 'orange'
				if i==2: color = 'green'
				self.graph(self.next_time,next_gen_data.values()[i],color,next_gen_data.keys()[i])
		if classic_data.values() != []:
			plot(0,classic_data.values()[0][1],'white',label = 'Legacy')
			for i in range(len(classic_data.keys())):
				if i==0: color = 'blue' 
				if i==1: color = 'purple'
				if i==2: color = 'teal'
				self.graph(self.classic_time,classic_data.values()[i],color,classic_data.keys()[i])
		legend(bbox_to_anchor=(1.004,0), loc=3,borderaxespad=0.)

	#bottom plot
	def freq_plot(self,next_gen_data,classic_data):
		subplot(2,1,2)
		title('frequency analysis')
		if next_gen_data.values() !=[]:
			plot(0,0,'white',label = 'next gen')
			for i in range(len(next_gen_data.keys())):
				if i==0: color = 'red' 
				if i==1: color = 'orange'
				if i==2: color = 'green'

				self.plotSpectrum(next_gen_data.values()[i] ,color, next_gen_data.keys()[i])

		if classic_data.values() != []:
			plot(0,0,'white',label = 'Legacy')
			for i in range(len(classic_data.keys())):
				if i==0: color = 'blue' 
				if i==1: color = 'purple'
				if i==2: color = 'teal'
				self.plotSpectrum(classic_data.values()[i],color,classic_data.keys()[i])

		legend(bbox_to_anchor=(1.004,0), loc=3,borderaxespad=0.)

	def output_plots(self,save,display):
		#adjust the plots for optimal display
		subplots_adjust(right = .78, hspace = .35)
		print(save)
		if bool(save) == True:
			savefig('figures/'+save+'.png',dpi = 300,facecolor = '.75',pad_inches = 2)

		if display == True:
			show()
		close()