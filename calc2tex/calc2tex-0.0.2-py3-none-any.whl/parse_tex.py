# -*- coding: utf-8 -*-
"""
Created on Thu May  7 22:36:15 2020

@author: stefa
"""
from .helper import search_bracket, search_char
from .calc2tex import Calc2tex

def process_tex(in_file: str, out_file: str) ->None:
    commands = []
    #TODO table und anderen functionen die anzahl an leerzeichen vor einer Zeile mitgeben
    with open(in_file) as stdin, open(out_file, "w") as stdout:
        for line in stdin:
            while True:
                if "Calc2tex(" in line:
                    index = line.index("Calc2tex(")
                    bracket = search_bracket(line, index+8, 1)
                    end = line.rindex("=", 0, index)
                    while line[end] == " ":
                        end -= 1
                
                    start = line.rfind(" ", 0, end-1) + 1
                    if start == 0:
                        start = line.rindex("\t", 0, end-1) + 1
                
                    commands.append(line[start:end-1] + ".")
                    exec(line[start:bracket+1])
                    line = line.replace(line[start:bracket+1], "")
                else:
                    break
               
            for command in commands:
                while True:
                    if command in line:
                        index = line.index(command)
                        opening = search_char(line, index, ["("])
                        closing = search_bracket(line, opening, 1)
                        line = line.replace(line[index:closing+1], eval(line[index:closing+1]))
                    else:
                        break
            
            stdout.write(line)
            
            