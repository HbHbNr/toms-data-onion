# GNU General Public License Version 3

def decrypt(decoded):
    # beginning of the text is known, leading to the first bytes of the key
    expectedstart = bytearray('==[ Layer 4/6: ', 'utf-8')
    xor = bytearray()

    for i in range(len(expectedstart)):
        x = expectedstart[i] ^ decoded[i]
        xor.append(x)

    # a) 15 * '=' must be in the encrypted text, because the line "==[ Payload ]==" contains 47 * '='.
    # b) Multiple occurences are possible, but hopefully in at least one case 17 more '=' will follow.
    # c) The last occurence is tried first, because that should be the "Payload"-line.
    tattletale = bytearray()
    for x in xor:
        tattletale.append(x ^ ord('='))
    xorfullstart = decoded.rfind(tattletale)

    # assumption/hope: the next 32 bytes are all encoded '='
    xorfull = bytearray()
    for d in decoded[xorfullstart:xorfullstart+32]:
        xorfull.append(d ^ ord('='))
    
    # decrypt the bytes with the assumed key
    decrypted = bytearray()
    for i in range(len(decoded)):
        decrypted.append(decoded[i] ^ xorfull[i % 32])

    return decrypted


if __name__ == '__main__':
    import ascii85

    payload = ascii85.loadpayload('layers/layer3.txt')
    decoded = ascii85.decode(payload)
    decoded = decrypt(decoded)
    print(decoded.decode()[0:500])
