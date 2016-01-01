##################################################
# GNU Radio Python Flow Graph
# Title: DPSK FHSS Modem
# Author: Jason Noble
# Description: DPSK Modem based on J. Malbury's GMSK Modem from gr-mac
# Generated: Thu Dec 31 15:49:28 2015
##################################################

from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
import mac
import pmt


class dpsk_radio(gr.hier_block2):

    def __init__(self, access_code_threshold=0, ampl=0.7, rate=1e6, samps_per_sym=4):
        gr.hier_block2.__init__(
            self, "DPSK FHSS Modem",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )
        self.message_port_register_hier_out("freq_in")
        self.message_port_register_hier_out("msg_in")
        self.message_port_register_hier_in("msg_out")

        ##################################################
        # Parameters
        ##################################################
        self.access_code_threshold = access_code_threshold
        self.ampl = ampl
        self.rate = rate
        self.samps_per_sym = samps_per_sym

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = rate
        self.nfilts = nfilts = 32
        self.eb = eb = 0.35
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(samps_per_sym), eb, 5*samps_per_sym*nfilts)
        self.rnd_sync_listen_channel = rnd_sync_listen_channel = 0
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, 2000, 25000, firdes.WIN_HAMMING, 6.76)
        self.excess_bw = excess_bw = 0.35

        ##################################################
        # Message Queues
        ##################################################
        mac_packet_deframer_0_msgq_out = mac_packet_to_pdu_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        self.mac_packet_to_pdu_0 = mac.packet_to_pdu(msgq=mac_packet_to_pdu_0_msgq_in, dewhiten=True, output_invalid=False)
        self.mac_packet_framer_0 = mac.packet_framer(
            access_code="",
        	whitener_offset=0,
        	rotate_whitener_offset=0,
        	whiten=True,
        	preamble=''.join(['\x55']*((256*1)/8/samps_per_sym)),
        	postamble=''.join(['\x00']*(16/8/samps_per_sym)*0),
        )
        self.mac_packet_deframer_0 = mac.packet_deframer(msgq=mac_packet_deframer_0_msgq_out, access_code="", threshold=access_code_threshold)
        self.mac_burst_tagger_0 = mac.burst_tagger('length', samps_per_sym*8, 32*0+ 0, 16*0 + 16)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes_tap), 0, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes_tap), rnd_sync_listen_channel, samp_rate)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
          constellation_points=2,
          mod_code="gray",
          differential=True,
          samples_per_symbol=samps_per_sym,
          excess_bw=excess_bw,
          verbose=False,
          log=False,
          )
        self.digital_psk_demod_0 = digital.psk.psk_demod(
          constellation_points=2,
          differential=True,
          samples_per_symbol=samps_per_sym,
          excess_bw=excess_bw,
          phase_bw=6.28/100.0,
          timing_bw=6.28/100.0,
          mod_code="gray",
          verbose=False,
          log=False,
          )
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samps_per_sym, 2*3.14/100.0, (rrc_taps), nfilts, 0, 0.5, 1)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(1*3.14/50.0, 2, False)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "length")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((ampl, ))
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.mac_packet_framer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.mac_packet_to_pdu_0, 'pdu'), (self, 'msg_out'))    
        self.msg_connect((self, 'freq_in'), (self.freq_xlating_fir_filter_xxx_0_0, 'freq'))    
        self.msg_connect((self, 'msg_in'), (self.mac_packet_framer_0, 'in'))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blks2_selector_0, 0), (self.digital_psk_demod_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.mac_burst_tagger_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_psk_mod_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.digital_psk_demod_0, 0), (self.mac_packet_deframer_0, 0))    
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self.mac_burst_tagger_0, 0), (self, 0))    
        self.connect((self, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    


    def get_access_code_threshold(self):
        return self.access_code_threshold

    def set_access_code_threshold(self, access_code_threshold):
        self.access_code_threshold = access_code_threshold

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.blocks_multiply_const_vxx_0.set_k((self.ampl, ))

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.set_samp_rate(self.rate)

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samps_per_sym), self.eb, 5*self.samps_per_sym*self.nfilts))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, 2000, 25000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samps_per_sym), self.eb, 5*self.samps_per_sym*self.nfilts))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samps_per_sym), self.eb, 5*self.samps_per_sym*self.nfilts))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.set_taps((self.rrc_taps))

    def get_rnd_sync_listen_channel(self):
        return self.rnd_sync_listen_channel

    def set_rnd_sync_listen_channel(self, rnd_sync_listen_channel):
        self.rnd_sync_listen_channel = rnd_sync_listen_channel
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.rnd_sync_listen_channel)

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.firdes_tap))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.firdes_tap))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

