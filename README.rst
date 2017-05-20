logging-spinner: non-intrusive spinner for Python
=================================================

.. image:: https://travis-ci.org/dahlia/logging-spinner.svg
   :alt: Build Status
   :target: https://travis-ci.org/dahlia/logging-spinner

.. image:: sample.gif
   :alt: Demo session

This library helps to display loading spinners in CLI in non-intrusive manner.
Applications/libraries don't have to depend on any third-party API, but only
need to log loading messages through Python's standard ``logging`` library:

.. code-block:: python

   logger = logging.getLogger('myapp.logger')
   logger.info('Loading data...', extra={'user_waiting': True})
   # some long taking process goes here...
   logger.info('Finished loading!', extra={'user_waiting': False})

At the outest code of the application, setup a ``SpinnerHandler``:

.. code-block:: python

   from logging_spinner import SpinnerHandler

   logger = logging.getLogger('myapp')
   logger.setLevel(logging.INFO)
   logger.addHandler(SpinnerHandler())

``SpinnerHandler`` is only aware of log records with ``user_waiting`` extra
field and displays them with a spinner.

See also :file:`sample.py` code.
