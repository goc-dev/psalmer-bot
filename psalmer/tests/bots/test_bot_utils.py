import pytest
from bots.utils.messages import Message

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