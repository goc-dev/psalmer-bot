#-*- coding: cp1251 -*-
import re
import enum

def get_chords_for_mode(s, mode: str)->str:
    result = ""
    if mode == 'd':
        result = re.sub(r'\{([^:}]*):([^:{}]*)\}', r'{\1}', s)
    elif mode == 'u':
        result = re.sub(r'\{([^:}]*):([^:{}]*)\}', r'{\2}', s)
    else:
        raise Exception("The second argument must be only u or d")
    return re.sub(r'{}', "", result)

def chords_up(s: str)->[]:
    if not "{" in s:
        return [s,]
    chords = ""
    while "{" in s:
        first_chord = re.search(r'\{[^\}]{1,}}', s)
        begin = first_chord.start()
        end = first_chord.end()
        chord_text = s[begin + 1 : end - 1]
        s = s[:begin] + s[end:]
        insert_pos = begin - len(chord_text) // 2
        if insert_pos - 1 <= len(chords):
            len_diff = 1 + len(chords) - insert_pos
            insert_pos = len(chords) + 1
            s = s[:begin] + '+' * len_diff + s[begin:]
        chords += " " * (insert_pos - len(chords))
        chords += chord_text
        while (True):
            pluces_region = re.search(r'\w\++\w', s)
            if pluces_region is None:
                break
            start = pluces_region.start()
            end = pluces_region.end()
            s = s[:start + 1] + "-" * (end - start - 2) + s[end - 1:]
        while "+" in s:
            s = s.replace("+", " ")
        #это костыль
        if chords[0] == " " and s[0] == " ":
            chords = chords[1:]
            s = s[1:]
    return [chords, s]
                    
def convert_f1_to_f2(s, mode: str)->[]:
    return chords_up(get_chords_for_mode(s, mode))

def convert_f1_to_f0(s: str)-> str:
    while "{" in s:
        begin = s.find("{")
        end = s.find("}")
        chord = s[begin : end + 1]
        s = s.replace(chord, "", 1)
    return s

class PsalmType(enum.Enum):
    choir = 0
    children = 1

