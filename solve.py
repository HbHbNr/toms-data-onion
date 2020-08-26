import ascii85

# GNU General Public License Version 3

def dumpexcerpt(fulltext, frombegin, fromend):
    fulltextlength = len(fulltext)
    print(str(fulltextlength) + ' characters of fulltext found')
    print('first ' + str(frombegin) + ': ' + fulltext[0:frombegin])
    print(' last ' + str(fromend) + ': ' + fulltext[fulltextlength - fromend:fulltextlength])

def writetofile(filename, data):
    f = open(filename, 'w', encoding='utf-8')
    f.write(data)
    f.close()

def layer1bitmod(decoded):
    decoded2 = bytearray()
    for c in decoded:
      c ^= 0b01010101
      last = c & 1
      c >>= 1
      c |= (last << 7)
      decoded2.append(c)
    return decoded2

def layer2parityvalid(i):
    amountofones = 0
    for e in range(8):
        amountofones += (i & (2 ** e)) != 0
        #print(amountofones)
    return (amountofones & 1) == 0

def layer2filtervalid(payload):
    valid = bytearray()
    for c in payload:
        if(layer2parityvalid(c)):
            valid.append(c >> 1)

    merged = []
    currentsum = 0
    i = 0
    while i < len(valid):
        ii = i % 8
        currentsum |= valid[i] << ((7 - ii) * 7)
        if ii == 7:
            merged.append(currentsum)
            currentsum = 0
        i += 1

    divided = bytearray()
    for i in merged:
        for ii in range(7):
            divided.append((i >> ((6 - ii) * 8)) & 255)
    return divided

def layer3decrypt(decoded):
    # as found by layer3.py:
    xorfull = bytearray(b'l$\x84\x8eB\x19\xa8\xe1\xc5\xdbWe\xb9\xc6\x14\x9e\xa5\x195\x96;9\x7f\xa5e\xd1\xfe\x01\x85}\xd9L')
    for i in range(len(decoded)):
        decoded[i] ^= xorfull[i % 32]
    return(decoded)

for layer in [3]:
    inputfile = 'layers/layer' + str(layer) + '.txt'
    outputfile = 'layers/layer' + str(layer + 1) + '.txt'

    payload = ascii85.loadpayload(inputfile)
    dumpexcerpt(payload, 20, 20)
    decoded = ascii85.decode(payload)
    if layer == 1:
        decoded = layer1bitmod(decoded)
    elif layer == 2:
        decoded = layer2filtervalid(decoded)
    elif layer == 3:
        decoded = layer3decrypt(decoded)
    #print(decoded[0:100].decode())
    #quit()
    dumpexcerpt(decoded.decode(), 200, 200)

    writetofile(outputfile, decoded.decode())
