from Crypto.Cipher import AES

# GNU General Public License Version 3
#
# AES Known Answer Test Values from https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/block-ciphers#AES

kat = [('00000000000000000000000000000000', '00000000000000000000000000000000', '80000000000000000000000000000000', '3ad78e726c1ec02b7ebfe92b23d9ec34'),
       ('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', '00000000000000000000000000000000', '00000000000000000000000000000000', '4bf85f1b5d54adbc307b0a048389adcb')]

def test_knownanswertest():
    for (key, iv, plaintext, ciphertext) in kat:
        obj = AES.new(bytes.fromhex(key), AES.MODE_CBC, bytes.fromhex(iv))
        encryptedtexthex = obj.encrypt(bytes.fromhex(plaintext)).hex()
        assert encryptedtexthex == ciphertext
        obj = AES.new(bytes.fromhex(key), AES.MODE_ECB)
        encryptedtexthex = obj.encrypt(bytes.fromhex(plaintext)).hex()
        assert encryptedtexthex == ciphertext
