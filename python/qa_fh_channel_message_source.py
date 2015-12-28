#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import fhmanet_swig as fhmanet

class qa_fh_channel_message_strobe (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_fh_channel_message_strobe(self):
        #need to establish control messages
        //msg = pmt.cons(pmt.intern("freq"), pmt.from_double(d_hop_sequence[d_current_hop]))
        //msg2 = pmt.intern("TESTING MSG2")
        src = fhmanet.fh_channel_message_strobe(msg, 100, msg2, 1000000000,
				25000, 100, 10000, 12500, 12345)
		snk1 = blocks.message_debug()
		snk2 = blocks.message_debug()

		tb = gr.top_block()
        tb.msg_connect(src, "freq_out", snk1, "store")
        tb.msg_connect(src, "offset_freq_out", snk2, "store")
        tb.start()
        time.sleep(1)
        tb.stop()
        tb.wait()
        rec_msg1 = snk1.get_message(0)
        rec_msg2 = snk2.get_message(0)
        self.assertTrue(pmt.eqv(rec_msg, msg))


if __name__ == '__main__':
    gr_unittest.run(qa_fh_channel_message_strobe, "qa_fh_channel_message_strobe.xml")
