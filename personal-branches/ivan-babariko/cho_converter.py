#-*- coding: cp1251 -*-
import re, sys, os, enum

#example of call in PowerShell
#PS C:\Users\Lenovo> python.exe E:\\j\\prepro_text\\cho_converter.py  E:\\j\\prepro_text\\in1.chox -ext

class ChoVersion(enum.Enum):
    EXT = 'ext'
    BAS = 'bas'

class ChoConverter():
    @staticmethod
    def check_f1(s: str)->(bool, list):
        string_valid = True
        report = []
        brackets_mistake = False
        sep_mistake = False
        if "|]" in s:
            string_valid = False
            report.append("Invalid sintaxis: you must use [chord|-] instead of [chord|]")
        brackets_level = 0
        sep_in = 0
        in_brackets = False
        for c in s:
            if c == "[":
                brackets_level += 1
                in_brackets = True
            elif c == "]":
                brackets_level -= 1
                in_brackets = False
                sep_in = 0
            elif c == "|" and in_brackets:
                sep_in += 1
            if not (0 == brackets_level or 1 == brackets_level):
                string_valid = False
                brackets_mistake = True
            if sep_in > 1:
                sep_mistake = True
                string_valid = False
        if brackets_mistake:
            report.append("The string contains unpaired or nested brackets")
        if sep_mistake:
            report.append("'The string contains more than 1 chords separators "|" in brackets'")
        return (string_valid, report)

    @staticmethod
    def to_cho( from_chox: str, version: ChoVersion) -> str:
        result = ""
        if version == ChoVersion.EXT:
            result = re.sub(r'\[([^|\]]*)\|([^|\[\]]*)\]', r'[\1]', from_chox)
        elif version == ChoVersion.BAS:
            result = re.sub(r'\[([^|\]]*)\|([^|\[\]]*)\]', r'[\2]', from_chox)
        else:
            raise TypeError("Version must be EXT or BAS")
        result = re.sub(r'\[\]', "", result)
        return re.sub(r'\[-\]', "", result)        

args = sys.argv
#the first arg args[0] is an address of the current script
input_filname = args[1]
mode_ = args[2] #must be -ext or -bas
try:
    mode_value = mode_.lstrip('-').lower()
    mode = ChoVersion[mode_value.upper()]
except KeyError:
    print(f"Preprocessing failed: unknown mode {mode_}")
    sys.exit()
    
file_name, file_extension = os.path.splitext(input_filname)
if not file_extension == ".chox":
    print(f'invalid file format {file_extension} Must be .chox')
    sys.exit()
output_filname = file_name + ".cho"
text = []
try:
    with open(input_filname, "rt", encoding = 'utf-8') as f:
        for s in f:
            text.append(s)
except:
    print(f'Can not to read file {input_filname}')
    sys.exit()
text_valid = True
text_result = []
for i in range(len(text)):
    line = text[i]
    check = ChoConverter.check_f1(line)
    if check[0]:
        text_result.append(ChoConverter.to_cho(line, mode))
    else:
        text_valid = False
        print(f"Mistake in line {i + 1}:")
        for q in check[1]:
            print(q)
if text_valid:
    with open(output_filname, 'wt', encoding = 'utf-8') as f:
        for s in text_result:
            print(s, file = f, end = "")
    print("ready")
else:
    print("preprocessing failed")
























































