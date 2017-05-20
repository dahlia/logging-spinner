import logging
import sys
import time

from logging_spinner import SpinnerHandler


logger = logging.getLogger('sample')


def sample_program(interval):
    l = logger.getChild('sample_program')

    l.info("Let's get started!", extra={'user_waiting': True})
    # The "user_waiting" extra field is used by logging-spinner.
    # "True" indicates a user need to wait until a process is finished.
    time.sleep(interval)  # Some time-taking process

    l.info("Still processing...", extra={'user_waiting': True})
    # Log records with {'user_waiting': True} can be continuous
    # in order to represent phase changes.
    time.sleep(interval)

    l.info("Done!", extra={'user_waiting': False})
    # Log records with {'user_waiting': False} indicates a time-taking process
    # is just finished so that a user don't have to wait now.

    # extra={'user_waiting': True}  -> show a spinner
    # extra={'user_waiting': False} -> hide a spinner


def main(stream=sys.stdout):
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 2

    # Setup a SpinnerHandler to application logger(s)
    handler = SpinnerHandler(stream=stream)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    sample_program(interval=interval)


if __name__ == '__main__':
    main()
