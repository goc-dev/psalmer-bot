from abc import ABC, abstractmethod
import os

#------------------
class HymnFinder(ABC):
    def __init__(self, i_hymnal_code: str):
        self.__hymnal_code = i_hymnal_code

    def get_hymnal_code(self):
        return self.__hymnal_code
    
    @abstractmethod
    def text_by_id(self, i_id: int) -> str:
        pass

#------------------
class FileHymnFinder(HymnFinder):
    __hymnal_home_dir:str = ''

    @classmethod
    def set_home_dir( cls, i_home_dir: str):
        cls.__hymnal_home_dir = i_home_dir

    @classmethod
    def get_home_dir(cls):
        return cls.__hymnal_home_dir

    def __init__(self, i_hymnal_dir: str):
        super().__init__(i_hymnal_code = i_hymnal_dir)

    def hymnal_dir(self):
        return os.path.join( self.get_home_dir(), self.get_hymnal_code())
    
    def text_by_id(self, i_id: int) -> str:
        """This handler is for the command `/psalm #id to print text/chords of Psalm#id"""

        v_hymnal_dir = self.hymnal_dir() 
        v_hymn_id  = i_id
        v_hymn_idx = str(v_hymn_id)
        v_hymn_file = ''

        # Iterate through files in the directory and find matching prefix
        for filename in os.listdir(v_hymnal_dir):
            print(v_hymnal_dir, filename)
            if filename.startswith(v_hymn_idx):
                v_hymn_file = os.path.join( v_hymnal_dir, filename)
                break

        if '' == v_hymn_file:
            v_song_text_md = f'File not found: {i_id}'
        else:
            with open( v_hymn_file, 'r') as song_file:
                v_song_text_md = song_file.read()

        return v_song_text_md
    

#--------------
class DbHymnFinder(HymnFinder):
    def __init__(self, i_hymnal_code: str):
        super(i_hymnal_code)

    def text_by_id(i_id:int) -> str:
        return f"TODO: SELECT hymn_text FROM hymnal_text WHERE hymn_id = {i_id}"