from __future__ import print_function
import pickle


class Writer:
    """Writes message to some kind of output.  The messages are written
    in a format that the Reader class can read."""

    def __init__(self, output):
        """Create an instance given an output.  The output should
        quack like a file, responding to write(), flush() and close()"""
        self._output = output
        self.array_of_jobs = []

    def write(self, message, flush=True):
        """Write a message to the output.  Flushes automatically, unless
        the flush option is False."""
        message = message.to_message()
        attrs = message.attrs()
        self.array_of_jobs.append(attrs)
        self._output.seek(0)
        pickle.dump(self.array_of_jobs, self._output)
        if flush:
            self.flush()

    def flush(self):
        """Flush the output, ensuring that all messages have been written"""
        self._output.flush()
        return self.array_of_jobs

    def close(self):
        """Close the output.  Do not use after closing."""
        self._output.close()
