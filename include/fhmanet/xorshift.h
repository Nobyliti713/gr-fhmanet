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
      uint64_t d_seed; //PRNG seed, should take the transmission security key
      uint64_t d_sequence_length;

     public:
       xorshift(unsigned int seed, unsigned int sequence_length)
              {d_seed = uint64_t(seed); 
			   d_sequence_length = uint64_t(sequence_length);}
           ~xorshift();

       //std::vector<uint64_t> hop_sequence;
       //^the vector that stores the PRNG output

       //std::vector<uint64_t> xor_sequence(std::vector<uint64_t>& hop_sequence)
       void xor_sequence(std::vector<unsigned long long> hop_sequence)
       {
          d_rng_state[0] = d_seed;
          d_rng_state[1] = d_seed;

          for( uint8_t i = 0; i < d_sequence_length; i++)
          {
            uint64_t x = d_rng_state[0];
            uint64_t const y = d_rng_state[1];

            d_rng_state[0] = y;
            x ^= x << 23; //a
            x ^= x >> 17; //b
            x ^= y ^ (y >> 26); //c

            d_rng_state[1] = x;
            d_rng_output = x + y;

            hop_sequence[i] = d_rng_output;
          }
          
          //return hop_sequence;
        }

    };

  } /* namespace fhmanet */
} /* namespace gr */

#endif /* INCLUDED_XORSHIFT_H */

