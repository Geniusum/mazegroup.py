import mazegroup.commands as commands
import os
import sys
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class MCP():
    def __init__(self) -> None:
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.temp_path = os.path.join(self.script_path, "temp")
        self.out_path = os.path.join(self.script_path, "out")
        self.ExistsDirOrMake(self.temp_path)
        self.ExistsDirOrMake(self.out_path)

    def ExistsDirOrMake(self, path):
        if not os.path.exists(path): os.mkdir(path)

    def Encrypt(self, source:str, key:str, salt):
        key = bytes(key, "utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(bytes(str(source), "utf-8")), salt

    def Decrypt(self, source:str, key:str, salt):
        if type(source) == bytes:
            source = source.decode("utf-8")
        if source.startswith("b'"):
            source = source[2:-1]
        key = bytes(key, "utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        cipher_suite = Fernet(key)
        return str(cipher_suite.decrypt(source))

    def SecureCompressProcess(self, path:str, output:str=None, password:str="", increment:int=0, tar:str=None):
        if not len(password):
            password = "KEY"
        if not tar:
            tar = bytes(password, "utf-8")
        if type(tar) == str:
            tar = bytes(tar, "utf-8")
        if increment <= 0:
            increment = len(password)
        data = []
        salt = os.urandom(16)
        name = os.path.splitext(path)[0]
        if not output:
            output = self.out_path
        msc = os.path.join(output, name + ".msc")
        if os.path.exists(msc):
                os.remove(msc)
        if not os.path.exists(path):
            exit("This path don't exists.")
        if os.path.isfile(path):
            if os.path.exists(os.path.join(self.temp_path, name)):
                os.remove(os.path.join(self.temp_path, name))
            os.mkdir(os.path.join(self.temp_path, name))
            shutil.copy(path, os.path.join(self.temp_path, name))
            path = os.path.join(self.temp_path, name)
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                data.append([file_path, open(os.path.abspath(file_path)).read()])
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                data.append([dir_path])
        encrypted = self.Encrypt(str(data), password, salt)
        for _ in range(increment - 1):
            encrypted = self.Encrypt(encrypted[0].decode("utf-8"), password, salt)
        content = {
            "salt": salt,
            "data": encrypted[0]
        }
        content_encrypted = self.Encrypt(str(content), password, tar)[0]
        f = open(msc, "w+")
        f.write(str(content_encrypted))
        f.close()
        print(f"Secure compress : the path is '{msc}'")
        #return content_encrypted
    
    def SCP_Decompress(self, path:str, output:str=None, password:str="", increment:int=0, tar:str=None):
        if not len(password):
            password = "KEY"
        if not tar:
            tar = bytes(password, "utf-8")
        if type(tar) == str:
            tar = bytes(tar, "utf-8")
        if increment <= 0:
            increment = len(password)
        
        if not output:
            output = self.out_path
        
        msc_file = os.path.splitext(path)[0] + ".msc"
        if not os.path.exists(msc_file):
            exit("The specified .msc file does not exist.")

        output = os.path.join(output, os.path.splitext(os.path.basename(msc_file))[0])
        
        with open(msc_file, "r") as f:
            content_encrypted = f.read().replace("b'", "").replace("'", "")
        
        content = self.Decrypt(content_encrypted, password, tar)
        content = eval(content)
        content = content.decode("utf-8")
        content = dict(eval(content))  # Convert string representation of dictionary to dictionary
        
        salt = content["salt"]
        data_encrypted = content["data"]
        
        for _ in range(increment):
            data_encrypted = self.Decrypt(data_encrypted, password, salt)

        data_encrypted = bytes(eval(data_encrypted))

        data = eval(data_encrypted)  # Convert string representation of data to list

        if not os.path.exists(output):
            os.mkdir(output)
        
        for item in data:
            if len(item) == 2:
                file_path, file_content = item
                file_content = file_content
                with open(os.path.join(os.path.dirname(output), file_path), "w") as f:
                    f.write(file_content)
            elif len(item) == 1:
                dir_path = item[0]
                os.makedirs(os.path.join(os.path.dirname(output), dir_path), exist_ok=True)

        print(f"Secure compress : the path is '{os.path.dirname(output)}'")

        #shutil.move(rc_temp, output)  # Move the decrypted files to the specified output directory

class Command():
    def __init__(self) -> None:
        self.name = "sc"
        self.command_class = commands.Command(self.name, self.func, commands.Args(overflow=True), True)
        self.command_class.register()

    def func(self, args_:dict):
        args = []
        for arg in args_.values():
            args.append(arg.active_value)
        if not args:
            print("Usage : mazegroup sc <compress/decompress> <path> <!* output path> <!* password> <!* increments> <!* tar>")
        else:
            if len(args) >= 2:
                if args[0] == "compress":
                    path = args[1]
                    try: output = args[2]
                    except: output = None
                    try: password = args[3]
                    except: password = "KEY"
                    try: increments = args[4]
                    except: increments = len(password)
                    try: tar = args[5]
                    except: tar = bytes(password, "utf-8")
                    ins = MCP()
                    ins.SecureCompressProcess(path, output, password, increments, tar)
                elif args[0] == "decompress":
                    path = args[1]
                    try: output = args[2]
                    except: output = None
                    try: password = args[3]
                    except: password = "KEY"
                    try: increments = args[4]
                    except: increments = len(password)
                    try: tar = args[5]
                    except: tar = bytes(password, "utf-8")
                    ins = MCP()
                    ins.SCP_Decompress(path, output, password, increments, tar)
                else:
                    print("Usage : mazegroup sc <compress/decompress> <path> <!* output path> <!* password> <!* increments> <!* tar>")
            else:
                print("Usage : mazegroup sc <compress/decompress> <path> <!* output path> <!* password> <!* increments> <!* tar>")
            
Command()
