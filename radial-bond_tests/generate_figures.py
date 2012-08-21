import data_reader
from frequencyVtime_plot import *

next_gen_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/next_gen/same_ellement/data.csv')
classic_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/classic/same_ellement/data.csv')
del classic_data['te']
del next_gen_data['te']
del classic_data['pe']
del next_gen_data['pe']
test = timeVSfreq_plot(next_gen_data,classic_data,'same_ellement_(no_te)')

next_gen_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/next_gen/same_ellement/data.csv')
classic_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/classic/same_ellement/data.csv')
del classic_data['ke']
del next_gen_data['ke']
del classic_data['pe']
del next_gen_data['pe']
test = timeVSfreq_plot(next_gen_data,classic_data,'same_ellement_(only_te)')

next_gen_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/next_gen/different_ellements/data.csv')
classic_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/classic/different_ellements/data.csv')
del classic_data['te']
del next_gen_data['te']
del classic_data['pe']
del next_gen_data['pe']
test = timeVSfreq_plot(next_gen_data,classic_data,'different_ellements_(no_te)')

next_gen_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/next_gen/different_ellements/data.csv')
classic_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/classic/different_ellements/data.csv')
del classic_data['ke']
del next_gen_data['ke']
del classic_data['pe']
del next_gen_data['pe']
del next_gen_data['te']
test = timeVSfreq_plot(next_gen_data,classic_data,'different_ellements_(classic_te)')

next_gen_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/next_gen/different_ellements/data.csv')
classic_data = data_reader.read_data('/home/jackson/lab/lab.md-analysis/radial-bond_tests/data/classic/different_ellements/data.csv')
del classic_data['ke']
del next_gen_data['ke']
del classic_data['pe']
del next_gen_data['pe']
del classic_data['te']
test = timeVSfreq_plot(next_gen_data,classic_data,'different_ellements_(next_gen_te)')