

from __future__ import with_statement

import sys, time, random, struct, threading
from math import pi
from datetime import datetime
import Queue
import numpy
from gnuradio import gr
import pmt
from gnuradio.digital import packet_utils
import gnuradio.digital as gr_digital
import fhmanet


class fh_msg_tester(gr.basic_block):
	"""
	docstring for block fh_msg_tester
	"""
	def __init__(self, center_freq, period_ms, sequence_length=86400):
		gr.basic_block.__init__(self, name="fh_msg_tester", in_sig=None, out_sig=None)     

		self.lock = threading.RLock()
		self.debug_stderr = False
        
		self.center_freq = center_freq
		self.period_ms = period_ms
		self.sequence_length = sequence_length
		self.hop_seq = []
		self.hopset_loaded = 'FALSE'
		
		self.message_port_register_out(pmt.intern('rx_freq_out'))
		self.message_port_register_out(pmt.intern('tx_freq_out'))
		self.message_port_register_in(pmt.intern('ctrl_in'))
		self.set_msg_handler(pmt.intern('ctrl_in'), self.ctrl_rx)

	def tx_hopset_import(self, hop_seq):
		#frequency values for signal source
		hop_seq = numpy.genfromtxt('channel_sequence.csv', dtype='float64', delimiter=',')
		return hop_seq
				
	def get_hop_freq_msg(self):
		if self.hopset_loaded == 'FALSE':
			self.hop_seq = self.tx_hopset_import(self.hop_seq)
			self.hopset_loaded = 'TRUE'
		
		d_time_ms = (datetime.now().minute * 60000) + (datetime.now().second * 1000) + (datetime.now().microsecond / 1000)
		d_current_hop = (d_time_ms / self.period_ms ) % self.sequence_length
		d_current_tx_freq = self.hop_seq[d_current_hop]
		fxff_freq = d_current_tx_freq + self.center_freq
		#fh_freq_msg = pmt.cons(pmt.intern("freq"), pmt.from_double(d_current_freq))
		fh_tx_msg = pmt.from_double(d_current_tx_freq)
		fh_rx_msg = pmt.from_double(fxff_freq)
		self.message_port_pub(pmt.intern('tx_freq_out'),fh_tx_msg)
		self.message_port_pub(pmt.intern('rx_freq_out'),fh_rx_msg)

	def ctrl_rx(self,msg):
		with self.lock:
			self.get_hop_freq_msg()

