import pytest
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('psalmer-bot')

from hymnal.meta import HymnalMeta
from hymnal.finder import FileHymnFinder
from hymnal.catalog import HymnalLib
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
        ID    = 1,
        CODE  = 'goc-2021',
        TITLE = 'Grace of Christ, 2021'
    )

@pytest.fixture
def fx__hymnal_test_1():
    return SimpleNamespace (
        ID    = 2,
        CODE  = 'test-1',
        TITLE = 'QA Testing Song Book'
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



@pytest.fixture
def fx__FHF_goc_2021():
    PS_HOME_DIR = '/workspaces/psalmer-bot/hymnal-lib/mdv2'
    PS_HYMNAL_DIR = 'goc-2021'
    v_hymnal = HymnalMeta(1, PS_HYMNAL_DIR, 'Благодать Христа, 2021')
    FileHymnFinder.set_home_path(PS_HOME_DIR)
    v_fhf = FileHymnFinder(v_hymnal)
    return v_fhf


@pytest.fixture
def fx__FHF_test_1():
    PS_HOME_DIR = '/workspaces/psalmer-bot/hymnal-lib/mdv2'
    v_hymnal = HymnalMeta(2, 'test-1', 'QA Testing Song Book')
    FileHymnFinder.set_home_path(PS_HOME_DIR)
    v_fhf = FileHymnFinder(v_hymnal)
    return v_fhf


### def test_text_by_id__smoke(fx__FHF_goc_2021):
###     v_id = 66
###     v_hymn_md = fx__FHF_goc_2021.text_by_id(v_id)
###     assert str(v_id) in v_hymn_md
###     assert "C#m" in v_hymn_md



def test_ranges(fx__FHF_test_1, fx__hymnal_test_1):
    v_home_path:Path = fx__FHF_test_1.get_home_path()

    assert v_home_path is not None

    v_hlib:HymnaLib = HymnalLib()
    v_hlib.init( str(v_home_path))

    v_range_id = 6
    v_range_meta = v_hlib.range_meta(fx__hymnal_test_1.ID, v_range_id)
    v_hymns = fx__FHF_test_1.hymn_list( None, v_range_meta)
    assert len(v_hymns) == 1

    v_range_id = 1
    v_range_meta = v_hlib.range_meta(fx__hymnal_test_1.ID, v_range_id)
    v_hymns = fx__FHF_test_1.hymn_list( None, v_range_meta)
    assert len(v_hymns) == 2