def isrussian(q):
    return (q in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

#Delete all, except russian letters, and changes all whiteSpace symbols to priors
def rafinator(s: str)-> str:
    s = s.lower()
    s1 = ""
    for q in s:
        if q.isspace():
            s1 += " "
        elif isrussian(q):
            s1 += q
        else:
            pass
    s1 += " "
    while "  " in s:
        s1 = s1.replace("  ", " ")
    return s1

class Psalm:
    def __init__(self, id_: int, info: {}):
        if not info["parse_succeeded"]:
            self = None
            return
        self.id_ = id_
        self.title = info["title"]
        self.f1 = info["text_f1"]
        self.type = info["type"]
        self.tone = info["tone"]
        text_for_search = ""
        for s in self.f1:
            text_for_search += rafinator(convert_f1_to_f0(s))
        self.str_for_search = text_for_search
        
    def show(self):
        print("id ", self.id_)
        print(self.str_for_search)

    def give_result_f0(self):
        return list(map(convert_f1_to_f0, self.f1))

    def give_result_f2(self, mode):
        pairs = list(map(lambda s: convert_f1_to_f2(s, mode), self.f1))
        result = []
        for M in pairs:
            result = [*result, *M]
        return result
    #id
    #tytle
    #str_for_search
    #f1
    #tone aka music key
    #type

class PsalmCollection:
    def __init__(self):
        self.psalms = {}

    def try_to_add(self, ps: Psalm)->bool:
        if ps.id_ in self.psalms.keys():
            return False
        else:
            self.psalms[ps.id_] = ps
            return True

    def remove(self, id_: int):
        if id_ in self.psalms.keys():
            del self.psalms[id_]

    def first_letter_search(self, letter: str):
        if len(letter) != 1:
            raise Exception("For search by first letter only one letter is required")
        letter = letter.lower()
        result = [x for x in self.psalms.values() if (x.title[0]).lower() == letter]
        return result

    def full_text_search(self, s: str):
        result = []
        s = rafinator(s)
        words = s.split()
        for ps in self.psalms.values():
            a = True
            for word in words:
                if not (word in ps.str_for_search):
                    a = False
                    break
            if a:
                result.append(ps)
        return result

    @staticmethod
    def filter_search_results(psalms: [], *, ps_type):
        if not ps_type:
            return [x for x in psalms if x.type == ps_type]
        

class DataManager:
    pass

def number_of_entries(subs: str, text: []):
    return len(list(filter(lambda s: subs in s, text)))

def find_pos(text, subs):
    for i in range(len(text)):
        if subs in text[i]:
            return i

def get_all_lines(filname):
    f = open(filname, "r", encoding = 'utf-8')
    result = []
    for s in f:
        if s[-1] == '\n':
            s = s[:-1]
        result.append(s)
    f.close()
    return result

#For visualization of too long strings
# call: insert_to_pos("123456", "|", 5)
# result: "12345|6"
def insert_to_pos(s, c: str, i: int)->str:
    if len(s) >= i:
        return s[:i] + c + s[i:]
    else:
        return s + " " * (i - len(s) - 1) + c

#This function parses file and gives info
# (errors, tags) as a dictionary
#with keys:
#"text_f1"
#    "warnings"
#   "errors"
# "parse_succeeded"
#  "title"
# "type"
# "tone"
def parse_file_to_psalm(text:[], max_length = 37)->{}:
    parse_successful = True
    psalm_info = {}
    list_of_errors = []
    list_of_warnings = []
    #placeholder 1: #title
    title_entries = number_of_entries("#title", text)
    psalm_info["title"] = None
    if 0 == title_entries:
        parse_successful = False
        list_of_errors.append("Text does not contain title of the psalm in format #title <title>")
    elif 1 == title_entries:
        title_line = ([x for x in text if "#title" in x])[0]
        title_line = title_line.replace("#title", "").strip()
        psalm_info["title"] = title_line
    else:
        parse_successful = False
        list_of_errors.append("Text contains more than one title of the psalm in format #title <title>")
    #placeholder 2: #type
    type_holders = {}
    for i in range(len(text)):
        if "#type" in text[i]:
            type_holders[i] = text[i]
    psalm_types = set()
    format_types = {"choir":PsalmType.choir, "children":PsalmType.children}
    for i in type_holders.keys():
        s = type_holders[i]
        s = s.replace("#type", "").strip()
        if s in format_types:
            psalm_types.add(format_types[s])            
        else:
            parse_successful = False
            list_of_errors.append("Line" + str(i + 1) + ": Unknown PsalmType " + s)
    psalm_info["type"] = psalm_types
    #music key
    tone_entries = number_of_entries("$", text)
    if 0 == tone_entries:
        parse_successful = False
        list_of_errors.append("Text does not contain music key in format $key")
    elif 1 == tone_entries:
        tone = ([x for x in text if "$" in x])[0]
        tone = tone.replace("$", "").strip()
        psalm_info["tone"] = tone
    else:
        parse_successful = False
        list_of_errors.append("Text contains more than one music key in format $key")
    #parsing of the lirics with chords
    psalm_text_f1 = []
    for i in range(len(text)):
        s = text[i]
        if "#" in s or "$" in s:
            continue
        if "{}" in s:
            list_of_warnings.append("Line" + str(i + 1) + ": empty chord")
        #validation rules
        # 1. Brackets {} shall be paired and not nested
        # 2. In one pair of brackets {}, there shall be no more than one separator symbol ":"
        # 3. Length of each resulting string after parsing shall not exceed max (37)
        # 4. come up with more:)
        brackets_level = 0
        colons_in = 0
        in_brackets = False
        for c in s:
            if c == "{":
                brackets_level += 1
                in_brackets = True
            elif c == "}":
                brackets_level -= 1
                in_brackets = False
                colons_in = 0
            elif c == ":" and in_brackets:
                colons_in += 1
            if not (0 == brackets_level or 1 == brackets_level):
                parse_successful = False
                list_of_errors.append("Line " + str(i + 1) + " contains unpaired or nested brackets")
            if colons_in > 1:
                parse_successful = False
                list_of_errors.append("Line " + str(i + 1) + ' contains more than 1 chords separators ":" in brackets')
        s_f2_u = convert_f1_to_f2(s, "u")
        s_f2_d = convert_f1_to_f2(s, "d")
        for line in s_f2_u:
            if len(line) > max_length:
                parse_successful = False
                list_of_errors.append("too long string #" + str(i + 1) + "in upr-mode >" + str(max_length)\
                                      + ": " + insert_to_pos(line, "|", max_length))
        for line in s_f2_d:
            if len(line) > max_length:
                parse_successful = False
                list_of_errors.append("too long string #" + str(i + 1) + "in dsp-mode >" + str(max_length)\
                                      + ": " + insert_to_pos(line, "|", max_length))
        if parse_successful:
                psalm_text_f1.append(s)
    psalm_info["text_f1"] = psalm_text_f1 if parse_successful else None
    psalm_info["warnings"] = list_of_warnings
    psalm_info["errors"] = list_of_errors
    psalm_info["parse_succeeded"] = parse_successful
    return psalm_info
        
M = get_all_lines("BogMoyHraniMenya.txt")
T = parse_file_to_psalm(M)
ps = Psalm(1, T)

collect = PsalmCollection()
collect.try_to_add(ps)
q = collect.first_letter_search("Б")
for c in q:
    c.show()











































    
