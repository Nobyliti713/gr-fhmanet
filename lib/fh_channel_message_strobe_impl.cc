/* -*- c++ -*- */
/*
 * Copyright 2012-2013 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "fh_channel_message_strobe_impl.h"
#include <gnuradio/io_signature.h>
#include <cstdio>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdexcept>
#include <string.h>
#include <iostream>
#include <cmath>

namespace gr {
  namespace fhmanet {

    fh_channel_message_strobe::sptr
    fh_channel_message_strobe::make(pmt::pmt_t msg2, double center_freq, 
			float channel_width, int num_channels, double sequence_length, 
			int freq_offset)
    {
      return gnuradio::get_initial_sptr
        (new fh_channel_message_strobe_impl(msg2, center_freq, channel_width, 
			num_channels, sequence_length, freq_offset));
    }

    fh_channel_message_strobe_impl::fh_channel_message_strobe_impl(pmt::pmt_t msg2, 
			double center_freq, float channel_width, int num_channels, 
			double sequence_length, int freq_offset)
      : message_strobe("fh_channel_message_strobe",
                 io_signature::make(0, 0, 0),
                 io_signature::make(0, 0, 0),
                 d_finished(false), d_period_ms(period_ms), d_msg(msg)),
        d_msg2(msg2),
        d_period_ms(period_ms),
        d_center_freq(center_freq),
        d_channel_width(channel_width),
        d_num_channels(num_channels),
        d_sequence_length(sequence_length),
        d_freq_offset(freq_offset)
    {
      message_port_register_out(pmt::mp("freq_out"));
      d_thread = boost::shared_ptr<boost::thread>
        (new boost::thread(boost::bind(&fh_channel_message_strobe_impl::run, this)));
        
      message_port_register_out(pmt::mp("offset_freq_out"));  

      //message_port_register_in(pmt::mp("set_msg"));
      //set_msg_handler(pmt::mp("set_msg"),
      //                boost::bind(&message_strobe_impl::set_msg, this, _1));
    }

    fh_channel_message_strobe_impl::~fh_channel_message_strobe_impl()
    {
    }

    bool
    fh_channel_message_strobe_impl::start()
    {
      // NOTE: d_finished should be something explicitely thread safe. But since
      // nothing breaks on concurrent access, I'll just leave it as bool.
      d_finished = false;
      d_thread = boost::shared_ptr<gr::thread::thread>
        (new gr::thread::thread(boost::bind(&fh_channel_message_strobe_impl::run, this)));

	  //call the xorshift PRNG here to generate the hop sequence?
	  xorshift(seed, d_sequence_length);

	  //translate raw PRNG output to frequencies
	  for( uint8_t i = 0; i < d_sequence_length; i++)
          {
			hop_sequence[i] = d_center_freq + ((int(hop_sequence[i] % 
				d_num_channels) - (d_num_channels / 2)) * 
				d_channel_width);
		  }
	  
      return block::start();
    }
    
    bool
    fh_channel_message_strobe_impl::stop()
    {
      // Shut down the thread
      d_finished = true;
      d_thread->interrupt();
      d_thread->join();

      return block::stop();
    }
    
    void fh_channel_message_strobe_impl::run()
    {
      while(!d_finished) {
        boost::this_thread::sleep(boost::posix_time::milliseconds(d_period_ms));
        if(d_finished) {
          return;
        }
		//check system time to get index of the hop sequence
		d_time = boost::posix_time::microsec_clock::local_time();
		d_duration.total_milliseconds( d_time.time_of_day() );
		
		d_current_hop = d_duration.total_milliseconds( d_time.time_of_day() ) 
			/ d_period_ms;
		
		d_current_hop = fmod(d_current_hop, d_sequence_length);

		//these are the values for the PMTs	
		d_msg = pmt::mp("freq", hop_sequence[d_current_hop]);
		d_msg2 = pmt::mp("freq", hop_sequence[d_current_hop] + d_freq_offset);
		
		message_port_pub(pmt::mp("freq_out"), d_msg);
        message_port_pub(pmt::mp("offset_freq_out"), d_msg2);
      }
    }

  } /* namespace fhmanet */
} /* namespace gr */
