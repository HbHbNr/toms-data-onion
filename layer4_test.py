import layer4

# GNU General Public License Version 3
#
# Checksum example from https://en.wikipedia.org/wiki/IPv4_header_checksum

ipheader = bytes(b'\x45\x00\x00\x73\x00\x00\x40\x00\x40\x11\xb8\x61\xc0\xa8\x00\x01\xc0\xa8\x00\xc7')

def test_headerchecksum():
    assert layer4.ipheaderchecksum(ipheader, 0, 10) == 0xffff
