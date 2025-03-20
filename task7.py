#Данный код написан в предположении, что 
#1. Музыканты быстрее понимают D-C, чем offset = -2
#2. Аккорды бывают в двух видах:
#  а. ПростоАккорд
#  б. Аккорд/Аккорд
#3. 
#
#
#
#




def calculate_offset(transponation_key, mode: str)->int:
    chips = transponation_key.split('-')
    first = chips[0]
    last = chips[1]
    chords = []
    if mode == "#":
        chords = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",]
    elif mode == 'b':
        chords = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab",]
    else:
        raise Exception("# -- диезы, b -- бемоли, иного не дано")
    return chords.index(last) - chords.index(first)

def transp_chord(chord, mode: str, offset: int)->str:
    all_chords = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",] if mode == '#'\
                 else ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab",]
    if "/" in chord:
        q = chord.split('/')
        first_chord = q[0]
        second_chord = q[1]
        return transp_chord(first_chord, mode, offset) + "/"\
               + transp_chord(second_chord, mode, offset)
    index = all_chords.index(chord)
    return all_chords[(index + offset) % 12]


#usage
offset = calculate_offset("D-C", '#')
print(offset)
print(transp_chord("F/G", '#', offset))







