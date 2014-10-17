import json
import os

from ceca_pass import settings
from ceca_pass.cipher import Cipher
from ceca_pass.helpers import dump_to_json, dump_to_bash, patch_bash_file, \
    get_password, json_date_hook, json_encode_datetime
from ceca_pass.models import Password, Project
from django.test import TestCase
from django.utils.timezone import now as utcnow, timedelta


class TestCase(TestCase):
    def setUp(self):
        if os.path.isfile(settings.CECA_PASS_PASSWORD_PATH):
            os.remove(settings.CECA_PASS_PASSWORD_PATH)

        if os.path.isfile(settings.CECA_PASS_BASH_PATH):
            os.remove(settings.CECA_PASS_BASH_PATH)

        if os.path.isfile(settings.CECA_PASS_BASH_PATH):
            os.remove(settings.CECA_PASS_BASH_PATH)

    def test_env_name(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')
        p2 = Password.objects.create(project=project, name='pass2',
            variable_name='123abc_ 1%^1', password='hello')

        self.assertEqual(p.env_name, 'PV_PASSV')
        self.assertEqual(p2.env_name, 'PV_123ABC__11')

    def test_password_field(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')

        self.assertEqual(p.password, 'hello')

    def test_password_field2(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')
        p = Password.objects.filter()[0]
        self.assertEqual(p.password, 'hello')

    def test_dump_json(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')
        p2 = Password.objects.create(project=project, name='pass2',
            variable_name='123abc_ 1%^1', password='hello')
        dump_to_json()

        with open(settings.CECA_PASS_PASSWORD_PATH) as f:
            cipher = Cipher()
            js = json.loads(cipher.decode_aes(f.read()),
                object_hook=json_date_hook)

        self.assertEqual(
            js['data'][project.variable_name][p.variable_name]['password'],
            p.password)
        self.assertEqual(
            js['data'][project.variable_name][p2.variable_name]['password'],
            p2.password)

    def test_dump_json_expired_date(self):
        with open(settings.CECA_PASS_PASSWORD_PATH, 'w') as f:
            s = '{"version": "0", "data": {"pv": {"passv": {"password": \
                "hello", "expire": "%s"}}}}' % \
                (utcnow()-timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

            cipher = Cipher()
            f.write(
                json.dumps(cipher.encode_aes(s),
                default=json_encode_datetime))

        self.assertEqual(get_password('pv', 'passv'), None)

    def test_dump_json_get_password(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')
        p2 = Password.objects.create(project=project, name='pass2',
            variable_name='123abc_ 1%^1', password='hello')
        dump_to_json()

        self.assertEqual(get_password(project.variable_name, p.variable_name),
            p.password)
        self.assertEqual(get_password(project.variable_name, p2.variable_name),
            p2.password)
        self.assertEqual(get_password('false', 'false'), None)

    def test_no_dump_json_get_password(self):
        self.assertRaises(Exception, get_password, ('', ''))

    def test_dump_to_bash(self):
        project = Project.objects.create(name='p', variable_name='pv')
        p = Password.objects.create(project=project, name='pass',
            variable_name='passv', password='hello')
        p2 = Password.objects.create(project=project, name='pass2',
            variable_name='123abc_ 1%^1', password='hello')
        dump_to_bash()

        with open(settings.CECA_PASS_BASH_PATH) as f:
            txt = f.read()

        self.assertIn('export {0}={1}'.format(p.env_name, p.password), txt)
        self.assertIn('export {0}={1}'.format(p2.env_name, p2.password), txt)

    def test_patch_bash_file(self):
        with open(settings.CECA_PASS_SYSTEM_BASH_FILE, 'w') as f:
            f.write('hello\n')

        patch_bash_file()

        with open(settings.CECA_PASS_SYSTEM_BASH_FILE) as f:
            txt = f.read()
        txt2 = '# ceca_pass config\nsource {0}' \
            .format(settings.CECA_PASS_BASH_PATH)
        self.assertIn(txt2, txt)
        self.assertIn('hello\n', txt)

    def test_re_patch_bash_file(self):
        with open(settings.CECA_PASS_SYSTEM_BASH_FILE, 'w') as f:
            f.write('hello\n')

        patch_bash_file()
        patch_bash_file()

        with open(settings.CECA_PASS_SYSTEM_BASH_FILE) as f:
            txt = f.read()
        txt2 = '# ceca_pass config\nsource {0}' \
            .format(settings.CECA_PASS_BASH_PATH)
        self.assertEqual(len(txt.split(txt2)), 2)
        self.assertIn('hello\n', txt)
