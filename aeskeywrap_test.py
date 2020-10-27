from Crypto.Cipher import AES
import aeskeywrap

# GNU General Public License Version 3
#
# AES Key Wrap test vectors from https://tools.ietf.org/html/rfc3394

defaultiv = 'A6A6A6A6A6A6A6A6'
testvectors = [('000102030405060708090A0B0C0D0E0F',
                '00112233445566778899AABBCCDDEEFF',
                defaultiv,
                '1FA68B0A8112B447AEF34BD8FB5A7B829D3E862371D2CFE5'),
               ('000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F',
                '00112233445566778899AABBCCDDEEFF000102030405060708090A0B0C0D0E0F',
                defaultiv,
                '28C9F404C4B810F4CBCCB35CFB87F8263F5786E2D80ED326CBC7F0E71A99F43BFB988B9B7A02DD21')]

def test_unwrap():
    for (kek, keydata, iv, ciphertext) in testvectors:
        decryptedtext = aeskeywrap.unwrapiv(bytes.fromhex(kek), bytes.fromhex(ciphertext), bytes.fromhex(iv))
        assert bytes.fromhex(keydata) == decryptedtext

if __name__ == '__main__':
    test_unwrap()
