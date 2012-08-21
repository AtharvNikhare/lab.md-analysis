import csv

#to read data from a csv file
def read_data(file_name):
	"""returns data from file as a dictionary where the keys are the first value in whichever row of the csv file"""
	dataReader = csv.reader(open(file_name, 'rb'), delimiter=' ')
	data = {}
	for row in dataReader:
		data[row[0]] = row[1:-1]
	new_data = {}

	#converts the vaues to floats
	for i in range(len(data.values())):
		vals = []
		for j in data.values()[i]:
			vals.append(float(j))
		new_data[data.keys()[i]] = vals

	return(new_data)
