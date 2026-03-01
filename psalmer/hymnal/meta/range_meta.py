from dataclasses import dataclass

@dataclass
class RangeMeta:
    hymnal_id      : int
    id             : int
    starting_prefix: str
    ending_prefix  : str
    label          : str