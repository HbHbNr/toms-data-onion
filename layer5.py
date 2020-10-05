# GNU General Public License Version 3

if __name__ == '__main__':
    import ascii85, aeskeywrap

    payload = ascii85.loadpayload('layers/layer5.txt')
    decoded = ascii85.decode(payload)
    
    kek = decoded[0:32]
    kekiv = decoded[32:40]
    wrappedkey = decoded[40:80]
    payloadiv = decoded[80:96]
    encryptedpayload = decoded[96:len(decoded)]
    
    print(wrappedkey.hex())
    
    payloadkey = aeskeywrap.unwrapiv(kek, wrappedkey, kekiv)
    print(payloadkey.hex())
