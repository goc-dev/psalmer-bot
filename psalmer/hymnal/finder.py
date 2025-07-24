from abc import ABC, abstractmethod
from pathlib import Path
from hymnal.meta import HymnalMeta, HymnMeta

import logging

logger = logging.getLogger('psalmer-bot')

#------------------
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


#------------------
class FileHymnFinder(HymnFinder):
    __hymnal_home_path:Path = Path()

    @classmethod
    def set_home_path( cls, i_home_path: Path):
        cls.__hymnal_home_path = i_home_path

    @classmethod
    def get_home_path(cls) -> Path:
        return cls.__hymnal_home_path

    def __init__(self, i_hymnal_meta: HymnalMeta):
        super().__init__(i_hymnal_meta)

    def hymnal_path(self) -> Path:
        v_home:Path = self.get_home_path()
        v_meta:HymnalMeta = self.get_hymnal_meta()
        logger.debug( f"HymnalPath: meta: {v_meta}")
        v_code:Path = Path(v_meta.code)
        v_home = v_home / v_code
        return v_home
    

    def hymn_list(self, i_hymn_id: int = None, i_range_id: int = None) -> list[HymnMeta]:
        logger.debug(f'hymn_list:[hymn_id:{i_hymn_id}][range_id:{i_range_id}]')
        v_hymns:list[HymnMeta] = []

        v_path = self.hymnal_path()
        if not v_path.exists():
            logger.warning( f'Path does not exist: {v_path}')
            return v_hymns
        
        for filename in v_path.iterdir():
            if not filename.is_file():
                continue

            v_hymn_id   :int = filename.stat().st_ino
            v_hymn_title:str = filename.stem
            v_hymn_fmt  :str = filename.suffix.lstrip('.')
            
            v_hymnal_meta = self.get_hymnal_meta()

            # check range:
            if i_range_id is not None:
                # TODO: add logic here
                pass

            # check hymn:
            if i_hymn_id is None or i_hymn_id == v_hymn_id:
                
                v_hymn_meta = HymnMeta( v_hymnal_meta.id, v_hymn_id, v_hymn_fmt, v_hymn_title)
                v_hymns.append(v_hymn_meta)
                
                if i_hymn_id is not None:
                    break

        return v_hymns
    

    def hymn_to_file(self, hymn: HymnMeta) -> Path:
        """Assemble a file name from its meta"""
        fn = f'{hymn.title}.{hymn.fmt}'
        fqn = self.hymnal_path() / fn
        return fqn


    def text_by_id(self, i_id: int) -> str:
        """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""
        logger.debug(f'text-by-id:{i_id}')
        # Iterate through files in the directory and find matching prefix
        v_hymns = self.hymn_list(i_id)

        v_song_text_md = f'File not found: {i_id}'
        if v_hymns is not None:
            v_hymn_meta = v_hymns[0]
            hymn_file = self.hymn_to_file(v_hymn_meta)
            with open( hymn_file, 'r') as song_file:
                v_song_text_md = song_file.read() 

        return v_song_text_md
    
    

#--------------
class DbHymnFinder(HymnFinder):
    def __init__(self, i_hymnal_code: str):
        super(i_hymnal_code)

    def text_by_id(i_id:int) -> str:
        return f"TODO: SELECT hymn_text FROM hymnal_text WHERE hymn_id = {i_id}"