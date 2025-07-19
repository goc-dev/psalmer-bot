from pathlib import Path
import csv
from hymnal.meta import HymnalMeta, HymnMeta
from hymnal.finder import FileHymnFinder

import logging

logger = logging.getLogger('psalmer-bot')


class HymnalLib:
    __lib_path: Path
    __list_file: Path

    @classmethod
    async def init(cls, i_lib_dir: str):
        cls.__lib_path = Path(i_lib_dir)
        cls.__list_file = cls.__lib_path / 'hymnals.csv'
        print(f"Hymnal Lib  is in: {cls.__lib_path} ({cls.__lib_path.exists()})")
        print(f"Hymnal list is in: {cls.__list_file} ({cls.__list_file.exists()})")
        

    @classmethod
    def hymnal_list(cls, i_hymnal_id: int = None) -> list[HymnalMeta]:
        """CSV: ID(int), CODE(str), TITLE(str)"""

        # TODO: keep content in-memory to not read from file each time

        print(f"Hymnal list: filter by id: {i_hymnal_id}")

        v_list=[]

        with open( cls.__list_file, newline='', encoding='utf-8') as csv_hymnals:
            reader = csv.DictReader(csv_hymnals)
            for row in reader:
                logger.debug(row)
                v_hymnal_meta = HymnalMeta( int(row['ID']), row['CODE'], row['TITLE'])
                if i_hymnal_id is None \
                or v_hymnal_meta.id == i_hymnal_id:
                    v_list += [v_hymnal_meta]
                    if i_hymnal_id is not None:
                        break
        return v_list
    

    @classmethod
    def hymnal_index(cls, i_hymnal_id: int) -> list[HymnMeta]:
        """Read the content of hymnal by its ID"""

        v_hymnal_1 = HymnalLib.hymnal_list( i_hymnal_id)
        v_hymnal_meta = v_hymnal_1[0]

        v_hymn_list = []

        if v_hymnal_meta:
            ff = FileHymnFinder( v_hymnal_meta)
            v_hymn_list = ff.hymn_list()
        else:
            logger.debug(f'Hymnal Index: no hymnal meta for {i_hymnal_id}')

        return v_hymn_list
    
    @classmethod
    def hymnal_code( cls, i_hymnal_id: int) -> str:
        v_hymnals = HymnalLib.hymnal_list(i_hymnal_id)
        return Path(v_hymnals[0].code)

    @classmethod
    def hymn_text(cls, i_hymnal_id: str, i_hymn_id: int) -> str:
        v_code = HymnalLib.hymnal_code( i_hymnal_id)
        v_hymnal_meta = HymnalMeta( i_hymnal_id, v_code, '-')
        v_ff = FileHymnFinder(v_hymnal_meta)
        v_hymn_md = v_ff.text_by_id(i_hymn_id)
        return v_hymn_md