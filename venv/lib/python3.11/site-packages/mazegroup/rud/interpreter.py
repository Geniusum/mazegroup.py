import time
import random

class Interpreter():
    def __init__(self, code:str):
        self.code = code
        self.lines = self.code.splitlines()

        self.active_line = 0

        self.stacks = {
            "opx": { # Operation
                "limit": 8,
                "stack": [],
                "locked": True
            },
            "opr": { # Operation
                "limit": 8,
                "stack": [],
                "locked": True
            },
            "iso": { # Isolation results
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "stk": { # Stacking data
                "limit": 64,
                "stack": [],
                "locked": True
            },
            "flx": { # Flux
                "limit": 64,
                "stack": [],
                "locked": True
            },
            "dmp": { # Dump
                "limit": 128,
                "stack": [],
                "locked": True
            },
            "max": { # Rest
                "limit": 0,
                "stack": [],
                "locked": True
            },
            "cha": { # Chunk A
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "chb": { # Chunk B
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "chc": { # Chunk C
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "chx": { # Chunk X
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "chy": { # Chunk Y
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "chz": { # Chunk Z
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "c1d": { # Chunk 1 dimensional
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "c2d": { # Chunk 2 dimensional
                "limit": 256,
                "stack": [],
                "locked": True
            },
            "c3d": { # Chunk 3 dimensional
                "limit": 4096,
                "stack": [],
                "locked": True
            }
        }

        self.lexer = {
            "comment": ";",
            "push": "push",
            "pop": "pop",
            "move": "mov",
            "copy": "cop",
            "print": "out",
            "input": "in",
            "jump": "jmp",
            "case": "cs",
            "ncase": "ncs",
            "lower": "lwr",
            "upper": "upr",
            "add": "add",
            "rev": "rev",
            "mul": "mul",
            "div": "div",
            "chr": "chr",
            "nb": "nb",
            "fill": "fill",
            "init": "ini",
            "copyall": "cpa",
            "reset": "res", # Must be clear
            "clear": "clr",
            "pass": "pass",
            "end": "end",
            "gst": "gst" # Get / Set / Call
        }

        self.err_pass = False
        self.err_count = 0

    def parseName(self, name:str):
        return name.lower().strip()

    def stackExists(self, stack:str):
        stack = self.parseName(stack)
        if stack in self.stacks.keys():
            return stack
        else:
            self.error("Stack", f"The stack {stack} don't exists.")

    def stackLocked(self, stack:str):
        return self.stacks[stack]["locked"]
    
    def stackInitialized(self, stack:str):
        if not self.stackLocked(stack): return stack
        else: self.error("Stack", f"Stack not initialized {stack}.")

    def fill(self, stack_name:str):
        stack = self.stacks[stack_name]
        limit = stack["limit"]
        lenght = len(stack["stack"])
        if not limit == 0:
            for seed in range(limit - lenght):
                random.seed(seed)
                stack["stack"].append(random.random())

    def intToChr(self, integer:int):
        try:
            char = chr(integer)
        except:
            self.error("Integer to char", "Invalid integer, impossible to get the Unicode character.")
        else:
            return char
        
    def chrsToNb(self, chrs:str):
        try:
            number = float(chrs)
            if int(chrs) == number:
                number = int(chrs)
        except:
            self.error("Char(s) to integer", "Invalid char(s) format, impossible to convert it to an integer or a decimal.")
        else:
            return number
        
    def initStack(self, stack_name:str):
        stack = self.stacks[stack_name]
        lock = stack["locked"]
        if not lock:
            self.error("Stack", "Stack already initialized.")
        else:
            stack["locked"] = False
    
    def rev(self, number:any): return -number

    def out(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack = stack_dict["stack"]
        
        try: last = stack[-1]
        except: self.error("Out",  f"Empty stack {stack_name}.")
        else: print(last, end="")
    
    def push(self, stack_name:str, value:any):
        stack_dict = self.stacks[stack_name]
        limit = stack_dict["limit"]
        lenght = len(stack_dict["stack"])
        if not lenght >= limit or limit == 0:
            stack = stack_dict["stack"]
            stack.append(value)
        else:
            self.error("Push", f"The stack {stack_name} can't get more elements than the limit : {limit}.")

    def pop(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack = stack_dict["stack"]
        try: stack.pop()
        except: self.error("Pop", f"Empty stack {stack_name}.")

    def copy(self, destination_name:str, from_name:str):
        stack_dict = self.stacks[from_name]
        stack = stack_dict["stack"]
        
        try: last = stack[-1]
        except: self.error("Out", f"Empty stack {from_name}.")
        else: self.push(destination_name, last)

    def copyall(self, destination_name:str, from_name:str):
        stack_dict = self.stacks[from_name]
        stack = stack_dict["stack"]
        
        if not len(stack):
            self.error("Out", f"Empty stack {from_name}.")
        else:
            for element in stack:
                self.push(destination_name, element)
    
    def move(self, destination_name:str, from_name:str):
        self.copy(destination_name, from_name)
        self.pop(from_name)

    def getLast(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack = stack_dict["stack"]
        try: return stack[-1]
        except: self.error("Stack", f"Empty stack {stack_name}.")

    def getStackList(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack = stack_dict["stack"]
        try: return stack
        except: self.error("Stack", f"Empty stack {stack_name}.")

    def reset(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack_dict["locked"] = True
        stack_dict["stack"] = []

    def clear(self, stack_name:str):
        stack_dict = self.stacks[stack_name]
        stack_dict["stack"] = []

    def error(self, err_type:str, err_message:str, err_line:int=-1):
        self.err_count += 1
        if not self.err_pass:# and err_type.lower() != "stack":
            if err_line == -1:
                err_line = self.active_line
            print(f"Error [{err_type}] line {err_line} : {err_message}\n\t{self.lines[err_line - 1]}", end="")

            self.endProgram()

            exit(0)

    def toInteger(self, input):
        try:
            input = int(input)
        except:
            pass
        if isinstance(input, int):
            return input
        elif isinstance(input, float):
            return float(input)
        elif isinstance(input, str):
            if len(input) > 0:
                if len(input) == 1:
                    return ord(input)
                else:
                    return str(input)
            else:
                return 0
        else:
            return 0

    def endProgram(self):
        if self.log:
            end_time = time.time()
            elements_count = 0
            for stack in self.stacks.values():
                elements_count += len(stack["stack"])
            print(f"\n\nProgram finished in {round(end_time - self.start_time, 30)}s with {self.err_count} error(s) and {elements_count} elements remaining in stacks.")

    def removeComments(self):
        lines_to_keep = {}

        for nb, line in enumerate(self.lines):
            try:
                if line[0] in self.lexer["comment"]:
                    continue
                else:
                    newline = ""
                    for ic, char in enumerate(line):
                        prechar = line[ic - 1] if ic > 0 else None
                        nextchar = line[ic + 1] if ic < len(line) - 1 else None

                        if char in self.lexer.comments:
                            break
                        newline += char
                    lines_to_keep[nb] = newline.strip()

                return lines_to_keep
            except Exception as e:
                self.error("Comment parsing", f"Comment removing error : {e}", nb)
    
    def printStacks(self):
        print("---")
        for stack_name, stack_dict in self.stacks.items():
            sep = "\n\t\t"
            stack_init = stack_dict["locked"]
            _stack = stack_dict["stack"]
            stack = []
            for v in _stack:
                stack.append(str(v))
            if len(stack):
                print(f"\t{stack_name.upper()} INIT {int(not stack_init)} :\n\t\t{sep.join(stack)}")
            else:
                print(f"\t{stack_name.upper()} INIT {int(not stack_init)} : -")
        print()
        
    def execute(self, log:bool=False, debug:bool=False):
        if log:
            self.start_time = time.time()
            print("Program started...\n")

        self.log = log

        lines = self.lines
        index = 1
        while index <= len(lines):
            try:
                line = lines[index - 1]
                self.active_line = index
                tokens = line.split()
                if debug:
                    print(index, line)
                    self.printStacks()
                if len(tokens):
                    command = tokens[0].lower()
                    args = tokens[1:]
                    if command == self.lexer["comment"]:
                        pass
                    elif command == self.lexer["push"]:
                        if len(args) >= 2:
                            stack_name = self.stackInitialized(self.stackExists(args[0]))
                            values = []
                            for value in args[1:]:
                                values.append(self.toInteger(value))
                            for value in values:
                                self.push(stack_name, value)
                        else:
                            self.error("Push", "At minimum 2 arguments.")
                    elif command == self.lexer["pop"]:
                        if len(args) >= 1:
                            stacks_name = []
                            for name in args:
                                stacks_name.append(self.stackInitialized(self.stackExists(name)))
                            for stack_name in stacks_name:
                                self.pop(stack_name)
                        else:
                            self.error("Pop", "At minimum 1 arguments.")
                    elif command == self.lexer["move"]:
                        if len(args) >= 2:
                            dest_stack_name = self.stackInitialized(self.stackExists(args[0]))
                            sources_stack_name = []
                            for source_stack in args[1:]:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                self.move(dest_stack_name, source_stack)
                        else:
                            self.error("Move", "At minimum 2 arguments.")
                    elif command == self.lexer["copy"]:
                        if len(args) >= 2:
                            dest_stack_name = self.stackInitialized(self.stackExists(args[0]))
                            sources_stack_name = []
                            for source_stack in args[1:]:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                self.copy(dest_stack_name, source_stack)
                        else:
                            self.error("Copy", "At minimum 2 arguments.")
                    elif command == self.lexer["print"]:
                        if len(args) == 0:
                            in_stack = self.stackInitialized(self.stackExists("dmp"))
                            self.out(in_stack)
                        else:
                            self.error("Output", "Take no argument.")
                    elif command == self.lexer["input"]:
                        if len(args) == 0:
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            self.push(out_stack, self.toInteger(input()))
                        else:
                            self.error("Input", "Take no argument.")
                    elif command == self.lexer["jump"]:
                        if len(args) == 1:
                            sel_line = int(self.toInteger(args[0])) - 1
                            index = sel_line
                        else:
                            self.error("Jump", "Take one argument.")
                    elif command == self.lexer["case"]:
                        if len(args) == 1:
                            sel_line = int(self.toInteger(args[0])) - 1
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            if stack_a == stack_b:
                                index = sel_line
                        else:
                            self.error("Case", "Take one argument.")
                    elif command == self.lexer["ncase"]:
                        if len(args) == 1:
                            sel_line = int(self.toInteger(args[0])) - 1
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            if stack_a != stack_b:
                                index = sel_line
                        else:
                            self.error("NCase", "Take one argument.")
                    elif command == self.lexer["lower"]:
                        if len(args) == 1:
                            sel_line = int(self.toInteger(args[0])) - 1
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            if stack_a < stack_b:
                                index = sel_line
                        else:
                            self.error("Lower", "Take one argument.")
                    elif command == self.lexer["upper"]:
                        if len(args) == 1:
                            sel_line = int(self.toInteger(args[0])) - 1
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            if stack_a > stack_b:
                                index = sel_line
                        else:
                            self.error("Upper", "Take one argument.")
                    elif command == self.lexer["add"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if (type(stack_a) in [int, float] and type(stack_b) == str) or (type(stack_a) == str and type(stack_b) in [int, float]):
                                stack_a, stack_b = str(stack_a), str(stack_b)
                            self.push(out_stack, stack_a + stack_b)
                        else:
                            self.error("Add", "Take no argument.")
                    elif command == self.lexer["rev"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("dmp")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            self.push(out_stack, self.rev(stack_a))
                        else:
                            self.error("Rev", "Take no argument.")
                    elif command == self.lexer["mul"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            self.push(out_stack, stack_a * stack_b)
                        else:
                            self.error("Mul", "Take no argument.")
                    elif command == self.lexer["div"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("opx")))
                            stack_b = self.getLast(self.stackInitialized(self.stackExists("opr")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if type(stack_a) == str:
                                stack_a = ord(stack_a)
                            if type(stack_b) == str:
                                stack_b = ord(stack_b)
                            self.push(out_stack, stack_a / stack_b)
                        else:
                            self.error("Div", "Take no argument.")
                    elif command == self.lexer["chr"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("dmp")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if type(stack_a) == str:
                                self.error("Char", "Already a char.")
                                self.push(out_stack, stack_a)
                            else:
                                self.push(out_stack, self.intToChr(stack_a))
                        else:
                            self.error("Char", "Take no argument.")
                    elif command == self.lexer["nb"]:
                        if len(args) == 0:
                            stack_a = self.getLast(self.stackInitialized(self.stackExists("dmp")))
                            out_stack = self.stackInitialized(self.stackExists("iso"))
                            if type(stack_a) in [int, float]:
                                self.error("Nb", "Already a number.")
                            self.push(out_stack, self.chrsToNb(stack_a))
                        else:
                            self.error("Nb", "Take no argument.")
                    elif command == self.lexer["fill"]:
                        if len(args) >= 1:
                            sources_stack_name = []
                            for source_stack in args:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                self.fill(source_stack)
                        else:
                            self.error("Fill", "At minimum one argument.")
                    elif command == self.lexer["init"]:
                        if len(args) >= 1:
                            sources_stack_name = []
                            for source_stack in args:
                                sources_stack_name.append(self.stackExists(source_stack))
                            for source_stack in sources_stack_name:
                                self.initStack(source_stack)
                        else:
                            self.error("Init", "At minimum one argument.")
                    elif command == self.lexer["copyall"]:
                        if len(args) >= 2:
                            dest_stack_name = self.stackInitialized(self.stackExists(args[0]))
                            sources_stack_name = []
                            for source_stack in args[1:]:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                self.copyall(dest_stack_name, source_stack)
                        else:
                            self.error("CopyAll", "At minimum 2 arguments.")
                    elif command == self.lexer["reset"]:
                        if len(args) >= 1:
                            sources_stack_name = []
                            for source_stack in args:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                if not len(self.getStackList(source_stack)) == 0:
                                    self.error("Reset", f"Stack not empty : {source_stack}.")
                                else:
                                    self.reset(source_stack)
                        else:
                            self.error("Reset", "At minimum one arguments.")
                    elif command == self.lexer["clear"]:
                        if len(args) >= 1:
                            sources_stack_name = []
                            for source_stack in args:
                                sources_stack_name.append(self.stackInitialized(self.stackExists(source_stack)))
                            for source_stack in sources_stack_name:
                                self.clear(source_stack)
                        else:
                            self.error("Clear", "At minimum one arguments.")
                    elif command == self.lexer["pass"]:
                        if len(args) == 0:
                            if not self.err_pass: self.err_pass = True
                            else: self.err_pass = False
                        else:
                            self.error("Pass", "Take no argument.")
                    elif command == self.lexer["end"]:
                        if len(args) == 0:
                            self.endProgram()
                            exit(0)
                        else:
                            self.error("End", "Take no argument.")
                    elif command == self.lexer["gst"]:
                        if len(args) >= 1:
                            try:
                                _type = args[0].lower()
                                if _type == "stklen":
                                    stack_name = self.stackInitialized(self.stackExists(args[1]))
                                    out_stack = self.stackInitialized(self.stackExists("iso"))
                                    self.push(out_stack, len(self.getStackList(stack_name)))
                                else:
                                    self.error("Gst", f"Invalid gst type.")
                            except Exception as e:
                                self.error("Gst", f"Bad argument(s) / Exception : {e}.")
                        else:
                            self.error("Gst", "At minimum one argument.")
            except Exception as e:
                self.error("Interpreter", f"Exception : {e}.")
            index += 1

        self.endProgram()

def interprete(argv):
    args = []
    options = []

    for i, arg in enumerate(argv):
        if i > 0:
            options.append(arg)
        else:
            args.append(arg)

    if len(args):
        file_path = args[0]
        
        log = False
        debug = False
        for option in options:
            if option == "-l":
                log = True
            elif option == "-d":
                debug = True
        if len(args) >= 2:
            options = args[1:]
        ins = Interpreter(open(file_path, encoding='utf-8-sig').read())
        ins.execute(log, debug)
    else:
        print("Usage : mazegroup rud <sourcecode> <options>")