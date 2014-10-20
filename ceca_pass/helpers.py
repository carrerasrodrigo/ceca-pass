import json
import os
import datetime

from ceca_pass import settings
from ceca_pass.models import Password
from ceca_pass.version import version
from ceca_pass.cipher import Cipher
from django.db.models import Q
from django.utils.timezone import now as utcnow


def json_date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = \
                datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except:
            pass
    return json_dict


def json_encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    raise TypeError(repr(obj) + " is not JSON serializable")


def dump_to_json():
    passwords = Password.objects.filter(Q(expire=False) |
        (Q(expire=True) & Q(datetime_expire__gte=utcnow())))

    d = {}
    for p in passwords:
        if p.project.variable_name not in d:
            d[p.project.variable_name] = {}
        d[p.project.variable_name][p.variable_name] = \
            dict(password=p.password, expire=p.datetime_expire)

    d = dict(data=d, version=version)
    if not os.path.exists(os.path.dirname(settings.CECA_PASS_PASSWORD_PATH)):
        os.makedirs(os.path.dirname(settings.CECA_PASS_PASSWORD_PATH))

    with open(settings.CECA_PASS_PASSWORD_PATH, 'w') as f:
        os.chmod(settings.CECA_PASS_PASSWORD_PATH, 400)
        cipher = Cipher()
        f.write(cipher.encode_aes(json.dumps(d, default=json_encode_datetime)))


def get_password(project_name, var_name):
    if not (os.path.exists(settings.CECA_PASS_PASSWORD_PATH) and
            os.path.isfile(settings.CECA_PASS_PASSWORD_PATH)):
        raise Exception('You have to do a dump_to_bash command first')

    with open(settings.CECA_PASS_PASSWORD_PATH, 'rb') as f:
        cipher = Cipher()
        js = json.loads(cipher.decode_aes(f.read()),
            object_hook=json_date_hook)

    try:
        if js['data'][project_name][var_name]['expire'] is None or \
                js['data'][project_name][var_name]['expire'] >= utcnow():
            return js['data'][project_name][var_name]['password']
    except KeyError:
        pass
    return None


def dump_to_bash():
    passwords = Password.objects.filter(Q(expire=False) |
        (Q(expire=True) & Q(datetime_expire__gte=utcnow())))

    data = u''
    for p in passwords:
        data += u'export {0}={1}\n'.format(p.env_name, p.password)

    if not os.path.exists(os.path.dirname(settings.CECA_PASS_BASH_PATH)):
        os.makedirs(os.path.dirname(settings.CECA_PASS_BASH_PATH))

    with open(settings.CECA_PASS_BASH_PATH, 'w') as f:
        os.chmod(settings.CECA_PASS_BASH_PATH, 400)
        f.write(data)


def patch_bash_file():
    with open(settings.CECA_PASS_SYSTEM_BASH_FILE, 'r') as f:
        content = f.read()

    if settings.CECA_PASS_BASH_PATH not in content:
        with open(settings.CECA_PASS_SYSTEM_BASH_FILE, 'a') as f:
            txt = '# ceca_pass config\nsource {0}'\
                .format(settings.CECA_PASS_BASH_PATH)
            f.write(txt)
