# GNU General Public License Version 3

def decode(a):
    if not a.startswith('<~'):
        print('start marker not found')
        return False
    print('start marker found')
    if not a.endswith('~>'):
        print('end marker not found')
        return False
    print('end marker found')
    a = a[2:len(a)-2]

    decoded = ''
    fulltuples = len(a) // 5
    remainder = len(a) % 5
    print(fulltuples)
    print(remainder)
    currentoffset = 0
    for i in range(fulltuples):
        decoded = decoded + decodeTuple(a[currentoffset:currentoffset+5])
        currentoffset += 5
    if remainder > 0:
        padded = a[currentoffset:len(a)].ljust(5, 'u')
        decoded = decoded + decodeTuple(padded)[0:4-(5-remainder)]
    return decoded

def decodeTuple(tuple5):
    if len(tuple5) != 5:
        print('wrong size of tuple: "' + tuple5 + '"')
        return False
    
    decoded = ''
    charsum = 0
    for i in range(5):
        charsum *= 85
        charsum += (ord(tuple5[i]) - 33)
    for i in range(4):
        decoded += chr((charsum >> (8 * (3 - i))) % 256)
    #print(tuple5)
    #print(decoded)
    return decoded
