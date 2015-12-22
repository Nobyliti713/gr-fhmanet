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

#ifndef INCLUDED_FH_CHANNEL_MESSAGE_STROBE_H
#define INCLUDED_FH_CHANNEL_MESSAGE_STROBE_H

#include "api.h"
#include <gnuradio/block.h>
#include <gnuradio/blocks/message_strobe.h>

namespace gr {
  namespace fhmanet {

    /*!
     * \brief Send message at defined interval
     * \ingroup fhmanet
     *
     * \details
     * Takes a PMT message and sends it out every \p period_ms
     * milliseconds. Useful for testing/debugging the message system.
     */
    class FHMANET_API fh_channel_message_strobe : virtual public gr::blocks::message_strobe
    {
    public:
      // gr::blocks::message_strobe::sptr
      /*!
       * Make a message strobe block that broadcasts the correct channel
       * frequency to send message \p msg every \p
       * period_ms milliseconds.
       *
       * \param msg The message to send as a PMT.
       * \param period_ms the time period in milliseconds in which to
       *                  send \p msg.
       */
      static sptr make(pmt::pmt_t msg2, float period_ms);

      /*!
       * \param sequence_length Number of hops before the sequence repeats.
       */
      virtual double sequence_length() const = 0;

      /*!
       * \param center_freq center frequency of the channel.
       */
      virtual double center_freq() const = 0;

      /*!
       * Width of each channel in Hz.
       * \param channel_widht width of each channel in Hz.
       */
      virtual float channel_width() const = 0;

      /*!
       * \param num_channels the number of sub-channels in the frequency bandwidth.
       */
      virtual int num_channels() const = 0;

      /*!
       * \param freq_offset the offset of the output frequency used for the 2nd output.
       */
      virtual int freq_offset() const = 0;
    };

  } /* namespace fhmanet */
} /* namespace gr */

#endif /* INCLUDED_FH_CHANNEL_MESSAGE_STROBE_H */
