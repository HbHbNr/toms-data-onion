import fileinput
import ascii85

# GNU General Public License Version 3

def loadpayload(inputfile):
    payloadmarkerfound = False
    payload = []
    for line in fileinput.input(inputfile):
        if not payloadmarkerfound and line.startswith('<~'):
            payloadmarkerfound = True
        if payloadmarkerfound:
            line = line.strip()
            payload.append(line)
    return ''.join(payload)

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
    decoded2 = []
    for i in range(len(decoded)):
      c = ord(decoded[i])
      c ^= 0b01010101
      last = c & 1
      c >>= 1
      c |= (last << 7)
      decoded2.append(chr(c))
    return ''.join(decoded2)

def layer2parityvalid(i):
    amountofones = 0
    for e in range(8):
        amountofones += (i & (2 ** e)) != 0
        #print(amountofones)
    return (amountofones & 1) == 0

def layer2filtervalid(payload):
    valid = []
    for i in range(len(payload)):
        c = ord(payload[i])
        if(layer2parityvalid(c)):
            valid.append(c)

    merged = []
    currentsum = 0
    i = 0
    while i < len(valid):
        currentsum <<= 7
        currentsum |= valid[i] >> 1
        if (i % 8) == 7:
            merged.append(currentsum)
            currentsum = 0
        i += 1

    divided = []
    for ii in merged:
        for i in range(7):
            divided.append(chr((ii >> (i * 8)) & 255))
    return ''.join(divided)

inputfile = 'layers/layer2.txt'

payload = loadpayload(inputfile)
dumpexcerpt(payload, 20, 20)
decoded = ascii85.decode(payload)
dumpexcerpt(decoded, 20, 20)
#decoded = layer1bitmod(decoded)
decoded = layer2filtervalid(decoded)
dumpexcerpt(decoded, 20, 20)

writetofile('layers/layer3.txt', decoded)
