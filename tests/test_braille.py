import pytest

from tplot.braille import (
    braille_bin,
    braille_from_xy,
    combine_braille,
    draw_braille,
    get_braille,
    is_braille,
)


def test_single_characters():
    assert get_braille("00000000") == "⠀"
    assert get_braille("10100111") == "⢵"
    assert get_braille("01011000") == "⡊"
    assert get_braille("11001111") == "⢻"
    assert get_braille("11111111") == "⣿"


def test_braille_bin():
    assert braille_bin("⠀") == "00000000"
    assert braille_bin("⢵") == "10100111"
    assert braille_bin("⡊") == "01011000"
    assert braille_bin("⢻") == "11001111"
    assert braille_bin("⣿") == "11111111"


def test_is_braille():
    assert is_braille("⠀") is True
    assert is_braille(" ") is False
    assert is_braille("⟿") is False
    assert is_braille("⤀") is False
    assert is_braille("⡷") is True


def test_braile_from_xy():
    assert braille_from_xy(x=1, y=0) == "⠈"
    assert braille_from_xy(x=1, y=3) == "⢀"
    with pytest.raises(ValueError):
        braille_from_xy(x=2, y=0)
    with pytest.raises(ValueError):
        braille_from_xy(x=0, y=4)


def test_combine_braille():
    assert combine_braille("⠁⠂") == "⠃"
    assert combine_braille(["⢵", "⡊"]) == "⣿"


def test_draw_braille():
    assert draw_braille(x=0.3, y=0.8, canvas_str=" ") == "⠐"
    assert draw_braille(x=0.3, y=0.8, canvas_str="#") == "⠐"
    assert draw_braille(x=0.5, y=0.5, canvas_str=" ") == "⡀"
    assert draw_braille(x=0, y=0, canvas_str=" ") == "⠐"
    assert draw_braille(x=-0.1, y=-0.2, canvas_str="⠁") == "⠃"
