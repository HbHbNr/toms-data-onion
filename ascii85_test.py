import ascii85

# GNU General Public License Version 3
#
# Ascii85 example from https://en.wikipedia.org/wiki/Ascii85#Example_for_Ascii85

leviathan_encoded = '''<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKYi(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIal(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>'''
leviathan_plain = 'Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure.'
leviathan_file = 'tests/leviathan.txt'

tuples = [('t', 'F8'), ('td', 'FCY'), ('tdo', 'FC]:'), ('tdo!', 'FC];5')]

def test_decode():
    assert bytearray(leviathan_plain, 'utf-8') == ascii85.decode(leviathan_encoded)
    
    for (plain, encoded) in tuples:
        assert bytearray(plain, 'utf-8') == ascii85.decode('<~' + encoded + '~>')
        assert False == ascii85.decode(encoded)
        assert False == ascii85.decode('<~' + encoded)
        assert False == ascii85.decode(encoded + '~>')

def test_decodeTuple():
    for (plain, encoded) in tuples:
        if len(encoded) == 5:
            assert bytearray(plain, 'utf-8') == ascii85.decodeTuple(encoded.ljust(5, 'u'))[0:len(plain)]
        else:
            assert False == ascii85.decodeTuple(encoded)

def test_loadpayload():
    payload = ascii85.loadpayload(leviathan_file)
    assert leviathan_encoded == payload
