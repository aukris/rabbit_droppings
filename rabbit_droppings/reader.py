import pickle

from message import Message


class Reader:
    """Read messages from some kind of input.  The messages should be
    in the format written by the Writer class."""

    def __init__(self, input):
        """Create an instance given a input.  The input should quack
        like a file, responding to readline() and close()."""
        self._input = input
        self.jobs_generator = (x for x in pickle.load(self._input))

    def close(self):
        """Close the reader.  Do not use after closing."""
        self._input.close()

    def read(self):
        """Read a Message"""
        try:
            attrs = self.jobs_generator.next()
            return Message(**attrs)
        except StopIteration:
            return None
