# -*- coding: utf-8 -*-

# standard library imports
from mxm.midifile.src.data_type_converters import readBew, readVar, varLen

import os, os.path, sys

class RawInstreamFile:

    """
    RawInstreamFile parses and reads data from an input file. It takes care of big 
    endianess, and keeps track of the cursor position. The midi parser 
    only reads from this object. Never directly from the file.
    
    >>> import io
    >>> f = io.BytesIO(b'0123456789')
    >>> raw_in = RawInstreamFile(f)
    >>> raw_in.nextSlice(length=4, move_cursor=0)
    b'0123'
    >>> raw_in.nextSlice(length=4, move_cursor=1)
    b'0123'
    >>> raw_in.nextSlice(length=4)
    b'4567'
    """

    def __init__(self, infile=''):
        """
        If 'file' is a string we assume it is a path and read from that file.
        If it is a file descriptor we read from the file, but we don't close it.
        Midi files are usually pretty small <50KB, so it should be safe to copy
        them into memory.
        """
        if infile:
            if isinstance(infile, str):
                infile = open(infile, 'rb')
                self.data = infile.read()
                infile.close()
            else:
                # don't close the f
                infile.seek(0)
                self.data = infile.read()
        else:
            self.data = b''
        # start at beginning ;-)
        self.setCursor(0)


    # # setting up data manually
    
    # def setData(self, data=''):
    #     "Sets the data from a string."
    #     self.data = data
    
    # cursor operations

    def setCursor(self, position=0):
        """
        Sets the absolute position of the cursor
        >>> import io
        >>> f = io.BytesIO(b'0123456789')
        >>> raw_in = RawInstreamFile(f)
        >>> raw_in.setCursor(6)
        >>> raw_in.nextSlice(length=4, move_cursor=0)
        b'6789'
        """
        self.cursor = position


    def getCursor(self):
        """
        Returns the value of the cursor
        >>> import io
        >>> f = io.BytesIO(b'0123456789')
        >>> raw_in = RawInstreamFile(f)
        >>> raw_in.nextSlice(length=4, move_cursor=1)
        b'0123'
        >>> raw_in.getCursor()
        4
        """
        return self.cursor
        
        
    def moveCursor(self, relative_position=0):
        """
        Moves the cursor to a new position relative to current position. Usually just forward.
        >>> import io
        >>> f = io.BytesIO(b'0123456789')
        >>> raw_in = RawInstreamFile(f)
        >>> raw_in.nextSlice(length=2, move_cursor=1)
        b'01'
        >>> raw_in.moveCursor(3)
        >>> raw_in.getCursor()
        5
        """
        self.cursor += relative_position


    # native data reading functions

    def nextSlice(self, length, move_cursor=1):
        """
        Reads the next text slice from the raw data, with length
        >>> import io
        >>> f = io.BytesIO(b'0123456789')
        >>> raw_in = RawInstreamFile(f)
        >>> [raw_in.nextSlice(length=3, move_cursor=1) for i in range(6)]
        [b'012', b'345', b'678', b'9', b'', b'']
        """
        c = self.cursor
        slc = self.data[c:c+length]
        if move_cursor:
            self.moveCursor(length)
        return slc


    def readBew(self, n_bytes=1, move_cursor=1):
        """
        Reads n bytes of date from the current cursor position.
        Moves cursor if move_cursor is true
        >>> import io
        >>> f = io.BytesIO(bytes([0,0,0,42, 0,0,1,0, 0,1,0,0, 1,0,0,0, 1,0, 42]))
        >>> raw_in = RawInstreamFile(f)
        >>> [raw_in.readBew(4) for i in range(4)] + [raw_in.readBew(2)] + [raw_in.readBew(1)]
        [42, 256, 65536, 16777216, 256, 42]
        """
        return readBew(self.nextSlice(n_bytes, move_cursor))


    def readVarLen(self):
        """
        Reads a variable length value from the current cursor position.
        Reads the length of varlen and moves cursor apropriately
        >>> import io
        >>> v1,v2,v3,v4 = (0b11111111, 0b11111110, 0b11111100, 0b00101010)
        >>> (v1,v2,v3,v4)
        (255, 254, 252, 42)
        >>> f = io.BytesIO( bytes([v1,v2,v3,v4, v2,v3,v4, v3,v4, v4]) )
        >>> raw_in = RawInstreamFile(f)
        >>> [raw_in.readVarLen() for i in range(4)]
        [268418602, 2080298, 15914, 42]
        """
        MAX_VARLEN = 4 # Max value varlen can be
        var = readVar(self.nextSlice(MAX_VARLEN, 0))
        # only move cursor the actual bytes in varlen
        self.moveCursor(varLen(var))
        return var


if __name__ == '__main__':

    import doctest
    doctest.testmod() # run test on inline examples first

    # import os, os.path, sys

    # # filesystem helpers
    # def datadir(fname):
    #     "returns the full path to fname in the importdata directory'"
    #     if __name__ == '__main__':
    #         filename = sys.argv[0]
    #     else:
    #         filename = __file__
    #     current_path = os.path.abspath(os.path.dirname(filename))
    #     parent_path = os.path.split(current_path)[0]
    #     return os.path.join(parent_path, fname)

    # test_file = datadir('tests/midifiles/minimal.mid')
    # fis = RawInstreamFile(test_file)
    # print ( fis.nextSlice(len(fis.data)) )

    # test_file = datadir('tests/midifiles/minimal-cubase-type0.mid')
    # with open(test_file, 'rb') as f:
    #     cubase_minimal = open(test_file, 'rb')
    #     fis2 = RawInstreamFile(cubase_minimal)
    #     print ( fis2.nextSlice(len(fis2.data)) )
    # # cubase_minimal.close()
