from .word import *
from .language import *
from .analysis import *

def verb_ending(radical:str, ending:str):
    return Word(radical + ending)

def conjugate(pronoun_type:str, verb_raw:Word):
    pronoun = language["pronouns"][pronoun_type]
    verb_radical = analyse_word(verb_raw)[RADICAL]
    if pronoun_type == "3s":
        verb = verb_ending(verb_radical, language["verbs"]["ending"]["3rdperson"])
    else:
        verb = verb_ending(verb_radical, language["verbs"]["ending"]["normal"])
    return str(" ".join([Word(pronoun).string, Word(verb).string]))