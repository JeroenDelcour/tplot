from typing import Iterable


def get_braille(s: str) -> str:
    """
    `s` specifies which dots in the desired braille character must be on ('1') and which must be off ('0').
    Dots in the 2x8 braille matrix are ordered top-down, left-to-right.
    The order of the '1's and '0's in `s` correspond to this.
    Schematic example:
    ▪    10
     ▪   01
    ▪▪ = 11
     ▪   01
    ⢵ = '10100111'

    More examples:
    '10000000' = ⠁ (only top left dot)
    '11001111' = ⢻
    '11111111' = ⣿
    '00000000' = ⠀ (empty braille character)
    """
    s = (
        s[:3] + s[4:7] + s[3] + s[7]
    )  # rearrange ISO/TR 11548-1 dot order to something more suitable
    return chr(0x2800 + int(s[::-1], 2))


def braille_bin(char: str) -> str:
    """Inverse of get_braille()"""
    o = ord(char) - 0x2800
    s = format(o, "b").rjust(8, "0")
    s = s[::-1]
    s = (
        s[:3] + s[6] + s[3:6] + s[7]
    )  # rearrange ISO/TR 11548-1 dot order to something more suitable
    return s


def is_braille(char: str) -> bool:
    """Return True if provided unicode character is a braille character."""
    return isinstance(char, str) and 0x2800 <= ord(char[0]) <= 0x28FF


def braille_from_xy(x: int, y: int) -> str:
    """
    Returns braille character with dot at x, y position filled in.
    Example: braille_from_xy(x=1, y=0) returns "⠈" (top right dot filled in)
    """
    if not 0 <= x <= 1 or not 0 <= y <= 3:
        raise ValueError("Invalid braille dot position.")
    s = ["0"] * 8
    s[x * 4 + y] = "1"
    return get_braille("".join(s))


def combine_braille(braille: Iterable[str]) -> str:
    """
    Returns braille character that combines dots of input braille characters.
    Example: combine_braille("⠁⠂") returns "⠃"
    """
    out_bin = 0b00000000
    for char in braille:
        braille_b = braille_bin(char)
        out_bin |= int(braille_b, 2)
    s = format(out_bin, "b").rjust(8, "0")
    return get_braille(s)


def draw_braille(x: float, y: float, canvas_str=None) -> str:
    """
    Returns braille character for given x, y position.
    If canvas_str is already a braille character, the new braille dot will be added to it.
    """
    x = round((x + 0.500000001) % 1)  # 0 or 1. 0.500000001 so it rounds half up.
    y = 3 - round((-y + 0.375000001) % 1 * 4) % 4  # 0, 1, 2, or 3
    out = braille_from_xy(x, y)
    for character in canvas_str:
        if is_braille(character):
            out = combine_braille([out, character])
            break
    return out
