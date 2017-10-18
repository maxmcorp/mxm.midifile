# -*- coding: utf-8 -*-

"""
This module writes the raw data to a file.
"""

# standard library imports
import sys
import io

# custom import
from mxm.midifile.src.data_type_converters import writeBew, writeVar

class RawOutstreamFile:

    """
    Writes a midi file to disk.
    >>> out = io.BytesIO()
    >>> rawOut = RawOutstreamFile(out)
    >>> rawOut.writeSlice(b'MThd')
    >>> rawOut.writeBew(6, 4)
    >>> rawOut.writeBew(1, 2)
    >>> rawOut.writeBew(2, 2)
    >>> rawOut.writeBew(15360, 2)
    >>> out.seek(0)
    0
    >>> list(out.read())
    [77, 84, 104, 100, 0, 0, 0, 6, 0, 1, 0, 2, 60, 0]
    >>> with RawOutstreamFile(io.BytesIO()) as r:
    ...     r.writeSlice(b'MTrk')
    ...     r.read()
    b'MTrk'
    """

    def __init__(self, f=None):
        "f can be a filename or an open file handle"
        if not f:
            self.outfile = io.BytesIO()
        elif isinstance(f, str): # is a filename
            self.outfile = open(f, 'wb')
        else: # is a file object
            self.outfile = f

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

    def close(self):
        self.outfile.close()

    # type specific data write methods

    def writeSlice(self, str_slice):
        "Writes the next text slice to the raw data"
        self.outfile.write(bytes(str_slice))

    def writeBew(self, value, length=1):
        "Writes a value to the file as big endian word"
        self.writeSlice(writeBew(value, length))

    def writeVarLen(self, value):
        "Writes a variable length word to the file"
        self.writeSlice(writeVar(value))

    def read(self):
        return self.read_all()

    def read_all(self):
        self.outfile.seek(0)
        return self.outfile.read()
        

if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first

    # from helpers import datadir
    # out_file = datadir('tests/midifiles/midiout.mid')
    # with RawOutstreamFile(out_file) as rawOut:
    #     rawOut.writeSlice(b'MThd')
    #     rawOut.writeBew(6, 4)
    #     rawOut.writeBew(1, 2)
    #     rawOut.writeBew(2, 2)
    #     rawOut.writeBew(15360, 2)
