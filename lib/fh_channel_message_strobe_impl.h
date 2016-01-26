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

#ifndef INCLUDED_FH_CHANNEL_MESSAGE_STROBE_IMPL_H
#define INCLUDED_FH_CHANNEL_MESSAGE_STROBE_IMPL_H

#include <../include/fhmanet/fh_channel_message_strobe.h>
#include <../include/fhmanet/xorshift.h>

namespace gr {
  namespace fhmanet {

    class FHMANET_API fh_channel_message_strobe_impl : 
		public fh_channel_message_strobe //gr::blocks::message_strobe
    {
    private:
      boost::shared_ptr<boost::thread> d_thread;
      bool d_finished;
      float d_period_ms;
      pmt::pmt_t d_msg;
      double d_center_freq;
      float d_channel_width;
      unsigned int d_num_channels;
      unsigned int d_sequence_length;
      unsigned int d_tx_security_key;
	  boost::posix_time::ptime d_time;
	  boost::posix_time::time_duration d_duration;
	  double d_current_hop; //which hop in the sequence at the current time
	  double d_hop_index; //must be <= sequence_length
	  std::vector<uint64_t> d_hop_sequence;
	  xorshift *d_xorshift;
	  
      void run();

    public:
      fh_channel_message_strobe_impl(float period_ms,
									 double center_freq,
									 float channel_width, 
									 unsigned int num_channels, 
									 unsigned int sequence_length, 
									 unsigned int tx_security_key);
      ~fh_channel_message_strobe_impl();

      void set_period(float period_ms) { d_period_ms = period_ms; }
      float period() const { return d_period_ms; }
      
      void set_center_freq(double center_freq) {d_center_freq = center_freq; }
      double center_freq() const { return d_center_freq; }
      
	  void set_channel_width(float channel_width) {d_channel_width = channel_width; }
      float channel_width() const { return d_channel_width; }

	  void set_num_channels(unsigned int num_channels) {d_num_channels = num_channels; }
      unsigned int num_channels() const { return d_num_channels; }
      
      void set_sequence_length(unsigned int sequence_length) {d_sequence_length = sequence_length; }
      unsigned int sequence_length() const { return d_sequence_length; }
      
      void set_tx_security_key(unsigned int tx_security_key) {d_tx_security_key = tx_security_key; }
      unsigned int tx_security_key() const { return d_tx_security_key; }
      
      bool start();
      bool stop();
    };

  } /* namespace fhmanet */
} /* namespace gr */

#endif /* INCLUDED_FH_CHANNEL_MESSAGE_STROBE_IMPL_H */
