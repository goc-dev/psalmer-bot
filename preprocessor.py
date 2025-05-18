#-*- coding: cp1251 -*-
import enum, os, sys, re

#python.exe E:\\j\\prepro_text\\preprocessor.py  E:\\j\\prepro_text\\in2.chox -ext -h
# example of call
# python.exe {address of the current file} {address of the .chox} {-ext or -bas} {-h -- optional. Creates a .chox with
#all [] replaced with chords before mode choose}

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


class StrType(enum.Enum):
    sov = 0,
    eov = 1,
    soc = 2,
    eoc = 3,
    text = 4

class TokenType(enum.Enum):
    sov = 0,
    eov = 1,
    soc = 2,
    eoc = 3,
    just_text = 4,
    verse = 5,
    chorus = 6

class Token:
    def __init__(self, text_: str, tt_: TokenType):
        self.text = text_
        self.tt = tt_

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

all_chords_file_needed = False
if len(args) > 3:
    all_chords_file_needed = args[3] == "-h"
     
file_name, file_extension = os.path.splitext(input_filname)
if not file_extension == ".chox":
    print(f'invalid file format {file_extension} Must be .chox')
    sys.exit()
output_filname = file_name + ".cho"

text = []
text_str = ""
try:
    with open(input_filname, "rt", encoding = 'utf-8') as f:
        for s in f:
            text.append(s)
            text_str += s
except:
    print(f'Can not to read a file {input_filname}')
    sys.exit()
    
def string_type(s: str)->StrType:
    brackets = re.search(r'\{[^\}]+\}', s)
    if brackets == None:
        return StrType.text
    sub_s = brackets.group()
    if "start_of_verse" in sub_s or "sov" in sub_s:
        return StrType.sov
    elif "end_of_verse" in sub_s or "eov" in sub_s:
        return StrType.eov
    elif "start_of_chorus" in sub_s or "soc" in sub_s:
        return StrType.soc
    elif "end_of_chorus" in sub_s or "eoc" in sub_s:
        return StrType.eoc
    else:
        return StrType.text

tokens = []
verse_started = False
chorus_started = False
def exit_claim():
    print("I cannot do preprocessing for not every start/end token in the text is")
    print("paired and/or unnested")
    sys.exit()
        
for s in text:
    str_type = string_type(s)
    if str_type == StrType.text:
        if not (verse_started or chorus_started):
            a = Token(s, TokenType.just_text)
            tokens.append(a)
        else:
            tokens[-1].text += s
    elif str_type == StrType.sov:
        if verse_started or chorus_started:
            exit_claim()
        else:
            verse_started = True
            a1 = Token(s, TokenType.sov)
            tokens.append(a1)
            a2 = Token("", TokenType.verse)
            tokens.append(a2)
    elif str_type == StrType.soc:
        if verse_started or chorus_started:
            exit_claim()
        else:
            chorus_started = True
            a1 = Token(s, TokenType.soc)
            tokens.append(a1)
            a2 = Token("", TokenType.chorus)
            tokens.append(a2)
    elif str_type == StrType.eov:
        if chorus_started or (not verse_started):
            exit_claim()
        else:
            verse_started = False
            a = Token(s, TokenType.eov)
            tokens.append(a)
    elif str_type == StrType.eoc:
        if verse_started or (not chorus_started):
            exit_claim()
        else:
            chorus_started = False
            a = Token(s, TokenType.eoc)
            tokens.append(a)
    else:
        raise TypeError("")
    
verse_standard = None
chorus_standard = None

for t in tokens:
    if t.tt == TokenType.verse:
        #here must be an initiallization of verse_standard
        s = t.text
        verse_standard = re.findall(r'\[[^\]]+\]', s)
        break

for t in tokens:
    if t.tt == TokenType.chorus:
        s = t.text
        chorus_standard = re.findall(r'\[[^\]]+\]', s)
        break

def substitute_by_standard(standard: list, s: str)->str:
    if s.count("[]") > len(standard):
        raise Exception(" number of [] in text is more then in standard")
    for current_chord in standard:
        s = s.replace("[]", current_chord, 1)
    return s

for token in tokens:
    if not (token.tt == TokenType.verse or token.tt == TokenType.chorus):
        continue
    elif token.tt == TokenType.verse:
        token.text = substitute_by_standard(verse_standard, token.text)
    else:
        token.text = substitute_by_standard(chorus_standard, token.text)

text = []
for t in tokens:
    qq = t.text.rstrip('\n').split("\n")
    for q in qq:
        text.append(q.strip("\n"))

if all_chords_file_needed:
    out_fname = file_name + "__" + ".chox"
    with open(out_fname, 'wt', encoding = "utf-8") as f:
        for t in text:
            print(t, file = f)

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
            print(s, file = f)
    print("ready")
else:
    print("preprocessing failed")



























































        
