# gr-fhmanet
Frequency-hopping time-synchronized mobile ad-hoc networking in GNURadio. Partially based on gr-mac. Definitely still a work in 
progress.

Adds a FH Channel Message Strobe block. This is meant to push a message (PMT pair) to a signal source on the transmitter side or 
to a Frequency Xlating FIR Filter on the receiver side. The hop sequence uses a XORSHIFT PRNG generated from a shared seed number 
(Transmission Security Key).

The MAC layer block is currently the same as gr-mac's. I need to add code for transmitting synchronization packets and changing 
the clock time. 

Also includes a DBPSK Modem hierarchical block.
