# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: BPSK FHSS Modem V3
# Author: Jason Noble
# Description: Modem based on J. Malbury's GMSK Modem from gr-mac and Aaron Scher's BPSK Mod/Demod flowgraph
# Generated: Tue Feb  9 08:07:49 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes


class bpsk_radio(gr.hier_block2):

    def __init__(self, access_code_threshold=0, hw_sample_rate=1e7, resample_rate=100, sps=8):
        gr.hier_block2.__init__(
            self, "BPSK FHSS Modem V3",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )
        self.message_port_register_hier_in("tx_freq_in")
        self.message_port_register_hier_in("rx_freq_in")
        self.message_port_register_hier_in("msg_in")
        self.message_port_register_hier_out("msg_out")

        ##################################################
        # Parameters
        ##################################################
        self.access_code_threshold = access_code_threshold
        self.hw_sample_rate = hw_sample_rate
        self.resample_rate = resample_rate
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.nfilts = nfilts = 32
        self.excess_bw = excess_bw = 0.35
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 5*sps*nfilts)
        self.header_specs = header_specs = digital.packet_header_default(5,"packet_len","packet_num",8)
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, 22000, 8000, firdes.WIN_BLACKMAN_HARRIS, 6.76)
        self.BPSK = BPSK = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 4, 1).base()

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
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (1, ), 1e5, samp_rate)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes_tap), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, .063, (rrc_taps), nfilts, nfilts/2, 1.5, 1)
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_specs)
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_specs, "pkt_len")
        self.digital_header_payload_demux_0_0 = digital.header_payload_demux(
        	  5,
        	  1,
        	  0,
        	  "packet_len",
        	  "packet_len",
        	  False,
        	  gr.sizeof_char,
        	  "rx_time",
                  samp_rate,
                  (),
            )
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(True)
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
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, "pkt_len", 0)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "pkt_len")
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "output.bin", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))    
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self, 'msg_out'))    
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0_0, 'header_data'))    
        self.msg_connect((self, 'tx_freq_in'), (self.analog_sig_source_x_0, 'freq'))    
        self.msg_connect((self, 'rx_freq_in'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))    
        self.msg_connect((self, 'msg_in'), (self.digital_crc32_async_bb_1, 'in'))    
        self.connect((self.analog_agc_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 1))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_packet_headergenerator_bb_0, 0))    
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_constellation_modulator_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_header_payload_demux_0_0, 0))    
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_header_payload_demux_0_0, 1), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.digital_header_payload_demux_0_0, 0), (self.digital_packet_headerparser_b_0, 0))    
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_agc_xx_0, 0))    

    def get_access_code_threshold(self):
        return self.access_code_threshold

    def set_access_code_threshold(self, access_code_threshold):
        self.access_code_threshold = access_code_threshold

    def get_hw_sample_rate(self):
        return self.hw_sample_rate

    def set_hw_sample_rate(self, hw_sample_rate):
        self.hw_sample_rate = hw_sample_rate

    def get_resample_rate(self):
        return self.resample_rate

    def set_resample_rate(self, resample_rate):
        self.resample_rate = resample_rate

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

    def get_header_specs(self):
        return self.header_specs

    def set_header_specs(self, header_specs):
        self.header_specs = header_specs
        self.digital_packet_headergenerator_bb_0.set_header_formatter(self.header_specs)

    def get_firdes_tap(self):
        return self.firdes_tap

    def set_firdes_tap(self, firdes_tap):
        self.firdes_tap = firdes_tap
        self.fft_filter_xxx_0.set_taps((self.firdes_tap))

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK
