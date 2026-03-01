from enum import Enum

class HymnFileType(str, Enum):
    """Enumeration of supported hymn file types."""
    MD_V2 = 'mdv2'
    PDF   = 'pdf'
    TXT   = 'txt'
    MP3   = 'mp3'
    OGG   = 'ogg'
    JPEG  = 'jpeg'
    PNG   = 'png'