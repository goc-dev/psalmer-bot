import pytest
from bots.utils.messages import Message
from bots.utils.markdown import MarkdownV2

def test_greeting():
    v_user_name = 'Abc Def'
    v_message_tobe = """
Hello, *Abc Def*!
Are you looking for any psalm/chords?
"""
    v_message_asis = Message.hello_user( v_user_name)
    assert v_message_asis == v_message_tobe

def test_help_info():
    v_help_text = Message.help_info()
    assert len(v_help_text) > 0
    assert '/start' in v_help_text
    assert '/help' in v_help_text
    assert '/psalm' in v_help_text


def test_escape_md_V2():
    v_text_src = "*Bold* - _italic_ : new [123]"
    v_text_tobe = r"\*Bold\* \- \_italic\_ : new \[123\]"
    v_text_asis = MarkdownV2.escape_text(v_text_src)
    assert v_text_asis == v_text_tobe
