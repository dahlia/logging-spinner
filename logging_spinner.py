import io
import logging
import sys
import threading

from pyspin.spin import Default, Spinner

__all__ = 'SpinnerHandler',
__version__ = '0.1.0'


class SpinnerHandler(logging.Handler):

    def __init__(self,
                 stream=None,
                 spin_style=Default,
                 spin_interval=0.1,
                 format=u'{spinner} {message}',
                 level=logging.NOTSET):
        super(SpinnerHandler, self).__init__(level)
        self._stream = stream
        self._current_record_changed = threading.Condition()
        self._thread = threading.Thread(target=self._display, kwargs={
            'format': format,
            'spinner': Spinner(spin_style),
            'spin_interval': spin_interval,
        })
        self._current_record = None

    def filter(self, record):
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

    def _display(self, format, spinner, spin_interval):
        stream, _ = self.get_stream()
        format_message = format.format
        format_line = u'\r{0:{1}}\r'.format
        previous_line_length = 0
        while True:
            record = self._current_record
            if record is None or not record.user_waiting:
                break
            s = format_message(spinner=spinner.next(),
                               record=record,
                               message=record.getMessage())
            stream.write(format_line(s, previous_line_length or 1))
            previous_line_length = len(s)
            stream.flush()
            with self._current_record_changed:
                self._current_record_changed.wait(spin_interval)
        s = self._current_record.getMessage()
        stream.write(u'\r{0:{1}}\n'.format(s, previous_line_length))
        stream.flush()
