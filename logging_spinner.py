import io
import logging
import sys
import threading

from pyspin.spin import Default, Spinner

__all__ = 'SpinnerHandler', 'UserWaitingFilter'
__version__ = '0.2.2'


class SpinnerHandler(logging.Handler):

    def __init__(self,
                 stream=None,
                 spin_style=Default,
                 spin_interval=0.1,
                 format=u'{spinner} {message}',
                 level=logging.NOTSET):
        super(SpinnerHandler, self).__init__(level)
        self._stream = stream
        self._message_format = format
        self._spinner = Spinner(spin_style)
        self._spin_interval = spin_interval
        self._current_record_changed = threading.Condition()
        self._thread = threading.Thread(target=self._display)
        self._current_record = None

    @staticmethod
    def filter(record):
        return hasattr(record, 'user_waiting')

    def get_stream(self):
        stream = sys.stdout if self._stream is None else self._stream
        if callable(getattr(stream, 'isatty')):
            atty = stream.isatty()
        else:
            atty = False
        try:
            stream.write('')
        except TypeError:
            stream = io.TextIOWrapper(stream)
        return stream, atty

    def emit(self, record):
        if not self.filter(record):
            return
        stream, atty = self.get_stream()
        if not atty:
            stream.write(record.getMessage() + '\n')
            return
        with self._current_record_changed:
            self._current_record = record
            self._current_record_changed.notify()
        if not self._thread.is_alive():
            self._thread.start()

    def _display(self):
        stream, _ = self.get_stream()
        format_message = self._message_format.format
        format_line = u'\r{0:{1}}\r'.format
        previous_line_length = 0
        while True:
            record = self._current_record
            if record is None or not record.user_waiting:
                break
            s = format_message(spinner=self._spinner.next(),
                               record=record,
                               message=record.getMessage())
            stream.write(format_line(s, previous_line_length or 1))
            previous_line_length = len(s)
            stream.flush()
            with self._current_record_changed:
                self._current_record_changed.wait(self._spin_interval)
        s = self._current_record.getMessage()
        stream.write(u'\r{0:{1}}\n'.format(s, previous_line_length or 1))
        stream.flush()
        self._thread = threading.Thread(target=self._display)


class UserWaitingFilter(logging.Filter):
    """Logging filter to avoid duplicate message prints of a log record
    with ``user_waiting`` extra field.  If a ``SpinnerHandler`` and
    a ``StreamHandler`` are both installed to one logger at a time
    the ``StreamHandler`` need to ``addFilter()`` this.

    """

    def filter(self, record):
        return not SpinnerHandler.filter(record)
