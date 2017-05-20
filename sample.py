import logging
import sys
import time

from logging_spinner import SpinnerHandler


logger = logging.getLogger('sample')


def sample_program(interval):
    l = logger.getChild('sample_program')
    l.info("Let's get started!", extra={'user_waiting': True})
    time.sleep(interval)
    l.info("Still processing...", extra={'user_waiting': True})
    time.sleep(interval)
    l.info("Done!", extra={'user_waiting': False})


def main(stream=sys.stdout):
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 2
    logger.setLevel(logging.INFO)
    handler = SpinnerHandler(stream=stream)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    sample_program(interval=interval)


if __name__ == '__main__':
    main()
