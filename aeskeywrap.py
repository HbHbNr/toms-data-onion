from Crypto.Cipher import AES

# GNU General Public License Version 3
#
# AES Key Wrap test vectors from https://tools.ietf.org/html/rfc3394

defaultiv = 'A6A6A6A6A6A6A6A6'

def wrap(kek, keydata):
    return wrapiv(kek, keydata, bytes.fromhex(defaultiv))

def wrapiv(kek, keydata, iv):
    return bytes()


def unwrap(kek, ciphertext):
    return unwrapiv(kek, ciphertext, bytes.fromhex(defaultiv))

def unwrapiv(kek, ciphertext, iv):
    if len(ciphertext) % 8 != 0:
        raise ValueError("Ciphertext must consist of blocks of 8 bytes each")
    if len(ciphertext) < 24:
        raise ValueError("Ciphertext must consist of at least 3 blocks of 8 bytes each")
    
    # lock parameters
    kek = bytes(kek)
    ciphertext = bytes(ciphertext)
    iv = bytes(iv)
    
    # initialize variables
    n = len(ciphertext) // 8 - 1
    R = []
    for i in range(n + 1):
        R.append(ciphertext[i * 8:i * 8 + 8])
    #print(' '.join(rhex(R)))
    
    # compute values
    ecb = AES.new(kek, AES.MODE_ECB)
    A = R[0]
    R[0] = bytes()
    #printstep(-1, A, R)
    for j in range(5, -1, -1):
        for i in range(n, 0, -1):
            t = n * j + i
            B = xor(A, t)
            B.extend(R[i])
            B = ecb.decrypt(bytes(B))
            A = bytes(B[0:8])
            R[i] = bytes(B[8:16])
            #printstep(t, A, R)
    
    # check validity
    if iv != A:
        raise ValueError('The provided iv {} does not match the calculated value {}'.format(iv.hex(), A.hex()))

    # output results
    keydata = bytearray()
    for i in range(1, len(R)):
        keydata.extend(R[i])
    
    return bytes(keydata)

def xor(A, t):
    t = int.to_bytes(t,len(A),'big')
    B = bytearray()
    
    for i in range(len(A)):
        B.append(A[i] ^ t[i])
    
    return B

def rhex(R):
    s = []
    for i in range(len(R)):
        s.append(R[i].hex())
    return s

def printstep(t, A, R):
    print(t, A.hex(), ' '.join(rhex(R)))