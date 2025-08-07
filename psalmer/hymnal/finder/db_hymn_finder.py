from .hymn_finder import HymnFinder

class DbHymnFinder(HymnFinder):
    def __init__(self, i_hymnal_code: str):
        super(i_hymnal_code)

    def text_by_id(i_id:int) -> str:
        return f"TODO: SELECT hymn_text FROM hymnal_text WHERE hymn_id = {i_id}"