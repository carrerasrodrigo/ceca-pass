# -*- coding: utf-8 -*-
import string

from ceca_pass.cipher import Cipher
from django.contrib.auth.models import User
from django.db import models


class AESField(Cipher, models.CharField):

    __metaclass__ = models.SubfieldBase

    def get_prep_lookup(self, type, value):
        raise Exception('You cannot do lookups on an encrypted field.')

    def get_db_prep_lookup(self, *args, **kw):
        raise Exception('You cannot do lookups on an encrypted field.')

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and value is not None:
            return u'{0}{1}'.format(self.aes_prefix, self.encode_aes(value))
        return value

    def to_python(self, value):
        if value is None or not value.startswith(self.aes_prefix):
            return value
        return self.decode_aes(value[len(self.aes_prefix):])


class Project(models.Model):
    name = models.CharField(max_length=250)
    variable_name = models.CharField(max_length=250)

    class Meta:
        app_label = 'ceca_pass'

    def __unicode__(self):
        return self.name


class Password(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=250)
    variable_name = models.CharField(max_length=250)
    password = AESField(max_length=500)
    last_update_datetime = models.DateTimeField(auto_now_add=True)
    last_update_user = models.ForeignKey(User, null=True, blank=True,
        related_name='userr')
    expire = models.BooleanField(default=False)
    datetime_expire = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'ceca_pass'
        unique_together = ('project', 'name')

    def __unicode__(self):
        return self.name

    @property
    def env_name(self):
        valid_str = string.ascii_uppercase + '_' + string.digits
        name = u'{0}_{1}'.format(self.project.variable_name,
                self.variable_name).replace(' ', '_').upper()
        return ''.join(filter(lambda x: x in valid_str, name))
