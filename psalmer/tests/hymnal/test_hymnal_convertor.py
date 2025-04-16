import pytest
from hymnal.converter import convert_f1_to_f0


def test_cnv_f1_f0__one_liner():
    s_src = r'{A} text-1 {B#} text-2 {any long text}'
    s_tobe = r' text-1  text-2 '
    s_asis = convert_f1_to_f0(s_src)
    assert s_tobe == s_asis


def test_cnv_f1_f0__multiline():
    s_src = r"""
    Intro: {A}one {B}two
    Verse: Th{C#m}ree four{F#maj/E}
"""

    s_tobe = r"""
    Intro: one two
    Verse: Three four
"""

    s_asis = convert_f1_to_f0(s_src)
    assert s_tobe == s_asis