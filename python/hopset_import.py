
#http://stackoverflow.com/questions/3518778/how-to-read-csv-into-record-array-in-numpy

from numpy import genfromtxt
from datetime import datetime
py_hop_seq = genfromtxt('../apps/hop_sequence.csv', delimiter=',')
#d_period_ms
#d_sequence_length

def get_hop_freq(d_period_ms, d_sequence_length):

	d_time_ms = (datetime.now().minute * 60000) + (datetime.now().second * 1000) + (datetime.now().microsecond / 1000)
	d_current_hop = (d_time_ms / d_period_ms ) % d_sequence_length
	d_current_freq = py_hop_seq[d_current_hop]
	
#hopset_import.d_current_hop
