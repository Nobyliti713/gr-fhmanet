
#http://stackoverflow.com/questions/3518778/how-to-read-csv-into-record-array-in-numpy

from numpy import genfromtxt
from datetime import datetime
import pmt
py_hop_seq = genfromtxt('../apps/hop_sequence.csv', dtype='float64', delimiter=',')

def get_hop_freq_msg(d_period_ms, d_sequence_length):

	d_time_ms = (datetime.now().minute * 60000) + (datetime.now().second * 1000) + (datetime.now().microsecond / 1000)
	d_current_hop = (d_time_ms / d_period_ms ) % d_sequence_length
	d_current_freq = py_hop_seq[d_current_hop]
	d_freq_pmt = pmt.to_pmt(d_current_freq)#pmt.cons(pmt.intern("freq"), pmt.from_double(d_current_freq))
	return d_freq_pmt
