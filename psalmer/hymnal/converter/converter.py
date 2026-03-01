import re

def convert_f1_to_f0(s: str)-> str:
    return re.sub(r'{.*?}', '', s)
    