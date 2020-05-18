import requests

import os
import io
import sys
from datetime import datetime


RECIPIENT_VAR = 'EMAIL_ADDRESS'


def log_function(function):
    recipient = get_recipient()

    def log_function_wrapper(*args, **kwargs):
        # If recipient is not defined, just run the function
        if recipient == "":
            return function(*args, **kwargs)

        arguments = get_function_arguments(args, kwargs)

        subject = "Function '{}' execution log".format(function.__name__)

        text = "Function {}({}) finished its execution.\n\n".format(
            function.__name__, arguments)

        start_time = datetime.now()
        text += "Start time: {0:%b %d %H:%M:%S}\n".format(start_time)

        with CapturingOutput() as text_output:
            return_value = function(*args, **kwargs)

        if text_output:
            text += 'Function text output:\n'
            for op in text_output:
                print(op)
                text += op + '\n'
        else:
            text += 'No text output\n'

        text += 'Function returned: {}\n'.format(
            return_value) if return_value else 'No returned value\n'

        end_time = datetime.now()
        text += "End time: {0:%b %d %H:%M:%S}\n".format(end_time)

        total = (end_time - start_time).seconds
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        text += '\nTotal execution time: {0:02d}:{1:02d}:{2:02d}\n'.format(
            hours, minutes, seconds)

        send_email(recipient, text, subject)

        return return_value

    return log_function_wrapper


def send_email(recipient, text, subject):
    data = {
        "recipient": recipient,
        "text": text,
        "subject": subject
    }

    requests.post("https://arthur-email-bot.herokuapp.com/send", json=data)


def get_recipient():
    return os.environ.get(RECIPIENT_VAR) \
        if os.environ.get(RECIPIENT_VAR) \
        else input('{}: '.format(RECIPIENT_VAR))


def get_function_arguments(args, kwargs):
    args_repr = [repr(a) for a in args]
    kwargs_repr = ["{0}={1!r}".format(k, v) for k, v in kwargs.items()]
    arguments = ", ".join(args_repr + kwargs_repr)

    return arguments


class CapturingOutput(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
