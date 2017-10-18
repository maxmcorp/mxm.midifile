Overall architecture
====================

Files overview.

**constants.py** contains all the midi constants used in the library.

**data_type_converters.py** contains all the functions that converts to the specific data types used in the midi format.

**raw_instream_file.py** and **raw_outstream_file.py** reads and writes python data to midi files. Using the type converters.

**MidiFileParser** does alle the parsing of the binary data, converts them to python data types and calls the related event handler.

**EventDispatcher** takes the general high level midi events and turns them into more fine grained events that are usable for triggering **MidiEvents** objects.

**MidiInFile** is just a small wrapper that glues the parser together with an event handler. Usually a subclass of **MidiEvents**.

**MidiEvents** is the basic event handler and data validation class. This is the center of mxm.midifile. You have to subclass it to get any real work done.

**MidiToCode** and **MidiOutFile** are both subclasses of **MidiEvents**. They implement their own version of the event handlers.