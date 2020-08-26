import ascii85

payload = ascii85.loadpayload('layers/layer3.txt')
decoded = ascii85.decode(payload)

expectedstart = bytearray('==[ Layer 4/6: ', 'utf-8')
xor = bytearray()
print(expectedstart)
print(decoded[0:len(expectedstart)])

# find first len(expected) bytes of key
for i in range(len(expectedstart)):
    x = expectedstart[i] ^ decoded[i]
    xor.append(x)

# verify xor
print(xor)
#for i in range(len(xor)):
#    print(chr(xor[i] ^ decoded[i]))

# a) 15 * '=' must be in the crypted text, because the line "==[ Payload ]==" contains 47 * '='.
# b) Multiple occurences are possible, but hopefully in at least one case 17 * '=' follow.
# c) We try the last occurence first, because that should be the "Payload"-line.

tattletale = bytearray()
for x in xor:
    t = x ^ ord('=')
    tattletale.append(t)

# verify tattletale
#print(tattletale)
#for i in range(len(tattletale)):
#    print(chr(xor[i] ^ tattletale[i]))

xorfullstart = decoded.rfind(tattletale)
print(xorfullstart)
# last occurance found at: 3488 (correct)
print(decoded[xorfullstart:xorfullstart+32])

xorfull = bytearray()
for d in decoded[xorfullstart:xorfullstart+32]:
    x = d ^ ord('=')
    xorfull.append(x)
print(xorfull)
print(list(xorfull))
xorfull = bytearray(b'l$\x84\x8eB\x19\xa8\xe1\xc5\xdbWe\xb9\xc6\x14\x9e\xa5\x195\x96;9\x7f\xa5e\xd1\xfe\x01\x85}\xd9L')

for i in range(xorfullstart - 10 * 32, xorfullstart + 10 * 32):
    print(chr(decoded[i] ^ xorfull[i % 32]), end='')
    if i % 32 == 31:
        print('|', end='')
