/* -*- c++ -*- */

#define FHMANET_API

%include "gnuradio.i"			// the common stuff

%apply std::vector<unsigned long> { std::vector<size_t> };

//load generated python docstrings
%include "fhmanet_swig_doc.i"

%{
#include "fhmanet/fh_channel_message_strobe.h"
#include "fhmanet/xorshift.h"
%}

%include "fhmanet/fh_channel_message_strobe.h"
%include "fhmanet/xorshift.h"

GR_SWIG_BLOCK_MAGIC2(fhmanet, fh_channel_message_strobe);
