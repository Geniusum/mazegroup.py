import mazegroup.commands as commands
import mazegroup.utils as utils
import time, os, requests, json.decoder, colorama, psutil, random, platform

mazegroup_logo = r"""
    __  ___                 ______                    
   /  |/  /___ _____  ___  / ____/________  __  ______ 
  / /|_/ / __ `/_  / / _ \/ / __/ ___/ __ \/ / / / __ \
 / /  / / /_/ / / /_/  __/ /_/ / /  / /_/ / /_/ / /_/ /
/_/  /_/\__,_/ /___/\___/\____/_/   \____/\__,_/ .___/ 
                                              /_/      

"""


class Command():
    def __init__(self) -> None:
        self.name = "vwft"
        self.command_class = commands.Command(
            self.name, self.func, commands.Args(overflow=True), True)
        self.command_class.register()

    def delay_1(self):
        time.sleep(0.05)

    def print_line_by_line(self, s: str):
        for line in s.splitlines():
            print(line)
            self.delay_1()
    
    def ping_mazegroup(self) -> list[int, int, int]:
        s_time = time.time()
        r = requests.get("https://mazegroup.org/ping")
        if r.status_code != 200:
            return [0, 0, 0]
        c = json.decoder.JSONDecoder().decode(r.text)
        c_time = c["time"]
        e_time = time.time()
        return [s_time, c_time, e_time]

    def func(self, args: dict):
        r_clear = commands.executeCommand("clear", [])
        if type(r_clear) != utils.NoError:
            print("Error :", r_clear.message)
        print(colorama.Fore.RED + " _ _  _ _ _  ___  ___ ")
        self.delay_1()
        print("| | || | | || __>|_ _|")
        self.delay_1()
        print("| ' || | | || _>  | | ")
        self.delay_1()
        print("|__/ |__/_/ |_|   |_| ViewFetch from the MazeGroup.py Shell")
        self.delay_1()
        print("===========================================================")
        self.delay_1()
        print("    2024 - MazeGroup Research Intitute""")
        self.delay_1()
        print(colorama.Fore.RESET)
        self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== SHELL LOGO ===" + colorama.Fore.RESET)
        self.delay_1()
        self.print_line_by_line(mazegroup_logo)
        print(colorama.Fore.LIGHTRED_EX + "=== WEBSITES ===" + colorama.Fore.RESET)
        self.delay_1()
        print("https://mazegroup.org/")
        self.delay_1()
        print("https://github.com/Geniusum/mazegroup.py")
        self.delay_1()
        print()
        self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== VERSION ===" + colorama.Fore.RESET)
        self.delay_1()
        r_version = commands.executeCommand("version", [])
        if type(r_version) != utils.NoError:
            print("Error :", r_version.message)
        print()
        self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== MAZEGROUP PING ===" + colorama.Fore.RESET)
        self.delay_1()
        max_attempt = 3
        for _ in range(max_attempt):
            r = self.ping_mazegroup()
            print(f"ATTEMPT {_ + 1}/{max_attempt} :")
            self.delay_1()
            print(f"\tSTART TIME : {r[0]}s")
            print(f"\tSERVICE TIME : {r[1]}s")
            print(f"\tEND TIME : {r[2]}s")
            self.delay_1()
            print(f"\tSTART TO SERVICE : {abs(r[1] - r[0])}s")
            print(f"\tSERVICE TO END : {abs(r[2] - r[1])}s")
            print(f"\tSTART TO END : {abs(r[2] - r[1])}s")
            self.delay_1()
            print()
            self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== CHECKING CPU ===" + colorama.Fore.RESET)
        self.delay_1()
        max_cpu_check = 10
        cpu_check_list = []
        for _ in range(max_cpu_check):
            check = psutil.cpu_percent(0.2)
            print(f"[{random.randint(100000, 999999)} {_ + 1}/{max_cpu_check}] Current CPU Usage : {check}%", end="\r")
            cpu_check_list.append(check)
        print()
        print(f"Average CPU usage : {round(sum(cpu_check_list) / len(cpu_check_list), 2)}%")
        self.delay_1()
        print()
        self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== PC SPECS ===" + colorama.Fore.RESET)
        self.delay_1()
        print(f"Platform : {platform.platform()}")
        self.delay_1()
        print(f"System : {platform.system()}")
        self.delay_1()
        print(f"Machine architecture : {platform.machine()}")
        self.delay_1()
        print(f"Machine version : {platform.version()}")
        self.delay_1()
        print()
        self.delay_1()
        print(colorama.Fore.LIGHTRED_EX + "=== DONE ===" + colorama.Fore.RESET)
        self.delay_1()
        print()
        self.delay_1()

Command()
