from pika_message import PikaMessage
from rabbit_droppings import Message

from reader import Reader


class _Queue:
    """A RabbitMQ queue.

    Not for external use."""

    def __init__(self, channel, name):
        """Create an instance given a pika.Channel and the queue's name."""
        self._channel = channel
        self.name = name
        self.jobs_array = []

    def read(self):
        """Read and return a Message, or None if the queue is empty.

        The message will not be removed from the queue until it is given to
        the ack method.
        
        Returns: [Message, None]
        """
        method_frame, header_frame, body = self._channel.basic_get(self.name)
        if method_frame:
            pika_message = PikaMessage(body,
                                       delivery_info=method_frame,
                                       properties=header_frame,
                                       )
            return pika_message.to_message()
        else:
            return None

    def ack(self, message, multiple=False):
        """Acknowledge a message.

        Args:
          message [Message]
          multiple [bool] If true, all outstanding messages up to and
            including this message are acknowledged.
        """
        delivery_tag = message.delivery_info["delivery_tag"]
        self._channel.basic_ack(delivery_tag, multiple=multiple)

    def nack(self, message, multiple=False):
        """Negative-acknowledge a message.

        Args:
          message [Message]
          multiple [bool] If true, all outstanding messages up to and
            including this message are acknowledged.
        """
        delivery_tag = message.delivery_info["delivery_tag"]
        self._channel.basic_nack(delivery_tag, multiple=multiple)

    def publish(self, message):
        """Publish a message to the queue.
        
        Args:
          message [Message]
        """
        pika_message = message.to_pika_message()
        self._channel.basic_publish(exchange='',
                                    routing_key=self.name,
                                    properties=pika_message.properties,
                                    body=message.body)

    def dump(self, writer, destructive=False):
        """Dump the queue to a Writer."""
        last_msg_written = None
        while True:
            msg = self.read()
            if msg is None:
                break
            writer.write(msg, flush=False)
            last_msg_written = msg
            self.jobs_array = writer.flush()

        if last_msg_written is not None:
            if destructive:
                self.ack(last_msg_written, multiple=True)
            else:
                self.nack(last_msg_written, multiple=True)

    def restore(self, reader):
        """Restore a queue from a message reader.  This publishes to the queue
        any messages returned by the reader.  Any existing messages in the queue will
        still be in the queue.

        Args:
          path [str] The path of the file
        """
        while True:
            msg = reader.read()
            if msg is None:
                break
            self.publish(msg)

    def restore_excluding_job(self, job_id):
        total_jobs_count = len(self.jobs_array)
        for x in self.jobs_array:
            print (x['properties']['headers']['task'] )
        priority_jobs_array = filter(lambda x: x['properties']['headers']['task'] != job_id, self.jobs_array)
        priority_jobs_count = len(priority_jobs_array)

        while True:
            input = raw_input('Would you like to remove %d of the total %d jobs...'
                              'You can always restore it later form the file  (Y/N)   ' % (
                                total_jobs_count - priority_jobs_count, total_jobs_count))
            if input == 'Y' or input == 'y' or input == 'yes':
                break
            elif input == 'N' or input == 'n' or input == 'no':
                return None

        for attrs in priority_jobs_array:
            self.publish(Message(**attrs))
