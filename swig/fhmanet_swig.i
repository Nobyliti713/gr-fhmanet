/* -*- c++ -*- */

#define FHMANET_API

%include "gnuradio.i"			// the common stuff

/* unsigned64 Convert from Python --> C */
%typemap(in) uint64_t {
%#ifdef HAVE_LONG_LONG
    if (PyLong_Check($input)) {
        $1 = (uint64_t)PyLong_AsUnsignedLongLong($input);
    } else if (PyInt_Check($input)) {
        $1 = (uint64_t)PyInt_AsUnsignedLongLongMask($input);
    } else
%#endif
    {
        SWIG_exception_fail(SWIG_ValueError, "unsupported integer size - uint64_t input too large");
    }
}

/* unsigned64 Convert from C --> Python */
%typemap(out) uint64_t {
%#ifdef HAVE_LONG_LONG
    $result = PyLong_FromUnsignedLongLong((unsigned PY_LONG_LONG)$1);
%#else
    SWIG_exception_fail(SWIG_ValueError, "unsupported integer size - uint64_t output too large");
%#endif
}


//load generated python docstrings
%include "fhmanet_swig_doc.i"

%{
#include "fhmanet/fh_channel_message_strobe.h"
#include "fhmanet/xorshift.h"
%}

%include "fhmanet/fh_channel_message_strobe.h"
%include "fhmanet/xorshift.h"

GR_SWIG_BLOCK_MAGIC2(fhmanet, fh_channel_message_strobe);
