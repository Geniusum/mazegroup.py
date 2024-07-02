from libs.word import *
from libs.vowels import*

def split_syllables(word:Word) -> list[str]:
    syllables = []
    current_syllable = ""
    
    for i, char in enumerate(word.string):
        current_syllable += char
        if char in vowels:
            if i < len(word.string) - 1 and word.string[i + 1] not in vowels:
                syllables.append(current_syllable)
                current_syllable = ""
    
    if current_syllable:
        syllables.append(current_syllable)

    return syllables