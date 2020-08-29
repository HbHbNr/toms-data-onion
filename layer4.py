# GNU General Public License Version 3

def ipheaderchecksum(s, i, count):
    sum = 0
    for ii in range(0, count * 2, 2):
        sum += int.from_bytes([s[ii], s[ii + 1]], 'big')
    
    while sum > 0xffff:
        carry = sum >> 16
        sum &= 0xffff
        sum += carry
    
    return sum

def parseIPpackage(s, i):
    version = s[i + 0] >> 4
    headerlength = (s[i + 0] & 0xf) * 4
    totallength = int.from_bytes([s[i + 2], s[i + 3]], 'big')
    identification = int.from_bytes([s[i + 4], s[i + 5]], 'big')
    protocol = s[i + 9]
    sourceip = int.from_bytes([s[i + 12], s[i + 13], s[i + 14], s[i + 15]], 'big')
    destinationip = int.from_bytes([s[i + 16], s[i + 17], s[i + 18], s[i + 19]], 'big')
    print(str(version) + ' ' + str(headerlength) + ' ' + str(totallength) + ' ' + str(identification) + ' ' + str(protocol) + ' ' + hex(sourceip) + ' ' + hex(destinationip))
    
    content = ''
    ipchecksum2 = ipheaderchecksum(s, i, 10)
    if ipchecksum2 != 0xffff:
        print('wrong IP checksum: ' + hex(ipchecksum2))
    else:
        if protocol == 17:
            u = i + headerlength
            sourceport = int.from_bytes([s[u + 0], s[u + 1]], 'big')
            destinationport = int.from_bytes([s[u + 2], s[u + 3]], 'big')
            udplength = int.from_bytes([s[u + 4], s[u + 5]], 'big')
            udpchecksum = int.from_bytes([s[u + 6], s[u + 7]], 'big')
            print(str(sourceport) + ' ' + str(destinationport) + ' ' + str(udplength) + ' ' + str(udpchecksum))
            
            udpchecksum2 = 0xabcd # needs proper checking of pseudo header
            if udpchecksum2 != 0xffff:
                print('wrong UDP checksum: ' + hex(udpchecksum2))
            else:
                if sourceip == 0x0a01010a and destinationip == 0x0a0101c8 and destinationport == 42069:
                    content = s[u + 8:u + udplength]
    return (totallength, content)

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
