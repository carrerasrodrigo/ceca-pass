import os

from django.conf import settings


def get_value(name, default=None):
    """
        First we lookup into the settings, if its not found we lookup into
        the env variables and finally we use a default value.
    """
    value = getattr(settings, name, None)
    if value is None:
        value = os.environ.get(name, None)
    return default if value is None else value

CECA_PASS_SECRET_STRING = get_value('CECA_PASS_SECRET_STRING')
CECA_PASS_PASSWORD_PATH = get_value('CECA_PASS_PASSWORD_PATH',
    os.path.join(os.path.expanduser("~"), '.ceca_pass', 'dump.json'))
CECA_PASS_BASH_PATH = get_value('CECA_PASS_BASH_PATH',
    os.path.join(os.path.expanduser("~"), '.ceca_pass', 'ceca_bash.rc'))
CECA_PASS_SYSTEM_BASH_FILE = get_value('CECA_PASS_SYSTEM_BASH_FILE',
    os.path.join(os.path.expanduser("~"), '.bashrc'))
