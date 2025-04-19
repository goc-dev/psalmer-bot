from pathlib import Path
import csv

class HymnalList:
    pass

class HymnalLib:
    __lib_path: Path
    __list_file: Path

    @classmethod
    async def init(cls):
        cls.__lib_path = Path('/workspaces/psalmer-bot/hymnal-lib/md')
        cls.__list_file = cls.__lib_path / 'hymnals.csv'
        print(f"Hymnal Lib  is in: {cls.__lib_path} ({cls.__lib_path.exists()})")
        print(f"Hymnal list is in: {cls.__list_file} ({cls.__list_file.exists()})")
        

    @classmethod
    def hymnal_list(cls):
        """CSV: ID(int), DIR(str), TITLE(str)"""

        print("Hymnal list...")

        v_list=[]

        with open( cls.__list_file, newline='', encoding='utf-8') as csv_hymnals:
            reader = csv.DictReader(csv_hymnals)
            for row in reader:
                #print(row)
                v_hymnal = { 'id': row['ID'], 'title': row['TITLE']}
                v_list += [v_hymnal]
                print(v_hymnal)

        return v_list
    

    @classmethod
    def hymnal_content(cls, i_hymnal_id: int):
        """Read the content of hymnal by its ID"""

        v_hymnal = {}
        v_hymn_list = []

        with open( cls.__list_file, newline='', encoding='utf-8') as csv_hymnals:
            reader = csv.DictReader(csv_hymnals)
            for row in reader:
                v_hymnal = { 'id': row['ID'], 'dir': row['DIR'], 'title': row['TITLE']}
                if v_hymnal['id'] == i_hymnal_id:
                    break

        if v_hymnal:
            v_hymn_list += [{"id": 1, "title": "One"}]
            v_hymn_list += [{"id": 2, "title": "Two"}]
            v_hymn_list += [{"id": 3, "title": "Tri"}]

        return v_hymn_list