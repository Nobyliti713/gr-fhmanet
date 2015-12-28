/* -*- c++ -*- */
/*
 * Copyright 2015 Jason Noble.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_XORSHIFT_H
#define INCLUDED_XORSHIFT_H

#include <cstdint>
#include <vector>
#include "api.h"

namespace gr {
  namespace fhmanet {

    /*!
     * \brief XORshift pseudo-random number generator
     * \ingroup fhmanet
     *
     * \details
     * Generates a pseudo-random sequence of maximal length 2^64 - 1
     * The |a,b,c| values are currently hardcoded at |23,17,25|.
     */
    class FHMANET_API xorshift
    {
     private:
      uint64_t d_rng_state[2]; //initial xorshift values
      uint64_t d_rng_output = 0; //raw xorshift output
      uint16_t d_generated_num = 0; //output after modulus
      //short d_channel_shift; //re-centers channels at 0
      //uint16_t d_num_channels;
      uint64_t d_seed; //PRNG seed, should take the transmission security key
      uint64_t d_sequence_length;

     public:
       xorshift(uint64_t seed, uint64_t sequence_length)
              {d_seed = seed; d_sequence_length = sequence_length;}
           ~xorshift();

       //static int checkseed(int d_seed);

       std::vector<uint64_t> hop_sequence;
       //^the vector that stores the PRNG output

       std::vector<uint64_t> xor_sequence()
       {
          d_rng_state[0] = d_seed;
          d_rng_state[1] = d_seed; //consider changing this to clock time?

          for( uint8_t i = 0; i < d_sequence_length; i++)
          {
            uint64_t x = d_rng_state[0];
            uint64_t const y = d_rng_state[1];

            d_rng_state[0] = y;
            x ^= x << 23; //a
            x ^= x >> 17; //b
            x ^= y ^ (y >> 25); //c

            d_rng_state[1] = x;
            d_rng_output = x + y;

            //stuff after isn't pure PRNG, adjusts the output for the FHSS channels. consider moving to another block/source file?
            //d_generated_num = d_rng_output % d_num_channels;
            //d_channel_shift = int(d_generated_num) - (d_num_channels / 2);
            hop_sequence[i] = d_rng_output;
          }
          return hop_sequence;

        }

       //int seed() const {return d_seed;}
    };

  } /* namespace fhmanet */
} /* namespace gr */

#endif /* INCLUDED_XORSHIFT_H */

