# -*- coding: utf-8 -*-
import base64

from Crypto.Cipher import AES
from ceca_pass import settings


class Cipher(object):

    def __init__(self, *args, **kwargs):
        self.block_size = 32
        self.padding = '{'
        self.pad = lambda s: s + \
            (self.block_size - len(s) % self.block_size) * self.padding
        self.cipher = AES.new(settings.CECA_PASS_SECRET_STRING)
        self.aes_prefix = kwargs.pop('aes_prefix', 'aes:')
        if not self.aes_prefix:
            raise ValueError('AES Prefix cannot be null.')
        super(Cipher, self).__init__(*args, **kwargs)

    def encode_aes(self, s):
        return base64.b64encode(self.cipher.encrypt(self.pad(s)))

    def decode_aes(self, s):
        return self.cipher.decrypt(base64.b64decode(s)).rstrip(self.padding)
