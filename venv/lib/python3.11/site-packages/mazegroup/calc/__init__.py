import mazegroup.commands as commands

import re
import random as rd

class Exp():
    def __init__(self) -> None:
        self.lexical = {
            "syn_operators": {
                "plus": ["+"],
                "minus": ["-"],
                "divide": ["/"],
                "mul": ["*"],
                "is_equal": ["==", "?="],
                "is_not_equal": ["!=", "!?="],
                "more_equal": [">="],
                "less_equal": ["<="],
                "more": [">"],
                "less": ["<"],
                "concat": ["&"],
                "power": ["^"],
                "bracket_open": ["("],
                "bracket_close": [")"]
            },
            "strings": {
                "string": ["\"", "'"],
                "backslash": ["\\\\"],
                "new_line": ["\\n"],
                "tab": ["\\t"],
                "db_quotes": ["\\\""],
                "quote": ["\\'"]
            }
        }

        self.numbers = [*"0123456789"]

        self.strings = {}
    
    def genStringID(self):
        r = "#"
        for _ in range(16):
            r += rd.choice(self.numbers)
        if r in self.strings.keys():
            r = self.genStringID()
        return r
    
    def mkStringReference(self, string:str, id:str):
        self.strings[id] = string

    def refAllStrings(self, exp:str):
        ls = self.lexical["strings"]
        for i in ls["backslash"]:
            exp = exp.replace(i, "\\")
        for k, h in {"new_line": "\n", "tab": "\t", "db_quotes": "š", "quote": "ž"}.items():
            for i in ls[k]:
                exp = exp.replace(i, h)
        string = False
        buffer = ""
        buffer2 = ""
        current_sep = ""
        strings = []
        for char in [*exp]:
            ex = char in ls["string"]
            if current_sep != "":
                ex = char == current_sep
            if ex:
                if string:
                    current_sep = ""
                    string = False
                    id = self.genStringID()
                    buffer = buffer.replace("š", "\"").replace("ž", "\'")
                    strings.append([buffer, id])
                    buffer = ""
                    buffer2 += id
                else:
                    string = True
                    current_sep = char
            else:
                if string:
                    buffer += char
                else:
                    buffer2 += char
        for string_ in strings:
            string = string_[0]
            id = string_[1]
            self.mkStringReference(string, id)
        return buffer2
    
    def getStringFromRefID(self, id:str):
        for string_id, string in self.strings.items():
            if id == string_id:
                return string

    def split_spec(self, exp:str):
        for k, ops in self.lexical["syn_operators"].items():
            for op in ops:
                exp = re.sub(r'(?<!\S)' + re.escape(op) + r'(?!\S)', ' ' + op + ' ', exp)

        exp = re.sub(r'(?<=\d|\))(?=[^\d\)])|(?<=[^\d\()])(?=\d|\()|(?<=\()(?=\d)|(?<=\d)(?=\))', ' ', exp)
        
        return " ".join(exp.split())
    
    def convertFloatToIntIfPossible(self, num):
        if isinstance(num, float):
            if num.is_integer():
                return int(num)
        return float(num)

    def parse(self, exp:str):
        exp = exp.strip()
        exp = self.refAllStrings(exp)
        tokens_ = self.split_spec(exp).split()
        string_id = None
        tokens = []
        for ind, token in enumerate(tokens_):
            if token == "#":
                try:
                    tokens.append(tokens_[ind] + tokens_[ind + 1])
                except:
                    tokens.append(token)
                tokens_.pop(ind + 1)
            else:
                tokens.append(token)
        parsed = []
        for token in tokens:
            type = "UNK"
            nb_type = ""
            op_type = ""
            if token[0] in self.numbers:
                type = "NB"
                nb_type = "INT"
                if "." in token:
                    nb_type = "DEC"
            if not type == "NB":
                if token[0] == "#":
                    token = self.getStringFromRefID(token)
                    type = "STR"
            for k, op in self.lexical["syn_operators"].items():
                for op_ in op:
                    if token == op_:
                        type = "OP"
                        op_type = k
            r = [token, type]
            if op_type != "":
                r.append(op_type)
            if nb_type != "":
                r.append(nb_type)
            parsed.append(r)
        parsed2 = []

        # Ici, utilise l'algorithme Shunting Yard pour convertir en notation postfixe
        precedence = {
            "mul": 2,
            "divide": 2,
            "power": 2,
            "is_equal": 2,
            "is_not_equal": 2,
            "more_equal": 2,
            "less_equal": 2,
            "more": 2,
            "less": 2,
            "concat": 2,
            "plus": 1,
            "minus": 1
        }

        stack = []
        for token in parsed:
            if token[1] == "NB":
                parsed2.append(token)
            elif token[1] == "STR":
                parsed2.append(token)
            elif token[1] == "OP":
                if token[2] == "bracket_open":
                    stack.append(token)
                elif token[2] == "bracket_close":
                    while stack and stack[-1][2] != "bracket_open":
                        parsed2.append(stack.pop())
                    if stack:
                        stack.pop()  # Dépiler la parenthèse ouvrante
                else:
                    while stack and precedence.get(stack[-1][2], 0) >= precedence.get(token[2], 0):
                        parsed2.append(stack.pop())
                    stack.append(token)
        while stack:
            parsed2.append(stack.pop())

        return parsed2

    def exec(self, parsed_exp):
        stack = []
        for token in parsed_exp:
            if token[1] == "NB":
                stack.append(self.convertFloatToIntIfPossible(float(token[0])))
            elif token[1] == "STR":
                stack.append(str(token[0]))
            elif token[1] == "OP":
                if token[2] == "plus":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    try:
                        stack.append(a + b)
                    except:
                        stack.append(str(a) + str(b))
                elif token[2] == "minus":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(a - b)
                elif token[2] == "divide":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(a / b)
                elif token[2] == "mul":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(a * b)
                elif token[2] == "power":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(a ** b)
                elif token[2] == "is_equal":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a == b))
                elif token[2] == "is_not_equal":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a != b))
                elif token[2] == "more_equal":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a >= b))
                elif token[2] == "less_equal":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a <= b))
                elif token[2] == "more":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a > b))
                elif token[2] == "less":
                    try: b = stack.pop()
                    except: b = 1
                    try: a = stack.pop()
                    except: a = 1
                    stack.append(int(a < b))
                elif token[2] == "concat":
                    b = stack.pop()
                    a = stack.pop()
                    if type(a) in [int, float] and type(b) in [int, float]:
                        stack.append(int(str(int(a)) + str(int(b))))
                    elif type(a) == str and type(b) == str:
                        stack.append(str(a) + str(b))
                    elif type(a) in [int, float]:
                        try:
                            stack.append(self.convertFloatToIntIfPossible(float(str(a) + str(b))))
                        except:
                            stack.append(str(str(a) + str(b)))
                    else:
                        stack.append(str(str(a) + str(b)))
        return stack[0] if stack else None

class echoCommand():
    def __init__(self) -> None:
        self.name = "calc"
        self.command_class = commands.Command(self.name, self.echo, commands.Args(overflow=True), True)
        self.command_class.register()

    def echo(self, args:dict):
        expression = ""
        for arg in args.values():
            expression += arg.active_value + " "
        parsed_exp = Exp().parse(expression)
        result = Exp().exec(parsed_exp)
        if result:
            print(result)
        
echoCommand()