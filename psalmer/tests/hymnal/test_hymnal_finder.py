import pytest
from hymnal.finder import FileHymnFinder

def test_home_dir():
    v_dir_tobe = '/home/psalmer-bot/hymnal'
    FileHymnFinder.set_home_path(v_dir_tobe)
    v_dir_asis = FileHymnFinder.get_home_path()
    #v_dir_asis = 'abc/def'
    assert v_dir_asis == v_dir_tobe, 'Home dirs are not the same'

def test_hymnal_dir():
    v_dir_tobe = '/home/abc/def'

    v_hf = FileHymnFinder(v_dir_tobe)
    v_dir_asis = v_hf.hymnal_path()
    assert v_dir_tobe == v_dir_asis
    v_dir_asis = v_hf.get_hymnal_code()
    assert v_dir_tobe == v_dir_asis


@pytest.fixture
def fixture__FHF_goc_2021():
    PS_HOME_DIR = '/workspaces/psalmer-bot/hymnal'
    PS_HYMNAL_DIR = 'goc-2021'
    FileHymnFinder.set_home_path(PS_HOME_DIR)
    v_fhf = FileHymnFinder(PS_HYMNAL_DIR)
    return v_fhf


def test_text_by_id__smoke(fixture__FHF_goc_2021):
    v_id = 66
    v_hymn_md = fixture__FHF_goc_2021.text_by_id(v_id)
    assert str(v_id) in v_hymn_md
    assert "C#m" in v_hymn_md
