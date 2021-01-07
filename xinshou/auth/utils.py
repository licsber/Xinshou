import base64
import random

from Crypto.Cipher import AES


def pad(s: bytes, block_size: int) -> bytes:
    l = len(s)
    pad_num = block_size - (l % block_size)
    if pad_num == 0:
        pad_num = block_size
    pad_b = bytes([pad_num])
    return s + pad_b * pad_num


def aes_encrypt(s: str, key: str, iv='\0' * 16, coding='utf-8') -> str:
    key_b = key.encode(coding)
    iv_b = iv.encode(coding)
    raw_b = s.encode(coding)

    cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
    padded = pad(raw_b, AES.block_size)
    encrypted = cipher.encrypt(padded)
    encoded = base64.b64encode(encrypted)
    return encoded.decode(coding)


def encrypt(pwd, salt):
    charsets = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    rnd_16 = ''.join(random.choice(charsets) for _ in range(16))
    rnd_64 = ''.join(random.choice(charsets) for _ in range(64))
    return aes_encrypt(rnd_64 + pwd, salt, rnd_16)
