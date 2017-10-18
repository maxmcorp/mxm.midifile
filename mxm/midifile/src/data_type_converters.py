# -*- coding: utf-8 -*-

from struct import pack, unpack

"""
This module contains functions for reading and writing the special data types
that a midi file contains.

Good info here.
http://www.devdungeon.com/content/working-binary-data-python#bytes

"""

"""
nibbles are four bits. A byte consists of two nibles.
hiBits==0xF0, loBits==0x0F Especially used for setting
channel and event in 1. byte of musical midi events
"""


def getNibbles(byte):
    """
    Returns hi and lo bits in a byte as a tuple
    >>> getNibbles(142)
    (8, 14)
    
    Asserts byte value in byte range
    >>> getNibbles(256)
    Traceback (most recent call last):
        ...
    ValueError: Byte value out of range 0-255: 256
    """
    if not 0 <= byte <= 255:
        raise ValueError('Byte value out of range 0-255: %s' % byte)
    return (byte >> 4 & 0xF, byte & 0xF)


def setNibbles(hiNibble, loNibble):
    """
    Returns byte with value set according to hi and lo bits
    Asserts hiNibble and loNibble in range(16)
    >>> setNibbles(8, 14)
    142
    
    >>> setNibbles(8, 16)
    Traceback (most recent call last):
        ...
    ValueError: Nible value out of range 0-15: (8, 16)
    """
    if not (0 <= hiNibble <= 15) or not (0 <= loNibble <= 15):
        raise ValueError('Nible value out of range 0-15: (%s, %s)' % (hiNibble, loNibble))
    return (hiNibble << 4) + loNibble


def readBew(value):
    """
    Reads bytes as unsigned big endian word, (asserts len(value) in [1,2,4])
    >>> readBew( bytes([0x61, 0xe1, 0xe2, 0xe3]) )
    1642193635
    >>> readBew( bytes([0x61, 0xe1]) )
    25057
    >>> readBew(writeBew(42, 1))
    42
    >>> readBew('')
    Traceback (most recent call last):
      ...
    ValueError: value of wrong length. must be 1, 2 or 4. len(value)==0
    """
    if not len(value) in [1,2,4]:
        raise ValueError('value of wrong length. must be 1, 2 or 4. len(value)==%s' % len(value) )
    return int.from_bytes(value, byteorder='big', signed=False)


def writeBew(value, length):
    """
    Write int as big endian formatted bytes, (asserts length in [1,2,4])
    Difficult to print the result in doctest, so I do a simple roundabout test.
    >>> readBew(writeBew(25057, 2))
    25057
    >>> readBew(writeBew(1642193635, 4))
    1642193635
    >>> readBew(writeBew(16, 3))
    Traceback (most recent call last):
        ...
    ValueError: words must be one of 1,2 or 4
    """
    if not length in [1,2,4]:
        raise ValueError('words must be one of 1,2 or 4')
    return value.to_bytes(length, byteorder='big', signed=False)


"""
Variable Length Data (varlen) is a data format sprayed liberally throughout
a midi file. It can be anywhere from 1 to 4 bytes long.
If the 8'th bit is set in a byte another byte follows. The value is stored
in the lowest 7 bits of each byte. So max value is 4x7 bits = 28 bits.
"""


def readVar(value):
    """
    Converts varlength format to integer. Just pass it 0 or more chars that
    might be a varlen and it will only use the relevant chars.
    use varLen(readVar(value)) to see how many bytes the integer value takes.
    asserts len(value) >= 0
    >>> readVar(bytes([64]))
    64
    >>> readVar(bytes([225, 226, 227, 97]))
    205042145
    """
    sum = 0
    for byte in value:
    # for byte in unpack('%sB' % len(value), value):
        sum = (sum << 7) + (byte & 0x7F)
        if not 0x80 & byte: break # stop after last byte
    return sum



def writeVar(value):
    """
    Converts an integer to varlength format
    >>> writeVar(127)
    [127]
    >>> writeVar(205042145)
    [225, 226, 227, 97]
    """
    sevens = to_n_bits(value)
    for i in range(len(sevens)-1):
        sevens[i] = sevens[i] | 0x80 # set msb to 1
    return sevens


def varLen(value):
    """
    Returns the the number of bytes an integer will be when
    converted to varlength
    >>> varLen(0)
    1
    >>> varLen(2097154)
    4
    """
    if value <= 127:
        return 1
    elif value <= 16383:
        return 2
    elif value <= 2097151:
        return 3
    else:
        return 4


def to_n_bits(value, length=None, nbits=7):
    """
    returns the integer value as a sequence of nbits bytes
    >>> v = 205042145
    >>> l = varLen(v)
    >>> to_n_bits(v, length=l)
    [97, 98, 99, 97]
    >>> to_n_bits(127)
    [127]
    >>> to_n_bits(300)
    [2, 44]
    """
    if length is None:
        length = varLen(value)
    bit7s = [(value >> (i*nbits)) & 0b1111111 for i in range(length)]
    bit7s.reverse()
    return bit7s


def manufacturer_id(man_id):
    """
    man_id is 1 OR 3 bytes long. If the first byte is zero then it MUST be a 3 byte value
    >>> manufacturer_id([0])
    Traceback (most recent call last):
    ...
    ValueError: Incorrect manufacturer id.
    >>> manufacturer_id([42, 0, 42])
    Traceback (most recent call last):
    ...
    ValueError: Incorrect manufacturer id.
    >>> list(manufacturer_id([0x41]))
    [65]
    >>> list(manufacturer_id([0,0,0x41]))
    [0, 0, 65]

    Note that microsofts 4 byte id [0x00, 0x00, 0x41] is different than Rolands 1 byte
    id of [0x41], so not only the values matter but also the length of the id.
     """
    man_id = bytes(man_id)
    len_id = len(man_id)
    if len_id == 1 and man_id[0] != 0:
        assert(0 <= man_id[0] <= 127), '1 byte manufacturer id is out of range.'
    elif len_id == 3 and man_id[0] == 0:
        num_val = (man_id[1]<<7) + man_id[2]
        assert(0 <= num_val <= 16384), '3 byte manufacturer id is out of range.'
    else:
        raise ValueError('Incorrect manufacturer id.')
    return man_id


def from_twos_complement(val):
    """
    >>> bin(from_twos_complement(7))
    '0b111'
    >>> from_twos_complement(-7)
    249
    >>> bin(from_twos_complement(-7))
    '0b11111001'
    >>> bin(from_twos_complement(-128))
    '0b10000000'
    """
    # assert(0<=val<=255), 'val expected to be in range 0..255. Was: %s' % val
    if val & 0b10000000:
        val = -((val^0xFF)+1)
    return val

def to_twos_complement(val):
    """
    >>> to_twos_complement(-7)
    249
    >>> bin(to_twos_complement(-7))
    '0b11111001'
    >>> bin(to_twos_complement(-1))
    '0b11111111'
    >>> bin(to_twos_complement(1))
    '0b1'
    >>> bin(to_twos_complement(256))
    Traceback (most recent call last):
    ...
    AssertionError: val expected to be in range -128..127. Was: 256
    """
    assert(-128<=val<=127), 'val expected to be in range -128..127. Was: %s' % val
    if val < 0:
        val = -((val^0xFF)+1)
    return val


if __name__ == '__main__':
    
    import doctest
    doctest.testmod() # run test on inline examples first

