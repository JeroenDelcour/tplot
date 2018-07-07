# -*- coding: utf-8 -*- 

def get_braille(s):
    """
    `s` is a string of '1's and '0's specifying which dots in the desired braille character must be on ('1') and which must be off ('0').
    Dots in the 2x8 braille matrix are ordered top-down, left-to-right, i.e:

    a •• e
    b •• f
    c •• g
    d •• h

    Schematic example:

    •    10
     •   01
    •• = 11
     •   01

    ⢵ = '10100111'
    
    More examples:
    '10000000' = ⠁ (only top left dot)
    '00011110' = ⡸
    '11001111' = ⢻
    '11111111' = ⣿
    '00000000' = ⠀ (empty braille character)

    For more info on the interesting relationship between binary and unicode braille dot ordering, see: https://en.wikipedia.org/wiki/Braille_Patterns#Identifying,_naming_and_ordering
    """
    s = s[:3] + s[4:7] + s[3] + s[7] # rearrange ISO/TR 11548-1 dot order to something more managable
    return chr(10240 + int(s[::-1],2))

def test_braille():
    assert(get_braille('10000000') == '⠁')
    assert(get_braille('11001111') == '⢻')
    assert(get_braille('11001111') == '⢻')
    assert(get_braille('11111111') == '⣿')
    assert(get_braille('00011110') == '⡸')
    assert(get_braille('00000000') == '⠀')
    print('All tests completed succesfully.')
