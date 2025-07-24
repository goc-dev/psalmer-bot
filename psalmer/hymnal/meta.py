from dataclasses import dataclass

@dataclass
class HymnalMeta:
    id: int
    code: str
    title: str

@dataclass
class RangeMeta:
    hymnal_id: int
    id: int
    starting_prefix: str
    ending_prefix: str

@dataclass
class HymnMeta:
    hymnal_id: int
    id: int
    fmt: str
    title: str

