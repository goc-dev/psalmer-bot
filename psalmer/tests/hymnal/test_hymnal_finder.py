import pytest
from hymnal.finder import FileHymnFinder
from hymnal.meta import HymnalMeta
from types import SimpleNamespace
from pathlib import Path

@pytest.fixture
def fx__cfg_codespace():
    return SimpleNamespace(
        HYMNAL_PATH = Path('/home/psalmer-bot/hymnal-lib/mdv2')
    )

@pytest.fixture
def fx__hymnal_goc_2021():
    return SimpleNamespace (
        ID = 1,
        CODE = 'goc-2021',
        TITLE = 'Grace of Christ, 2021'
    )

def test_home_dir(fx__cfg_codespace, fx__hymnal_goc_2021):
    v_dir_tobe = fx__cfg_codespace.HYMNAL_PATH
    FileHymnFinder.set_home_path(v_dir_tobe)
    v_dir_asis = FileHymnFinder.get_home_path()
    #v_dir_asis = 'abc/def'
    assert v_dir_asis == v_dir_tobe, 'Home dirs are not the same'


def test_hymnal_dir(fx__cfg_codespace, fx__hymnal_goc_2021):
    v_dir_tobe = Path( fx__cfg_codespace.HYMNAL_PATH / fx__hymnal_goc_2021.CODE)

    v_hymnal_meta = HymnalMeta( 1, 'goc-2021', 'Grace of Christ, 2021')

    v_hf = FileHymnFinder(v_hymnal_meta)
    v_dir_asis = v_hf.hymnal_path()
    assert v_dir_tobe == v_dir_asis
    v_dir_asis = v_hf.get_hymnal_code()
    assert v_dir_tobe == v_dir_asis


@pytest.fixture
def fixture__FHF_goc_2021():
    PS_HOME_DIR = '/workspaces/psalmer-bot/hymnal-lib/mdv2'
    PS_HYMNAL_DIR = 'goc-2021'
    v_hymnal = HymnalMeta(1, PS_HYMNAL_DIR, 'Благодать Христа, 2021')
    FileHymnFinder.set_home_path(PS_HOME_DIR)
    v_fhf = FileHymnFinder(v_hymnal)
    return v_fhf


def test_text_by_id__smoke(fixture__FHF_goc_2021):
    v_id = 66
    v_hymn_md = fixture__FHF_goc_2021.text_by_id(v_id)
    assert str(v_id) in v_hymn_md
    assert "C#m" in v_hymn_md
