import pika

from rabbit_droppings.queue import _Queue


class _Rabbit:
    """A connection with a Rabbit server.

    Not for external use"""

    def __init__(self, config):
        """Create an instance given a _RabbitConfig"""
        self._config = config
        self._connected = False

    def is_connected(self):
        """Returns True if connected to the server"""
        return self._connected

    def connect(self):
        """Connect to the server.  Does nothing if already connected."""
        if self.is_connected():
            return
        params = pika.URLParameters(self._config.host)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._connected = True

    def disconnect(self):
        """Disconnect from to the server.  Does nothing if already disconnected."""
        if not self.is_connected():
            return
        self._connection.close()
        self._connected = False

    def queue(self, name):
        """Given a queue's name, return an instance of _Queue"""
        self.connect()
        return _Queue(self._channel, name)
