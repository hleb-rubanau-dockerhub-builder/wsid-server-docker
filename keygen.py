#!/usr/bin/env python3

from nacl.binding import crypto_sign_SEEDBYTES
import nacl.bindings
import nacl.c.crypto_box

signbytes=nacl.bindings.crypto_sign_SEEDBYTES
encbytes=nacl.c.crypto_box.SEEDBYTES

print("Signbytes=%s, encbytes=%s" % [ signbytes , encbytes ] )
