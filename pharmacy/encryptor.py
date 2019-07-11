# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import base64
import hashlib
import json
import urllib
from Crypto.Cipher import AES


# ### -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* ### #
# ###                                                        ### #
# ### ENCRYPTOR / DECRYPTOR                                  ### #
# ###                                                        ### #
# ### -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* ### #

ecela_kev = "4645d43f13b4d6d3"
ecela_iv = "2d6639b088097e39"

key = hashlib.sha1(ecela_kev).hexdigest()[0:16]  # 32bytes => 128bits
iv = ecela_iv[0:16]  # 32bytes forced


def encrypt_json(json_raw_data):

	data = json_raw_data
	jsondata = json.dumps(data)

	# PKCS#7 padding
	padding_len = 16 - (len(jsondata) % 16)
	jsondata += chr(padding_len) * padding_len

	cipher = AES.new(key, AES.MODE_CBC, iv)  # AES-128-CBC
	encrypted = cipher.encrypt(jsondata)

	coded = urllib.quote_plus(base64.b64encode(encrypted))

	return coded


def decrypt_json(json_enc_data):

	decoded = base64.b64decode(urllib.unquote_plus(json_enc_data))

	cipher = AES.new(key, AES.MODE_CBC, iv)
	decrypted = cipher.decrypt(decoded)

	# remove padding
	padding_len = ord(decrypted[-1])
	decrypted = decrypted[:-padding_len]

	recovered_data = json.loads(decrypted)

	return recovered_data
