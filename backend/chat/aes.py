import binascii
from Crypto.Cipher import AES


KEY = 'This is a key123'
IV = 'This is an IV456'
MODE = AES.MODE_CFB
BLOCK_SIZE = 16
SEGMENT_SIZE = 128


def encrypt(key, iv, plaintext):
    aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
    plaintext = _pad_string(plaintext)
    encrypted_text = aes.encrypt(plaintext)
    return binascii.b2a_hex(encrypted_text).rstrip()


def decrypt(key, iv, encrypted_text):
    aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
    encrypted_text_bytes = binascii.a2b_hex(encrypted_text)
    decrypted_text = aes.decrypt(encrypted_text_bytes)
    decrypted_text = _unpad_string(decrypted_text)
    return decrypted_text


def _pad_string(value):
    length = len(value)
    pad_size = BLOCK_SIZE - (length % BLOCK_SIZE)
    return value.ljust(length + pad_size, '\x00')


def _unpad_string(value):
    while value[-1] == '\x00':
        value = value[:-1]
    return value


if __name__ == '__main__':
    input_plaintext = 'The answer is no'
    encrypted_text = encrypt(KEY, IV, input_plaintext)
    decrypted_text = decrypt(KEY, IV, encrypted_text)
    assert decrypted_text == input_plaintext