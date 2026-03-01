from dataclasses import dataclass

@dataclass
class HymnMeta:
    hymnal_id: int
    id       : int
    fmt      : str
    title    : str