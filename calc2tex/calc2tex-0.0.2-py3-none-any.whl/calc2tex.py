# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 08:34:03 2020

@author: stefa
"""
#TODO val_in erst bestimmen, wenn präzision bekannt oder Standardpräzision? -> Präzision in input.txt bestimmen
#TODO Exceptions-liste

from calc2tex import parse_txt
from .settings import language, accuracy
import json


class Calc2tex:
    def __init__(self, filename: str, lang: str="DE"):
        self.data = parse_txt.main(filename)
        self.lang = lang
    
    
    def to_json(self, output: str) -> None:
        """Exports the data-dictionary ta a json-file."""
        if "." not in output:
            output += ".json"
        with open(output, "w") as file:
            file.write(json.dumps(self.data, indent=4))
    
    
    def _search(self, py_var: str, lookup: str) -> str:
        """Searches for a variable and its sub-key inside the data-dictionary."""
        if py_var in self.data:
            return self.data[py_var][lookup]
        else:
            return "??"
            #TODO zum exceptions-dict hinzufügen
    
    
    def name(self, py_var: str) -> str:
        """Returns the name of a variable"""
        return self._search(py_var, "tex_var")
    
    
    def var(self, py_var: str) -> str:
        """Returns the formula with inputed variables."""
        return self._search(py_var, "var_in")
    
    
    def val(self, py_var: str) -> str:
        """Returns the formula with inputed values."""
        return self._search(py_var, "val_in")
    
    
    def raw(self, py_var: str, precision: int=3):
        """Returns the result with a certain precision"""
        return str(round(self._search(py_var, "res"), precision))
    
    
    def res(self, py_var: str, precision: int=accuracy) -> str:
        """Returns the result and its unit with a certain precision"""
        return "".join(("\\SI{", self.raw(py_var, precision), "}{", self.unit(py_var), "}"))
    
    
    def unit(self, py_var: str) -> str:
        """Returns the unit."""
        return self._search(py_var, "tex_un")
    
    
    def short(self, py_var: str, precision: int=accuracy) -> str:
        """Displays the name and value of a variable."""
        return " ".join((self.name(py_var), "=", self.res(py_var, precision)))
    
    
    def long(self, py_var: str, precision: int=accuracy) -> str:
        """Displays complete formula."""
        if self._search(py_var, "var") == "form":
            if self.var(py_var) == self.val(py_var):
                return " ".join((self.name(py_var), "=&", self.val(py_var), "=", self.res(py_var, precision)))
            else:
                return " ".join((self.name(py_var), "=&", self.var(py_var), "=", self.val(py_var), "=", self.res(py_var, precision)))
        else:
            return self.short(py_var, precision)
    
    
    def mult(self, first: str, last: str, precision: int=accuracy) -> str:
        """Displays multiple formulas at once."""
        #TODO var: val zulassen??, dafür table nur bis erstem var: form
        back = ""
        found = False
        
        for key, value in self.data.items():
            if key == first:
                found = True
            if found == True and self._search(key, "var") == "form":
                back += self.com(key, precision) + "\n"
            if key == last:
                break
                
        return back[:-2]
    
    
    #TODO zweispaltige Tabelle, dafür val-counter in read_file einbauen
    def table(self, columns: int=1) -> str:
        """
        Extracts the variables with predefined values from the main dictionary and parses them into a long string,
        which evaluates ta a table in LaTeX.

        Returns
        -------
        str
            The complete code block for displaying all input values.

        """
        start = ("\\begin{table}[htbp]", "\t\\centering", "\t\\caption{"+language[self.lang]['table']['header']+"}", 
                 "\t\\label{tab:input_val}", "\t\\begin{tabular}{lcc}", "\t\t\\toprule", 
                 "\t\t" + language[self.lang]['table']['var'] + " & " + language[self.lang]['table']['val'] + " & " + language[self.lang]['table']['unit'] + "\\\\", 
                 "\t\t\\midrule", "")
        end = ("\t\t\\bottomrule", "\t\\end{tabular}", "\\end{table}")
        
        tab = "\n".join(start)
        for value in self.data.values():
            if type(value) == dict:
                if value["var"] == "val":
                    tab += "".join(("\t\t$", value["tex_var"], "$ &", str(value["res"]), " & $\\si{", value["tex_un"], "}$\\\\ \n"))
                    # tab += "\t\t$" + value["tex_var"] + "$ & "
                    # tab += str(value["res"]) + " & $\\si{"
                    # tab += value["tex_un"] + "}$\\\\ \n"
            
        tab += "\n".join(end)
        return tab
    