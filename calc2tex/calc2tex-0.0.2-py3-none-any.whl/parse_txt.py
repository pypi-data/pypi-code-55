# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 22:37:36 2020

@author: stefa
"""
from .helper import is_float, search_char
from calc2tex import calc_formula

singleun  = {"m": "\\meter", "g": "\\gram", "A": "\\ampere", "C": "\\coulomb", "K": "\\kelvin", "s": "\\second", "J": "\\joule", "N": "\\newton",
             "V": "\\volt", "W": "\\watt", "h": "\\hour", "l": "\\litre", "t": "\\tonne", "d": "\\day", "a": "\\year", "°": "\\degree"}
singlepre = {"p": "\\pico", "n": "\\nano", "m": "\\milli", "c": "\\centi", "d": "\\dezi", "h": "\\hecto", "k": "\\kilo",
             "M": "\\mega", "G": "\\giga", "T": "\\tera", "P": "\\peta"}
doubleun  = {"ha": "\\hectare", "Pa": "\\pascal", "cd": "\\candela", "Bq": "\\bequerel", "Hz": "\\hertz",
             "lm": "\\lumen", "Sv": "\\sievert", "dB": "\\decibel", "°C": "\\degreeCelsius"}
doublepre = {"mu": "\\micro", "da": "\\deca"}
tribleun  = {"min": "\\minute", "mol": "\\mole", "bar": "\\bar", "ohm": "\\ohm", "rad": "\\radian",
             "gon": "\\gon"}

charUnits   = ["/", "*"]
charFormula = ["/", "*", "(", ")", "+", "-", "%"]


def read_file(filename: str) -> dict:
    """
    Parses a txt-file into a dictionary.

    Parameters
    ----------
    filename : str
        The path to a txt-file, containing a semicolon-separated list.

    Returns
    -------
    dict
        A dictionary, containing the parsed file.

    """
    data: dict = {"used_bib": []}                       #creates an empty container for the information in the file
    data: dict = {}
    input_list: list = []                               #a list for holding the pre-processed lines 
    
    with open(filename) as file:
        for line in file:                               #iterates over the lines in file
            save: list = line.split(";")                #splits line on every semi-colon
            save = [part.strip() for part in save]      #removes leading and trailing whitespace on every substring
            if save[0] == "":                           #empty lines and lines starting with the hash character are ignored
                continue
            elif save[0][0] != "#":
                input_list.append(save)
    
    #TODO in formel alle Leerzeichen entfernen
    #TODO Möglichkeit tex_var wegzulassen, wenn gleich
    #TODO bibs in eigene Liste, initialisierung anpassen, klasse.table anpassen
    #TODO Leerzeichen ersetzen nicht in Formel da dort if's etc.
    #TODO save input as dict with line-numbers, for exception handeling
    #TODO other decision making: look if line[2] can be converted to float
        #use: line[2].replace('.', '', 1).isdigit() no exponents
        #try catch- block: float(line[0]) as a helper function
    
    for line in input_list:                                 #extracts information from pre-processed file into data-container
        if len(line) == 1:                                  #differentiats different cases by length of list
            bibs = line[0].split(",")                       #splits at first on commas
            _, first = bibs.pop(0).split(":")               #the first element, which uses another delimiter, is seperatly processed
            bibs.insert(0, first)                           #and then added back again to the list
            bibs = [part.strip(" ") for part in bibs]       #removes whitespaces
            #data["used_bib"].extend(bibs)
            #TODO zweites dict mit Werten von Bibs, auf Reihenfolge von Einfügen achten falls Doppelkey,
                #erst im aktuellen Verzeichnis schauen-> Aufbau und Verarbeitung wie read-file, dann im Modulverzeichnis Biblio suchen
                #dort als json oder txt speichern, letzteres geringerer Platzbedarf, langsameres parsen; abhängig von Dateiendung verarbeiten
            #TODO keine Endung: Standardendung festlegen wahrscheinlich json -> so schon berechnetes txt-später verwendbar
            #TODO gewünschte Präzision angeben, verwendung dann in val_in??
            #TODO erste drei als reference by pos, Rest mit key = schreiben
        elif len(line) == 4:
            data[line[0]] = {"var": "val", "tex_var": line[1], "res": float(line[2]), "unit": line[3], "tex_un": None}
            #TODO line[3] only to next hash character
        elif len(line) == 5:
            data[line[0]] = {"var": "form", "tex_var": line[1], "res": None, "unit": line[4], "tex_un": None, "type": line[2], "form": line[3]}
    
    return data


#TODO unit conversion in eigenes Modul auslagern??
def subunit_to_tex(split: str) -> str:
    """
    Converts part of a unit from the symbol to the command of the siunitx-package

    Parameters
    ----------
    split : str
        Part of the inputed unit, one symbol or a number.

    Returns
    -------
    str
        The command from the siunitx-package representing the symbol.

    """
    length = len(split)
    if is_float(split):
        return "\\tothe{" + split + "}"
    
    if length == 1:
        return singleun[split]
    elif length == 2:
        try:
            return doubleun[split]
        except:
            pass
        return singlepre[split[0]] + singleun[split[1]]
    elif length == 3:
        try:
            return tribleun[split]
        except:
            pass
        try: 
            return doublepre[split[0:2]] + singleun[split[2]]
        except:
            pass
        return singlepre[split[0]] + doubleun[split[1:3]]
    elif length == 4:
        try:
            return singlepre[split[0]] + tribleun[split[1:4]]
        except:
            pass
        return doublepre[split[0:2]] + doubleun[split[2:4]]

    
    return None



def unit_to_tex(unit: str) -> str:
    """
    Converts the unit from the input-file to a string, that can be used by the siunitx-package.

    Parameters
    ----------
    unit : str
        The complete unit, as extracted from the file.

    Returns
    -------
    str
        A string, that can be inputed in LaTeX.

    """
    if unit == "-" or "":
        return "-"
    
    truth = True
    index_last = 0
    tex_unit = ""
    
    while truth:
        index_next = search_char(unit, index_last, charUnits)
        
        if index_next - index_last != 0:
            tex_unit += subunit_to_tex(unit[index_last:index_next])
        if index_next == len(unit):
            break
        if unit[index_next] == "/":
            tex_unit += "\\per"
        index_last = index_next + 1
            
    
    return tex_unit



def calculate(data: dict) -> dict:
    """
    Takes the dictionary with the inputs from the txt-file, and returns
    a dictionary with all values and LaTeX-strings calculated.

    Parameters
    ----------
    data : dict
        The unprocessed dictionary.

    Returns
    -------
    dict
        A dictionary, with every value calculated.

    """
    for key in data.keys():
        data[key]["tex_un"] = unit_to_tex(data[key]["unit"])
        if data[key]["var"] == "form":
            data[key]["res"], data[key]["var_in"], data[key]["val_in"] = calc_formula.main(data[key]["form"], data)
        
    return data


def main(filename: str) -> dict:
    """
    Reads and calculates a fully filled dictionary to use in the class.

    Parameters
    ----------
    filename : str
        The filename of a txt-file containing the inputs.

    Returns
    -------
    dict
        A dictionary with springs for displaying in LaTeX and values.

    """
    data = read_file(filename)
    return calculate(data)

