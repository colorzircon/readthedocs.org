# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_ssh_pair_keys(key_size=2048, comment='support@readthedocs.com'):
    """Generate SSH Public/Private key."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=openssl.backend,
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    private_string = private_bytes.decode('utf8')

    public_string = generate_public_from_private_key(private_key)
    return private_string, public_string


def generate_public_from_private_key(private_key, text_format=False, comment='support@readthedocs.com'):
    # TODO: if the public key is generated from a private key, maybe we don't want to add a default message
    if text_format:
        private_key = serialization.load_pem_private_key(
            private_key.encode('utf8'),
            password=None,
            backend=openssl.backend,
        )

    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )
    public_string = '{key} {comment}'.format(
        key=public_bytes.decode('utf8'),
        comment=comment,
    )
    return public_string


def is_valid_private_key(key_text):
    try:
        private_key = serialization.load_pem_private_key(
            key_text.encode('utf8'),
            password=None,
            backend=openssl.backend,
        )
        return True
    except TypeError:
        return False
