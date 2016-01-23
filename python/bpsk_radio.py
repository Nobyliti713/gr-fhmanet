# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: BPSK FHSS Modem
# Author: Jason Noble
# Description: Modem based on J. Malbury's GMSK Modem from gr-mac and Aaron Scher's BPSK Mod/Demod flowgraph
# Generated: Sat Jan 23 21:13:47 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
import mac
import pmt


class bpsk_radio(gr.hier_block2):

    def __init__(self, access_code_threshold=0, filename="input.bin"):
        gr.hier_block2.__init__(
            self, "BPSK FHSS Modem",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )
        self.message_port_register_hier_in("freq_in")
        self.message_port_register_hier_in("msg_in")
        self.message_port_register_hier_out("msg_out")

        ##################################################
        # Parameters
        ##################################################
        self.access_code_threshold = access_code_threshold
        self.filename = filename

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1e5
        self.nfilts = nfilts = 32
        self.excess_bw = excess_bw = 0.35
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 5*sps*nfilts)
        self.resample_rate = resample_rate = 30
        self.freq_offset = freq_offset = 0
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, 22000, 8000, firdes.WIN_BLACKMAN_HARRIS, 6.76)
        self.center_freq = center_freq = 0
        self.BPSK = BPSK = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()

        ##################################################
        # Message Queues
        ##################################################
        mac_packet_deframer_0_msgq_out = mac_packet_to_pdu_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=resample_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=resample_rate,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.mac_packet_to_pdu_0 = mac.packet_to_pdu(msgq=mac_packet_to_pdu_0_msgq_in, dewhiten=True, output_invalid=False)
        self.mac_packet_framer_0 = mac.packet_framer(
            access_code="",
        	whitener_offset=0,
        	rotate_whitener_offset=0,
        	whiten=True,
        	preamble=''.join(['\x55']*((256*1)/8/sps)),
        	postamble=''.join(['\x00']*(16/8/sps)*0),
        )
        self.mac_packet_deframer_0 = mac.packet_deframer(msgq=mac_packet_deframer_0_msgq_out, access_code="", threshold=access_code_threshold)
        self.mac_burst_tagger_0 = mac.burst_tagger('length', sps*8, 32*0+ 0, 16*0 + 16)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (firdes_tap), center_freq, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (1, ), 1e5, samp_rate)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes_tap), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, .063, (rrc_taps), nfilts, nfilts/2, 1.5, 1)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(3.14/100, 2, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=BPSK,
          differential=False,
          samples_per_symbol=sps,
          pre_diff_code=True,
          excess_bw=excess_bw,
          verbose=False,
          log=False,
          )
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "length")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blks2_selector_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1e5, 1, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.mac_packet_framer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.mac_packet_to_pdu_0, 'pdu'), (self, 'msg_out'))    
        self.msg_connect((self, 'freq_in'), (self.analog_sig_source_x_0, 'freq'))    
        self.msg_connect((self, 'freq_in'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))    
        self.msg_connect((self, 'msg_in'), (self.mac_packet_framer_0, 'in'))    
        self.connect((self.analog_agc_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.analog_agc_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blks2_selector_1, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blks2_selector_1, 0))    
        self.connect((self.blks2_selector_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.blks2_selector_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.mac_burst_tagger_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_constellation_modulator_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.mac_packet_deframer_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blks2_selector_0, 0))    
        self.connect((self.mac_burst_tagger_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_agc_xx_0, 0))    

    def get_access_code_threshold(self):
        return self.access_code_threshold

    def set_access_code_threshold(self, access_code_threshold):
        self.access_code_threshold = access_code_threshold

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 5*self.sps*self.nfilts))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_tap(firdes.low_pass(1, self.samp_rate, 22000, 8000, firdes.WIN_BLACKMAN_HARRIS, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 5*self.sps*self.nfilts))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 5*self.sps*self.nfilts))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.set_taps((self.rrc_taps))

    def get_resample_rate(self):
        return self.resample_rate

    def set_resample_rate(self, resample_rate):
        self.resample_rate = resample_rate

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap
        self.fft_filter_xxx_0.set_taps((self.firdes_tap))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.firdes_tap))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.analog_sig_source_x_0_0.set_frequency(self.center_freq)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.center_freq)

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK
