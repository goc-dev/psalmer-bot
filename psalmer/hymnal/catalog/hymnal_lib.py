from pathlib import Path
import csv
from hymnal.meta import HymnalMeta, RangeMeta, HymnMeta
from hymnal.finder import FileHymnFinder

import logging

logger = logging.getLogger('psalmer-bot')


class HymnalLib:
    __lib_path: Path
    __list_file: Path

    @classmethod
    def init(cls, i_lib_dir: str):
        cls.__lib_path = Path(i_lib_dir)
        cls.__list_file = cls.__lib_path / 'hymnals.csv'
        print(f"Hymnal Lib  is in: {cls.__lib_path} (Check: {cls.__lib_path.exists()})")
        print(f"Hymnal list is in: {cls.__list_file} (Check: {cls.__list_file.exists()})")
        return cls

    @classmethod
    async def init_async(cls, i_lib_dir: str):
        return cls.init(i_lib_dir)

    @classmethod
    def get_lib_path():
        return cls.__lib_path

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
    def hymnal_meta(cls, i_hymnal_id:int) -> HymnalMeta:
        v_hymnal_list_1 = cls.hymnal_list(i_hymnal_id)
        return v_hymnal_list_1[0]

    
    @classmethod
    def range_list(cls, i_hymnal_id: int, i_range_id: int = None) -> list[RangeMeta]:
        """CSV: HYMNAL_ID(int), ID(int), STARTING_PREFIX(str), ENDING_PREFIX(str)"""
        # get the filename for ranges
        v_hymnal_1 = HymnalLib.hymnal_list(i_hymnal_id)
        v_hymnal_meta = v_hymnal_1[0]
        v_hymnal_code = v_hymnal_meta.code
        v_hymn_ranges_file = f'hymn-ranges.{v_hymnal_code}.csv'
        v_hymn_ranges_path = cls.__lib_path / v_hymn_ranges_file

        v_range_list = []

        with open( v_hymn_ranges_path, newline='', encoding='utf-8') as csv_ranges:
            reader = csv.DictReader(csv_ranges)
            for row in reader:
                logger.debug(row)
                v_range_meta = RangeMeta( int(row['HYMNAL_ID']), int(row['RANGE_ID']), row['STARTING_PREFIX'], row['ENDING_PREFIX'])
                if i_range_id is None \
                or v_range_meta.id == i_range_id:
                    v_range_list += [v_range_meta]
                    if i_range_id is not None:
                        break
        return v_range_list


    @classmethod
    def range_meta(cls, i_hymnal_id:int, i_range_id:int) -> RangeMeta:
        v_range_list_1 = cls.range_list(i_hymnal_id, i_range_id)
        return v_range_list_1[0]


    @classmethod
    def hymnal_index(cls, i_hymnal_id: int, i_range_id: int = None) -> list[HymnMeta]:
        """Read the content of hymnal by its ID"""

        v_hymnal_1 = HymnalLib.hymnal_list( i_hymnal_id)
        v_hymnal_meta = v_hymnal_1[0]

        v_range_meta:RangeMeta | None = None

        if i_range_id is not None:
            v_range_1 = HymnalLib.range_list(i_hymnal_id, i_range_id)
            v_range_meta = v_range_1[0]

        v_hymn_list = []

        if v_hymnal_meta:
            ff = FileHymnFinder( v_hymnal_meta)
            v_hymn_list = ff.hymn_list(i_hymn_id = None, i_range_meta = v_range_meta)
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