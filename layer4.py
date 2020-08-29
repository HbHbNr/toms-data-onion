# GNU General Public License Version 3

def parseIPpackage(s, i):
    version = s[i + 0] >> 4
    headerlength = (s[i + 0] & 0xf) * 4
    totallength = int.from_bytes([s[i + 2], s[i + 3]], 'big')
    identification = int.from_bytes([s[i + 4], s[i + 5]], 'big')
    protocol = s[i + 9]
    sourceip = int.from_bytes([s[i + 12], s[i + 13], s[i + 14], s[i + 15]], 'big')
    destinationip = int.from_bytes([s[i + 16], s[i + 17], s[i + 18], s[i + 19]], 'big')
    print(str(version) + ' ' + str(headerlength) + ' ' + str(totallength) + ' ' + str(identification) + ' ' + str(protocol) + ' ' + hex(sourceip) + ' ' + hex(destinationip))
    return (totallength, s[i + headerlength + 8:i + totallength - headerlength + 1])

def parseIPpackages(stream):
    stream = bytes(stream)
    allcontent = bytearray()
    num = 1
    i = 0
    while i < len(stream):
        print(str(num) + '.: ' + str(i))
        (length, content) = parseIPpackage(stream, i)
        i += length
        allcontent.extend(content)
        num += 1
    return allcontent


if __name__ == '__main__':
    import ascii85

    payload = ascii85.loadpayload('layers/layer4.txt')
    decoded = ascii85.decode(payload)
    decoded = parseIPpackages(decoded)
    print(decoded)
