#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Simple Trx Mac
# Generated: Wed Jan  6 03:40:35 2016
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from dpsk_sch_radio import dpsk_sch_radio  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import mac
import osmosdr
import pmt
import time


class simple_trx_mac(gr.top_block):

    def __init__(self, ampl=0.7, args='', arq_timeout=.1*0 + 0.04, broadcast_interval=1, dest_addr=-1, lo_offset=5e6, max_arq_attempts=5 * 2, mtu=255, port="12345", radio_addr=0, rx_antenna="TX/RX", rx_freq=915e6, rx_gain=65-20, rx_lo_offset=0, samps_per_sym=4, tx_freq=915e6, tx_gain=45, tx_lo_offset=0, rate=1e6, cen_freq=2442500000):
        gr.top_block.__init__(self, "Simple Trx Mac")

        ##################################################
        # Parameters
        ##################################################
        self.ampl = ampl
        self.args = args
        self.arq_timeout = arq_timeout
        self.broadcast_interval = broadcast_interval
        self.dest_addr = dest_addr
        self.lo_offset = lo_offset
        self.max_arq_attempts = max_arq_attempts
        self.mtu = mtu
        self.port = port
        self.radio_addr = radio_addr
        self.rx_antenna = rx_antenna
        self.rx_freq = rx_freq
        self.rx_gain = rx_gain
        self.rx_lo_offset = rx_lo_offset
        self.samps_per_sym = samps_per_sym
        self.tx_freq = tx_freq
        self.tx_gain = tx_gain
        self.tx_lo_offset = tx_lo_offset
        self.rate = rate
        self.cen_freq = cen_freq

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = rate
        self.center_freq = center_freq = cen_freq

        ##################################################
        # Blocks
        ##################################################
        self.simple_mac = mac.simple_mac(
        radio_addr,
        arq_timeout,
        max_arq_attempts,
        broadcast_interval,
        False,
        0.05,
        node_expiry_delay=10.0,
        expire_on_arq_failure=False,
        only_send_if_alive=False,
        prepend_dummy=False,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.mac_virtual_channel_encoder_0 = mac.virtual_channel_encoder(dest_addr, True,mtu=mtu,
        chan_id=0,
        prepend_dummy=False,
        )
        self.mac_virtual_channel_decoder_0 = mac.virtual_channel_decoder(3, [0,1])
        self.dpsk_sch_radio_0 = dpsk_sch_radio(
            access_code_threshold=0,
            ampl=0.7,
            rate=1e6,
            samps_per_sym=4,
        )
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", port, mtu, False)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("T"), 1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.simple_mac, 'ctrl_in'))    
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.mac_virtual_channel_encoder_0, 'in'))    
        self.msg_connect((self.dpsk_sch_radio_0, 'msg_out'), (self.simple_mac, 'from_radio'))    
        self.msg_connect((self.mac_virtual_channel_decoder_0, 'out0'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.mac_virtual_channel_encoder_0, 'out'), (self.simple_mac, 'from_app_arq'))    
        self.msg_connect((self.simple_mac, 'to_radio'), (self.dpsk_sch_radio_0, 'msg_in'))    
        self.msg_connect((self.simple_mac, 'to_app'), (self.mac_virtual_channel_decoder_0, 'in'))    
        self.connect((self.dpsk_sch_radio_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.dpsk_sch_radio_0, 0))    

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl

    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_arq_timeout(self):
        return self.arq_timeout

    def set_arq_timeout(self, arq_timeout):
        self.arq_timeout = arq_timeout

    def get_broadcast_interval(self):
        return self.broadcast_interval

    def set_broadcast_interval(self, broadcast_interval):
        self.broadcast_interval = broadcast_interval

    def get_dest_addr(self):
        return self.dest_addr

    def set_dest_addr(self, dest_addr):
        self.dest_addr = dest_addr

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset

    def get_max_arq_attempts(self):
        return self.max_arq_attempts

    def set_max_arq_attempts(self, max_arq_attempts):
        self.max_arq_attempts = max_arq_attempts

    def get_mtu(self):
        return self.mtu

    def set_mtu(self, mtu):
        self.mtu = mtu

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_radio_addr(self):
        return self.radio_addr

    def set_radio_addr(self, radio_addr):
        self.radio_addr = radio_addr

    def get_rx_antenna(self):
        return self.rx_antenna

    def set_rx_antenna(self, rx_antenna):
        self.rx_antenna = rx_antenna

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_rx_lo_offset(self):
        return self.rx_lo_offset

    def set_rx_lo_offset(self, rx_lo_offset):
        self.rx_lo_offset = rx_lo_offset

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_tx_lo_offset(self):
        return self.tx_lo_offset

    def set_tx_lo_offset(self, tx_lo_offset):
        self.tx_lo_offset = tx_lo_offset

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.set_samp_rate(self.rate)

    def get_cen_freq(self):
        return self.cen_freq

    def set_cen_freq(self, cen_freq):
        self.cen_freq = cen_freq
        self.set_center_freq(self.cen_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--ampl", dest="ampl", type="eng_float", default=eng_notation.num_to_str(0.7),
        help="Set TX BB amp [default=%default]")
    parser.add_option(
        "-a", "--args", dest="args", type="string", default='',
        help="Set USRP device args [default=%default]")
    parser.add_option(
        "-t", "--arq-timeout", dest="arq_timeout", type="eng_float", default=eng_notation.num_to_str(.1*0 + 0.04),
        help="Set ARQ timeout [default=%default]")
    parser.add_option(
        "-b", "--broadcast-interval", dest="broadcast_interval", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Broadcast Interval [default=%default]")
    parser.add_option(
        "-d", "--dest-addr", dest="dest_addr", type="intx", default=-1,
        help="Set Destination address [default=%default]")
    parser.add_option(
        "", "--lo-offset", dest="lo_offset", type="eng_float", default=eng_notation.num_to_str(5e6),
        help="Set lo_offset [default=%default]")
    parser.add_option(
        "", "--max-arq-attempts", dest="max_arq_attempts", type="intx", default=5 * 2,
        help="Set Max ARQ attempts [default=%default]")
    parser.add_option(
        "", "--mtu", dest="mtu", type="intx", default=255,
        help="Set TCP Socket MTU [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default="12345",
        help="Set TCP port [default=%default]")
    parser.add_option(
        "-l", "--radio-addr", dest="radio_addr", type="intx", default=0,
        help="Set Local address [default=%default]")
    parser.add_option(
        "-A", "--rx-antenna", dest="rx_antenna", type="string", default="TX/RX",
        help="Set RX antenna [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set RX freq [default=%default]")
    parser.add_option(
        "", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(65-20),
        help="Set RX gain [default=%default]")
    parser.add_option(
        "", "--rx-lo-offset", dest="rx_lo_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set RX LO offset [default=%default]")
    parser.add_option(
        "", "--samps-per-sym", dest="samps_per_sym", type="intx", default=4,
        help="Set Samples/symbol [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(915e6),
        help="Set TX freq [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(45),
        help="Set TX gain [default=%default]")
    parser.add_option(
        "", "--tx-lo-offset", dest="tx_lo_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set TX LO offset [default=%default]")
    parser.add_option(
        "-r", "--rate", dest="rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set Sample rate [default=%default]")
    parser.add_option(
        "-c", "--cen-freq", dest="cen_freq", type="eng_float", default=eng_notation.num_to_str(2442500000),
        help="Set Center Freq [default=%default]")
    return parser


def main(top_block_cls=simple_trx_mac, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ampl=options.ampl, args=options.args, arq_timeout=options.arq_timeout, broadcast_interval=options.broadcast_interval, dest_addr=options.dest_addr, lo_offset=options.lo_offset, max_arq_attempts=options.max_arq_attempts, mtu=options.mtu, port=options.port, radio_addr=options.radio_addr, rx_antenna=options.rx_antenna, rx_freq=options.rx_freq, rx_gain=options.rx_gain, rx_lo_offset=options.rx_lo_offset, samps_per_sym=options.samps_per_sym, tx_freq=options.tx_freq, tx_gain=options.tx_gain, tx_lo_offset=options.tx_lo_offset, rate=options.rate, cen_freq=options.cen_freq)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
