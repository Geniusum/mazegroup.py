"""
Jygo is a Python general library who works with packages.
"""

import os
try:
    import colorama
    from colorama import Fore, Back
except:
    os.system("pip install colorama")
colorama.init()
import jygo.lib.package as package
import jygo.lib.base.inits as inits
import jygo.lib.base.logs as logs
from jygo.jygo import *

logs.Log("Starting Jygo initialization...").show()

inits.Init("jygo", os.path.dirname(__file__)).show()