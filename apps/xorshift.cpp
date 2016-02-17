/* -*- c++ -*- */
/*
 * Copyright 2016 Jason Noble.
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

#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <map>
#include <utility>

/*
* XORshift pseudo-random number generator
* Generates a pseudo-random sequence of maximal length 2^64 - 1
* The |a,b,c| values are currently hardcoded at |23,17,26|.
*/

uint64_t d_rng_state[2]; //initial xorshift values
uint64_t d_rng_output = 0; //raw xorshift output

std::vector<uint64_t> d_hop_sequence;
std::vector<int64_t> d_chan_sequence;
std::map <std::string, unsigned int> d_config_options;
unsigned int d_sequence_length;
unsigned int d_center_freq;
unsigned int d_channel_width;
unsigned int d_num_channels;

std::ifstream input_file("hopset.conf");
std::string line;

//config file parser code from:
//http://stackoverflow.com/questions/6892754/creating-a-simple-configuration-file-and-parser-in-c
//and
//http://www.yolinux.com/TUTORIALS/CppStlMultiMap.html

void read_conf()
{
	if(!input_file.is_open())
	{
		//could not open
		std::cout << "Could not open config file." << std::endl;
	}
	else
	{
		std::cout << "Reading config file." << std::endl;
		
		while( std::getline(input_file, line) )
		{
			std::istringstream input_line(line);
			std::string key;
			if( std::getline(input_line, key, '=') )
			{
				std::string value;
				if( std::getline(input_line, value) ) 
					d_config_options.insert(std::make_pair(key,std::stoul(value)));
			}
		}
	}
	d_sequence_length = d_config_options.at("sequence_length");
	for( std::map<std::string, unsigned int>::iterator ii=d_config_options.begin(); ii!=d_config_options.end(); ii++)
       std::cout << (*ii).first << ": " << (*ii).second << std::endl;
    input_file.close();
}

std::vector<uint64_t> xor_sequence(std::vector<uint64_t> hop_sequence)
{
	d_rng_state[0] = d_config_options.at("tx_security_key");
    d_rng_state[1] = d_rng_state[0];

    for(unsigned int jj= 0 ; jj <d_sequence_length; jj++)
    {
		uint64_t x = d_rng_state[0];
		uint64_t const y = d_rng_state[1];

		d_rng_state[0] = y;
    
		x ^= x << 23; //a
		x ^= x >> 17; //b
		x ^= y ^ (y >> 26); //c

		d_rng_state[1] = x;
		d_rng_output = x + y;

		hop_sequence.push_back(d_rng_output);
    }
    std::cout << "XORSHIFT sequence generation complete" << std::endl;
    return hop_sequence;
}

//code to write to CSV:
//http://stackoverflow.com/questions/25201131/writing-csv-files-from-c
void write_rng_sequence(std::vector<uint64_t> hop_sequence)
{
	std::ofstream hop_sequence_file("rng_sequence.csv");
	
	std::cout << "Writing Raw XORSHIFT sequence to CSV..." << std::endl;
	
	for(std::vector<uint64_t>::iterator kk=hop_sequence.begin() ; kk !=hop_sequence.end(); kk++)
		hop_sequence_file << *kk << ",";

	hop_sequence_file.close();
	std::cout << "Export Complete" << std::endl;
}

std::vector<int64_t> chan_conversion(std::vector<uint64_t> hop_sequence, std::vector<int64_t> chan_sequence,
	std::map <std::string, unsigned int> config_options)
{
	//assigns values from the loaded config file
	d_center_freq = config_options.at("center_freq");
	d_channel_width = config_options.at("channel_width");
	d_num_channels = config_options.at("num_channels");
	uint64_t buff_in = 0;
	int64_t buff_out = 0;
		
	for(int i=0; i < hop_sequence.size(); i++)
    {
		buff_in = hop_sequence[i];
		//channelizer. uses the modulus of the raw PRNG number output
		//as a channel number from [0, num_channels]
		//sets the frequency by adjusting the center frequency based on 
		//channel bandwidth
		std::cout << "Buff In " << buff_in << " % " << d_num_channels << " = " << (buff_in % d_num_channels);
		std::cout << " Buff In (" << buff_in << ")";
		buff_out = ((buff_in % 
			d_num_channels - (d_num_channels /2)) * d_channel_width);
		std::cout << " % " << d_num_channels << " - " << (d_num_channels/2) << " * " << d_channel_width 
			<< " = " << buff_out << std::endl;
		chan_sequence.push_back(buff_out);
	}
	return chan_sequence;
}

void write_channel_sequence(std::vector<int64_t> chan_sequence)
{
	std::ofstream chan_sequence_file("channel_sequence.csv");
	
	std::cout << "Writing channel sequence to CSV..." << std::endl;
	
	for(std::vector<int64_t>::iterator nn=chan_sequence.begin() ; nn !=chan_sequence.end(); nn++)
	{
		chan_sequence_file << *nn << ",";
	}
	chan_sequence_file.close();
	std::cout << "Export Complete" << std::endl;
}

std::vector<uint64_t> freq_conversion(std::vector<uint64_t> hop_sequence,
	std::map <std::string, unsigned int> config_options)
{
	//assigns values from the loaded config file
	d_center_freq = config_options.at("center_freq");
	d_channel_width = config_options.at("channel_width");
	d_num_channels = config_options.at("num_channels");
		
	for(std::vector<uint64_t>::iterator ll=hop_sequence.begin() ; ll !=hop_sequence.end(); ll++)
    {
		
		//channelizer. uses the modulus of the raw PRNG number output
		//as a channel number from [0, num_channels]
		//sets the frequency by adjusting the center frequency based on 
		//channel bandwidth
		*ll = d_center_freq + ((*ll % 
			d_num_channels - (d_num_channels / 2)) * d_channel_width);
	}
	return hop_sequence;
}

void write_freq_sequence(std::vector<uint64_t> hop_sequence)
{
	std::ofstream hop_sequence_file("hop_sequence.csv");
	
	std::cout << "Writing Frequency Hop sequence to CSV..." << std::endl;
	
	for(std::vector<uint64_t>::iterator mm=hop_sequence.begin() ; mm !=hop_sequence.end(); mm++)
		hop_sequence_file << *mm << ",";

	hop_sequence_file.close();
	std::cout << "Export Complete" << std::endl;
}

int main()
{
	read_conf();
	d_hop_sequence = xor_sequence(d_hop_sequence);
	write_rng_sequence(d_hop_sequence);
	//d_chan_sequence = d_hop_sequence;
	d_chan_sequence = chan_conversion(d_hop_sequence, d_chan_sequence, d_config_options);
	write_channel_sequence(d_chan_sequence);
	d_hop_sequence = freq_conversion(d_hop_sequence, d_config_options);
	write_freq_sequence(d_hop_sequence);
	
	return 0;
}    
