"Imports"

import os, threading, time


"Classes"

class FluxFile():
    class FluxFileException(BaseException): ...
    class NotExistantPath(FluxFileException): ...
    class IsDirectory(FluxFileException): ...
    class FileReadingException(FluxFileException): ...
    class FileWritingException(FluxFileException): ...
    class TranslationException(FluxFileException): ...
    class FormatingException(FluxFileException): ...

    def __init__(self, path:str, delay:float=None) -> None:
        self.path = path.strip()

        if not os.path.exists(self.path):
            raise self.NotExistantPath(self.path)
        if os.path.isdir(self.path):
            raise self.IsDirectory(self.path)
        
        self.delay = delay
        self.content = ...

        self.last_result = None

    def try_get_content(self) -> str:
        try: return open(self.path, encoding="utf-8").read()
        except Exception as e: raise self.FileReadingException(e)
    
    def hex_address(self, address:str, line_nb:int, ref:bool=False, active_sector:str="") -> int:
        if not ref:
            address = address.upper()
            if not len(address) > 2:
                raise self.TranslationException(f"Not a valid hex format, line {line_nb}")
            if not address[:2] == "0X":
                raise self.TranslationException(f"Not a valid hex format, line {line_nb}")
            address = int(address[2:], 16)
            return address
        else:
            address = address.upper()
            tokens = address.split(":")
            sector = active_sector
            if len(tokens) == 1:
                address = tokens[0]
            elif len(tokens) == 2:
                address = tokens[1]
                sector = tokens[0]
            else:
                raise self.TranslationException(f"Not a valid reference syntax, line {line_nb}")
            address = address.upper()
            if not len(address) > 2:
                raise self.TranslationException(f"Not a valid hex format, line {line_nb}")
            if not address[:2] == "0X":
                raise self.TranslationException(f"Not a valid hex format, line {line_nb}")
            address = int(address[2:], 16)
            return {
                "sector": sector,
                "address": address
            }

    def translate(self) -> dict:
        r = {
            "flux_name": None,
            "sectors": {}
        }

        started = False
        active_sector = None

        self.lines = self.content.splitlines()
        if not len(self.lines):
            raise self.TranslationException("Empty file.")
        for index, line in enumerate(self.lines):
            line = line.strip()
            line_nb = index + 1
            if len(line):
                tag = False
                tag_content = ""
                if line.startswith("[") and line.endswith("]"):
                    tag = True
                    if not len(line) > 2:
                        raise self.TranslationException(f"Empty tag, line {line_nb}.")
                    tag_content = line[1:-1].upper()
                if tag:
                    if not len(tag_content):
                        raise self.TranslationException(f"Empty tag, line {line_nb}.")
                    parts = tag_content.split(";")
                    for part_index, part in enumerate(parts):
                        tokens = part.split()
                        if tokens[0] == "FLUX":
                            if len(tokens) != 2:
                                raise self.TranslationException(f"Waited 2 tokens here, line {line_nb}")
                            if not started:
                                started = True
                                r["flux_name"] = tokens[1]
                            else:
                                raise self.TranslationException(f"Redefining flux identity, line {line_nb}")
                        elif tokens[0] == "SECTOR":
                            if len(tokens) != 2:
                                raise self.TranslationException(f"Waited 2 tokens here, line {line_nb}")
                            active_sector = tokens[1]
                            if not active_sector in r["sectors"].keys():
                                r["sectors"][active_sector] = {
                                    "size": 0,
                                    "cells": {}
                                }
                        elif tokens[0] == "SIZE":
                            if active_sector == None:
                                raise self.TranslationException(f"No sector, line {line_nb}")
                            if len(tokens) != 2:
                                raise self.TranslationException(f"Waited 2 tokens here, line {line_nb}")
                            try:
                                size = int(tokens[1])
                            except:
                                raise self.TranslationException(f"Integer waited here, line {line_nb}")
                            if max(size, 0) != size:
                                raise self.TranslationException(f"Minimum size at 0, line {line_nb}")
                            r["sectors"][active_sector]["size"] = size
                elif line.strip().startswith("*"):
                    pass
                else:
                    tokens = line.split()
                    if not len(tokens) >= 2:
                        raise self.TranslationException(f"Waited 2 or more tokens here, line {line_nb}")
                    if active_sector == None:
                        raise self.TranslationException(f"No sector, line {line_nb}")
                    address = tokens[0].upper()
                    type = tokens[1].upper()
                    try:
                        value = " ".join(tokens[2:])
                    except:
                        value = None
                    address = self.hex_address(address, line_nb, False)
                    if type == "INTEGER":
                        if value == None: raise self.TranslationException(f"Empty value, line {line_nb}")
                        try: value = int(value)
                        except: raise self.TranslationException(f"Value error, line {line_nb}")
                    elif type == "STRING":
                        try: value = str(value)
                        except: raise self.TranslationException(f"Value error, line {line_nb}")
                    elif type == "DECIMAL":
                        if value == None: raise self.TranslationException(f"Empty value, line {line_nb}")
                        try: value = float(value)
                        except: raise self.TranslationException(f"Value error, line {line_nb}")
                    elif type == "BOOLEAN":
                        if value == None: raise self.TranslationException(f"Empty value, line {line_nb}")
                        try:
                            value = int(value)
                            if not value in [0, 1]:
                                raise self.TranslationException()
                            if value == 0: value = False
                            else: value = True
                        except: raise self.TranslationException(f"Value error, line {line_nb}")
                    elif type == "ADDR":
                        if value == None: raise self.TranslationException(f"Empty value, line {line_nb}")
                        addresses_ = str(value).split(";")
                        addresses = []
                        for address in addresses_:
                            address = address.strip()
                            if len(address):
                                address = self.hex_address(address, line_nb, True, active_sector)
                                if not address["sector"] in r["sectors"].keys():
                                    raise self.TranslationException(f"Sector not found, line {line_nb}")
                                addresses.append(address)
                        value = addresses
                    elif type == "EMPTY":
                        value = None
                    else:
                        raise self.TranslationException(f"Invalid value type, line {line_nb}")
                    r["sectors"][active_sector]["cells"][address] = {
                        "type": type,
                        "value": value
                    }
                    if not r["sectors"][active_sector]["size"] == 0:
                        if len(r["sectors"][active_sector]["cells"]) > r["sectors"][active_sector]["size"]:
                            raise self.TranslationException(f"Maximum size exceeded, line {line_nb}")
        
        if not started:
            raise self.TranslationException(f"Flux not started.")

        self.last_result = r
        return r

    def format(self, flux_trace:dict=None) -> str:
        if flux_trace == None:
            if self.last_result == None:
                raise self.FormatingException(f"Missing result.")
            flux_trace = self.last_result

        s = f"[FLUX {flux_trace['flux_name']}]\n"
        for sector_name, _ in flux_trace["sectors"].items():
            s += f"[SECTOR {sector_name}; SIZE {_['size']}]\n"
            for cell, __ in _["cells"].items():
                if not len(str(cell).strip()):
                    cell = 0
                address = hex(cell)
                type_ = __["type"]
                value = __["value"]
                if type_ == "BOOLEAN" and value:
                    value = "1"
                elif type_ == "BOOLEAN" and not value:
                    value = "0"
                if type_ == "EMPTY":
                    value = ""
                if type_ == "ADDR":
                    _v = ""
                    for addr in value:
                        _v += f"{addr['sector']}:{hex(addr['address'])}; "
                    value = _v
                value = str(value)
                s += f"    {address} {type_} {value}\n"

        return s

    def write_file(self, path:str, s:str):
        try:
            f = open(path, "w+")
            f.write(s)
            f.close()
        except Exception as e:
            raise self.FileWritingException(e)

    def write_file_dir(self, name:str, s:str):
        try:
            f = open(os.path.join(os.path.dirname(self.path), name), "w+")
            f.write(s)
            f.close()
        except Exception as e:
            raise self.FileWritingException(e)