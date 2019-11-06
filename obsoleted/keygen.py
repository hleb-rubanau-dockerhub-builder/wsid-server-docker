#!/usr/bin/env python3

import nacl.signing
import nacl.encoding

private_key = nacl.signing.SigningKey.generate()
private_key_hex = private_key.encode(encoder=nacl.encoding.HexEncoder).decode()
print(private_key_hex)
