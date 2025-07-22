from dataclasses import dataclass

@dataclass
class HymnalMeta:
    id: int
    code: str
    title: str

@dataclass
class HymnMeta:
    hymnal_id: int
    id: int
    fmt: str
    title: str

@dataclass
class TitleBucketMeta:
    start: str
    end: str
    size: int
