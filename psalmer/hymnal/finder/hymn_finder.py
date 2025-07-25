from abc import ABC, abstractmethod
from hymnal.meta import HymnalMeta, HymnMeta

class HymnFinder(ABC):
    def __init__(self, i_hymnal_meta: HymnalMeta):
        self.__hymnal_meta = i_hymnal_meta

    def get_hymnal_meta(self) -> HymnalMeta:
        return self.__hymnal_meta
    
    @abstractmethod
    def text_by_id(self, i_id: int) -> str:
        pass

    @abstractmethod
    def hymn_list(i_hymn_id:int = None, i_range_id:int = None) -> list[HymnMeta]:
        """List all of v_hymns of the hymnal, or 1 specific hymn"""
        pass