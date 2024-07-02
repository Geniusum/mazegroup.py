from .word import *
from .syllables import *
from .kw import *
from .vowels import *

def analyse_word(word:Word):
    result = {
        START_WITH: None,
        END_WITH: None,
        RADICAL: None,
        LENGHT: None
    }

    syllables = split_syllables(word)

    result[START_WITH] = syllables[0]
    result[END_WITH] = syllables[-1]
    result[LENGHT] = len("".join(syllables))

    if len(syllables[-1]) == 1 and not syllables[-1] in ["r", "s", "t"]:
        syllables[-1] = "le"
        syllables.append("r")

    if result[START_WITH] != result[END_WITH]:
        radical = syllables[:-1]
        if [*radical[-1]][-1] in vowels:
            radical[-1] = "".join([*radical[-1]][0:-1])
        result[RADICAL] = "".join(radical)

    if len(syllables) <= 2:
        radical = syllables
        if [*radical[-1]][-1] in vowels:
            radical[-1] = "".join([*radical[-1]][0:-1])
        result[RADICAL] = "".join(radical)
    
    return result