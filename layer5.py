# GNU General Public License Version 3

if __name__ == '__main__':
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
    import ascii85, aeskeywrap

    payload = ascii85.loadpayload('layers/layer5.txt')
    decoded = ascii85.decode(payload)
    
    kek = decoded[0:32]
    kekiv = decoded[32:40]
    wrappedkey = decoded[40:80]
    payloadiv = decoded[80:96]
    encryptedpayload = decoded[96:len(decoded)]
    print(len(encryptedpayload))
    
    print(wrappedkey.hex())
    
    payloadkey = aeskeywrap.unwrapiv(kek, wrappedkey, kekiv)
    print(payloadkey.hex())
    
    print('kek', len(kek))
    print('kekiv', len(kekiv))
    print('wrappedkey', len(wrappedkey))
    print('payloadiv', len(payloadiv))
    print('encryptedpayload', len(encryptedpayload))
    print('payloadkey', len(payloadkey))
    
    print(payloadiv.hex())
    counter = Counter.new(len(payloadiv)*8, initial_value=int.from_bytes(payloadiv, 'big'), allow_wraparound=False)
    
    # test: dump the counter values
    #print('call counter:')
    #print(counter().hex());
    #print(counter().hex());
    #print(counter().hex());
    #print(counter().hex());
    #print(counter().hex());
    
    ctr = AES.new(payloadkey, AES.MODE_CTR, counter=counter)
    decryptedpayload = ctr.decrypt(bytes(encryptedpayload))
    
    # first 200 bytes
    print(decryptedpayload[0:200].decode())
    # all bytes
    print(decryptedpayload.decode())
