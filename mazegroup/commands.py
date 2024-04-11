import mazegroup.utils as utils
import pickle
import os
import copy

COMMANDS = {}

script_path = os.path.dirname(os.path.abspath(__file__))

def loadPickleVar():
    global COMMANDS
    pth = os.path.join(script_path, "saves", "commands.pkl")
    if os.path.exists(pth):
        COMMANDS = pickle.load(open(pth, "rb"))

def savePickleVar():
    pth = os.path.join(script_path, "saves", "commands.pkl")
    with open(pth, 'wb') as f:
        pickle.dump(COMMANDS, f)

def delPickleVar():
    global COMMANDS
    pth = os.path.join(script_path, "saves", "commands.pkl")
    if os.path.exists(pth):
        os.remove(pth)
    COMMANDS = {}

loadPickleVar()
savePickleVar()

class Arg():
    def __init__(self, name:str, default:any=None, required:bool=False) -> None:
        self.name = name
        self.default = default
        self.required = required

        self.active_value = None

    def parse(self, value:str):
        r = value
        py_eval_prefix = "py:"
        if value.lower().startswith(py_eval_prefix):
            try:
                r = eval(value[len(py_eval_prefix):])
            except Exception as e:
                return utils.Error(f"Python Eval Exception : {e}")
        return r

    def tryToSet(self, value:any=None):
        if not value and self.required:
            return utils.Error("The value is required")
        elif not value:
            self.active_value = self.parse(self.default)
            if type(self.active_value) == utils.Error:
                return self.active_value
        else:
            self.active_value = self.parse(value)
            if type(self.active_value) == utils.Error:
                return self.active_value
        return utils.NoError()
    
class Args():
    def __init__(self, args:list=[], overflow:bool=False) -> None:
        self.args_ = args
        self.args = {}
        for arg in self.args_:
            self.args[arg.name] = arg
        self.overflow = overflow

    def addArg(self, arg:Arg): self.args.append(arg)

    def tryArgs(self, args:list):
        ag = []
        for arg in self.args.values():
            if arg.required: ag.append(arg)
        if len(args) > len(self.args) and not self.overflow:
            return utils.Error(f"Argument(s) overflow, {len(args)} was given but {len(self.args)} was waited")
        elif len(args) < len(ag):
            return utils.Error(f"Missing argument(s), {len(args)} was given but {len(ag)} was waited")
        for arg_index, value in enumerate(args):
            if type(value) == dict:
                try:
                    arg_index = value.keys()[0]
                except:
                    return utils.Error()
            try:
                if type(arg_index) == str:
                    r = self.args[arg_index].tryToSet(value)
                else:
                    i = ""
                    for k, j in enumerate(self.args.keys()):
                        if k == arg_index:
                            i = j
                    r = self.args[i].tryToSet(value)
            except:
                id = utils.RandIDv1Tiny()
                arg = Arg(id)
                r = arg.tryToSet(value)
                self.args[id] = arg
            if type(r) != utils.NoError:
                return r
        return utils.NoError()
    
    def getArgsNames(self) -> list:
        r = []
        for arg in self.args.keys():
            r.append(arg)
        return r

class Command():
    def __init__(self, name:str=None, function=utils.Void, args:Args=Args(), unique:bool=True) -> None:
        self.function = copy.deepcopy(function)
        if not name:
            name = f'{function=}'.split('=')[0].strip().lower()
        self.name = name
        self.args = args
        self.unique = unique

    def register(self):
        #loadPickleVar()
        if self.name in COMMANDS.keys():
            return utils.Error(f"A command was already registered at the name '{self.name}'")
        self_copy = copy.deepcopy(self)
        COMMANDS[self.name] = {
            "function": self_copy.function,
            "args": self_copy.args,
            "class" : self_copy
        }
        savePickleVar()
        return utils.NoError()
    
    def execute(self, args:any):
        if type(args) == str:
            args = args.split()
        elif type(args) == list:
            pass
        elif type(args) == dict:
            args = args.keys()
        else:
            return utils.Error(f"Bad arguments type on the '{self.name}' command execution")
        r = self.args.tryArgs(args)
        if type(r) != utils.NoError:
            _ = self.args.getArgsNames(); __ = ""
            args_ = []
            for arg in self.args.args_:
                if arg.required: args_.append(arg)
            if not len(args_) < len(self.args.args):
                for arg in _: __ += f"<{arg}>"
            else:
                __ = f"<...>"
            return utils.Error(f"{r.message}\nUsage : mazegroup {self.name} {__}")
        try:
            if self.unique:
                self.function(self.args.args)
            else:
                self.function(*self.args.args)
        except Exception as e:
            return utils.Error(f"Exception during the execution of the command '{self.name}' : {e}")
        return utils.NoError()

def executeCommand(command:str, args:list):
    loadPickleVar()
    command = command.lower()
    if command in COMMANDS.keys():
        r = COMMANDS[command]["class"].execute(args)
        if type(r) != utils.NoError:
            return r
    else:
        return utils.Error("Command not found")
    return utils.NoError()
