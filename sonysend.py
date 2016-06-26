#!/usr/bin/python3

import re;
import argparse

syn0_re = re.compile('^[01]+$');
syn1_re = re.compile('^(\d+)-(\d+)$');
syn3_re = re.compile('^(\d+)\.(\d+)\.(\d+)-(\d+)$');
syn2_re = re.compile('^(\d+)\.(\d+)-(\d+)$');

def bitsplit(bits, value, size):
    for _ in range(0, size):
        bits.append( value & 1 );
        value >>= 1;
    return bits;
    
def sony_code_to_bits(code):

    # allow a literal bitstring 010101010101
    if syn0_re.match(code) is not None:
        return [ int(x) for x in code ]

    # nope? okay, let's be smart about this.
        
    m = syn1_re.match(code)

    if m is not None:
        if int(m.groups()[0]) < 32:
            sizes = [7,5]
        else:
            sizes = [7,8]
    else:
        m = syn2_re.match(code)
        if m is not None:
            sizes = [7,5,8]
        else:
            m = syn3_re.match(code)
            if m is not None:
                sizes = [7,5,3,5]
            else:
                raise Exception('Invalid code syntax');
     
    values = [int(x) for x in m.groups()]
    values = values[1:] + values[:1]
    
    bits = []
    
    for value, size in zip(values, sizes):
        bitsplit(bits, value, size)

    return bits
        
def bits_to_ircode(bits):
    """ Convert e.g. [1,0,1,0,1,1,1,0,0] to an iTach ircode sequence """
    zero_one = [ '24,24,', '24,48,' ]
    return '96,' + ''.join( [ zero_one[x] for x in bits ] ) + '1032';

def call_sony(host, code):
    from itachsend import call_itach
    
    bits = sony_code_to_bits(code)
    ircode = bits_to_ircode(bits)
    call_itach(host, 40000, ircode, 3)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Send a message to a Sony device via an iTach.')
    parser.add_argument('-H', dest='host', help='IP address or hostname', required=True)
    parser.add_argument('-c', dest='code', help='Command code: a-c or a1.a2-c', required=True)

    args = parser.parse_args();
    
    call_sony(args.host, args.code)
    