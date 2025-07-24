import pytest
import asyncio
from hymnal.catalog import HymnalLib
from types import SimpleNamespace

@pytest.fixture
async def fx__HymnalLib():
    PS_LIB_DIR = '/workspaces/psalmer-bot/hymnal-lib/mdv2'
    hymnal_lib = await HymnalLib.init(PS_LIB_DIR)
    return hymnal_lib

@pytest.fixture
def fx__hymnal_2021():
    return SimpleNamespace(
        ID = 1,
        CODE = 'goc-2021'
    )

@pytest.mark.anyio('asyncio')
async def test_hymnal_meta(fx__HymnalLib, fx__hymnal_2021):
    # v_hymnal_id = 1
    # v_hymnal_code_tobe = 'goc-2021'
    v_hymnal_meta = fx__HymnalLib.hymnal_meta(fx__hymnal_2021.ID)
    
    assert v_hymnal_meta.code == fx__hymnal_2021.CODE # v_hymnal_code_tobe

@pytest.mark.anyio
async def test_range_meta(fx__HymnalLib, fx__hymnal_2021):
    v_range_meta = fx__HymnalLib.range_meta( fx__hymnal_2021.ID, 3)

    assert v_range_meta is not None
