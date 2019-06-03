This is a Python library and utilities for saving and loading RabbitMQ
messages to and from disk.

Why?
====

-  A program cannot publish a message to RabbitMQ, but does not want to
   lose the message. Using this library, the program can save the
   message to a file. Later, after fixing the problem, a person can use
   a utility in this package to publish the message.

-  The consumer has a bug and messages are piling up in a queue. You
   have fixed the bug and your tests seem to indicate the consumer will
   now work, but you want some insurance. Using a program in this
   package, you can back up the queue to a file. If the program
   processes the messages incorrectly, you can use use a program in this
   package to restore the queue from the file.

-  You want to edit messages in a queue. You can dump the queue to a
   file, use a text editor or a one-off program to change the file, and
   then write the messages back into the queue.

Why not?
========

This library is brand new and has not been battle tested. Proceed with
caution.

Backup format
=============

Queues are backed up and restored from text files containing json. Each
line in the file is a JSON dictionary with this structure:

::

    {
        "body": "This is a test",
        "delivery_info": {
            "delivery_tag": 1
        },
        "properties": {
            "app_id": null,
            "cluster_id": null,
            "content_encoding": null,
            "content_type": "text/plain",
            "correlation_id": null,
            "delivery_mode": 2,
            "expiration": null,
            "headers": {
                "client_id": null,
                "host_ip": "10.0.0.15",
                "host_name": "treebeard",
                "library_id": "olio_msg (Python) 1.9.0",
                "metadata_version": "1.0.0",
                "program_name": "olio_msg_send_test_messages",
                "version": "1.0.0"
            },
            "message_id": "1df3eb23ffeb476b8355d87b475eb627",
            "priority": null,
            "reply_to": null,
            "timestamp": 1434644774,
            "type": "test",
            "user_id": null
        }
    }

The line was shown pretty-printed, but it's actually just one line:

::

    {"body": "This is a test", "delivery_info": {...}, "properties: {...}}

Using the command-line utilities
================================

To remove a celery task

::

   rabbit_droppings --host localhost --queue jobs \
      --file /path/to/save/file -remove 'users.tasks.reindex'

To backup a queue

::

    rabbit_droppings --host localhost --queue jobs \
      --file /path/to/save/file --dump

To backup and purge a queue

::

    rabbit_droppings --host localhost --queue jobs \
      --file /path/to/save/file --purge

To restore a queue

::

    rabbit_droppings --host localhost --queue jobs \
      --file /path/to/save/file --restore

Saving a message with the pika library
======================================

If you have a program using the pika library to publish messages to a
RabbitMQ server, here's how to save messages that could not be
published:

First, import the library:

::

    import rabbit_droppings

If you have a program that needs to save messages that cannot be
published using the pika library, it should create a
rabbit\_droppings.Writer (probably in the constructor):

::

    file = open('/path/to/my/file', 'a')
    self._rd_writer = rabbit_droppings.Writer(file)

When you publish a message and a pika exception occurs, save the
message:

::

    body = "Message body"
    properties = pika.spec.BasicProperties(
        content_type='text/plain'
        )
    try:
        channel.basic_publish(exchange='',
                              routing_key='some_queue_name',
                              properties=properties,
                              body=body)
    except (pika.exceptions.AMQPError, pika.exceptions.ChannelError) as e:
        pika_message = rabbit_droppings.PikaMessage(body, properties=properties)
        self._rd_writer.write(pika_message)

Versioning
==========

This library practices `Semantic Versioning <http://semver.org/>`_.

This library is currently in alpha; it's versions look like "0.1.0",
"0.2.0", etc. There are no guarantees with alpha versions: Any version
bump could be any combination of bug fix, backwards compatible API
change, or breaking API change.

When the library becomes stable, its version number will be bumped to
"1.0.0". Semantic versioning makes these promises for stable versions:

-  A patch-level version bump (e.g. "1.0.0" to "1.0.1") does not change
   the public API.

-  A minor-level version bump (e.g. "1.0.0" to "1.1.0") changes the
   public API in a backward-compatible manner.

-  A major-level version bump (e.g. "1.0.0" to "2.0.0") changes the
   public API in some way that is not backward compatible.

Python version
==============

Known to work with Python versions:

-  2.6.9
-  2.7.9

Development
===========

Running the tests requires a RabbitMQ server installed locally. The
tests are known to pass with these RabbitMQ versions:

-  3.4.1

To run the tests:

::

    ./setup.py test

Working with the pypi test server
---------------------------------

To register (only once):

::

    python setup.py register -r https://testpypi.python.org/pypi

To publish to the pypi test server:

::

    python setup.py bdist_wheel upload -r pypitest
    python setup.py sdist upload -r pypitest

To install from the pypi test server:

::

    pip install -i https://testpypi.python.org/pypi rabbit_droppings

Working with the "real" pypi server
-----------------------------------

To register (only once):

::

    python setup.py register -r https://pypi.python.org/pypi

To publish to the "real" pypi server:

::

    python setup.py bdist_wheel upload -r pypi
    python setup.py sdist upload -r pypi

To install from the "real" pypi server:

::

    pip install -i https://pypi.python.org/pypi rabbit_droppings
