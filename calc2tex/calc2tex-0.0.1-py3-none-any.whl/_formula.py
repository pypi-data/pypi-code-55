# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:08:31 2020

@author: stefa
"""
from ._helper import is_float, search_char, search_bracket
from .settings import mult_sign
#Imports for evaluating formula:
import numpy as np
from calc2tex import trigo


def split_mult(string: str) -> str:
    """
    Splits the string on the highest order factors und passes them again into the split_sum-function.

    Parameters
    ----------
    string : str
        A formula, which is preprocessed by split_sum and split_quo.

    Returns
    -------
    str
        The input with the single factors processed.

    """
    index_last = 0
    back = ""
    
    while True:
        index_start = search_char(string, index_last, ["("])
        if index_start == len(string):
            back += string[index_last:index_start]
            break
        
        index_next = search_bracket(string, index_start, 1)
        
        back += "".join((string[index_last:index_start+1], split_sum(string[index_start+1:index_next]), string[index_next]))
        
        index_last = index_next + 1
    
    return back



def split_quo(string: str) -> str:
    """
    Converts fractions.

    Parameters
    ----------
    string : str
        The formula preprocessed by split_funct, split_expo and split_sum.

    Returns
    -------
    str
        Processed formula.

    """
    #TODO ?/?/? berücksichtigen -> \frac{?}{?*?}
    index_last, index_start = 0, 0
    back = ""
    
    if string[0] == "+" or string[0] == "-":
        index_last = 1
        back += string[0]
        
    while True:
        while True:
            index_next = search_char(string, index_start, ["/"])
            index_start = index_next + 1
            if string.count("(", 0, index_next) - string.count(")", 0, index_next) == 0:
                break
            
        if index_next == len(string):
            back += split_mult(string[index_last:])
            break
    
        if string[index_next+1] == "/":
            intdiv = True
            index_start += 1
            start, end = index_next - 1, index_next + 2
        else:
            intdiv = False
            start, end = index_next - 1, index_next + 1
        
        if string[start] == ")":
            start = search_bracket(string, start, -1)
            numerator = split_sum(string[start+1:index_next-1])
        else:
            numerator = string[start]
        
        if string[end] == "(":
            end = search_bracket(string, end, 1)
            if intdiv:
                denominator = split_sum(string[index_next+3:end])
            else:
                denominator = split_sum(string[index_next+2:end])
        else:
            denominator = string[end]
        
        before = split_mult(string[index_last:start])
        if intdiv:
            back += "".join((before,"\\left\\lfloor\\frac{", numerator, "}{", denominator, "}\\right\\rfloor "))
        else:
            back += "".join((before,"\\frac{", numerator, "}{", denominator, "}"))
        index_last = end + 1
      
    return back



def split_sum(string: str) -> str:
    """
    Splits the formula on single summands and processes one a time.

    Parameters
    ----------
    string : str
        The formula preprocessed by split_funct and split_expo.

    Returns
    -------
    str
        Processed formula.

    """
    if len(string) == 0:
        return string
    #TODO muss index_last auf 1 gesetzt werden, immer auf 1 -> if bedingung in schleife weg
    if string[0] == "+" or string[0] == "-":
        index_last, index_start = 1, 1
    else:
        index_last, index_start = 0, 0
    back = ""
    
    while True:
        index_next = search_char(string, index_start, ["+", "-"])
        if string.count("(", 0, index_next) - string.count(")", 0, index_next) == 0:
            if index_last == 0:
                #print(string, string[index_last:index_next])
                back += split_quo(string[index_last:index_next])
            else:
                #print(string, string[index_last-1:index_next])
                back += split_quo(string[index_last-1:index_next])
            index_last = index_next + 1
        
        #print("exit")
        if index_next == len(string):
            break
        
        index_start = index_next + 1
       
    return back 



def split_expo(string: str) -> str:
    """
    Takes a string and processes all exponents.

    Parameters
    ----------
    string : str
        Formula preprocessed by split_funct.

    Returns
    -------
    str
        Processed formula.

    """
    index_last = 0
    expos = []
    
    while True:
        index_next = search_char(string, index_last, ["**"])
        if index_next == len(string):
            break
        
        start, end = index_next - 1, index_next + 2
        
        if string[start] == ")":
            start = search_bracket(string, start, -1)
            base = "(" + split_sum(string[start+1:index_next-1]) + ")"
        else:
            base = string[start]
            
        if string[end] == "(":
            end = search_bracket(string, end, 1)
            if "**" in string[index_next+3:end]:
                power = split_expo(string[index_next+3:end])
            else:
                power = split_sum(string[index_next+3:end])
        else:
            power = string[end]
        
        expo_in_base = string.count("§", start, index_next)
        
        expos.insert(len(expos)- expo_in_base, "".join((base, "^{", power, "}")))
        string = string.replace(string[start:end+1], "§", 1)
        
        index_last = start
    
    back = split_sum(string)
    
    for expo in expos:
        back = back.replace("§", expo, 1)
        
    return back



def split_funct(string: str) -> str:
    """
    Searches for functions inside string and separatly converts them.

    Parameters
    ----------
    string : str
        The unprocessed formula.

    Returns
    -------
    str
        Nearly to LaTeX converted formula.

    """
    functions = []
    index_last = 0
    
    while True:
        index_start = search_char(string, index_last, ["?(", "~("])
        
        if index_start >= len(string):
            break
        
        index_next = search_bracket(string, index_start+1, 1) #von index_start+2 geändert
        
        if "?(" in string[index_start+2:index_next+1] or "~(" in string[index_start+2:index_next+1]:
            if string[index_start] == "~":
                functions.append("?{" + split_funct(string[index_start+2:index_next]) + "}")
            else:
                
                functions.append("?(" + split_funct(string[index_start+2:index_next]) + ")")
        else:
            if string[index_start] == "~":
                functions.append("?{" + split_expo(string[index_start+2:index_next]) + "}")
            else:
                functions.append(split_expo(string[index_start:index_next+1]))
                
        string = string.replace(string[index_start:index_next+1], "!", 1)
        index_last = index_start
      
    back = split_expo(string)
    
    for funct in functions:
        back = back.replace("!", funct, 1)
    
    return back



def find_vars(formula: str) -> (str, list):
    """
    Replaces all variables, numbers, commands inside formula by single chars, mainly question marks. 

    Parameters
    ----------
    formula : str
        The non-processed formula from the txt-file.

    Returns
    -------
    short_formula : str
        The shortened formula.
    var_list : list
        The list of extracted variables.

    """
    index_last = 0
    short_formula = ""
    var_list = []
    chars_in_formula = ["/", "*", "(", ")", "+", "-", "%"]
    tilde = ["sqrt"]
    #TODO abs -> $, (min, max) -> ° eigene Zeichen
    
    while True:
        index_next = search_char(formula, index_last, chars_in_formula)
        
        if index_next - index_last != 0:
            var_list.append(formula[index_last:index_next])
            if formula[index_last:index_next] in tilde:
                short_formula += "~"
            else:
                short_formula += "?"
                
        if index_next == len(formula):
            break
        
        short_formula += formula[index_next]
        index_last = index_next + 1
    
    return short_formula, var_list



def formula_to_tex(formula: str) -> str:
    """
    Mainly for calling a deeper level to convert the shortened formula to LaTeX and some post-processing.

    Parameters
    ----------
    formula : str
        The shortened formula, where variables are represented as question marks.

    Returns
    -------
    str
        The processed formula.

    """
    back = split_funct(formula)
    
    back = back.replace("*", mult_sign + " ")
    back = back.replace("(", "\\left(")
    back = back.replace(")", "\\right)")
    back = back.replace("%", "\bmod ")
    
    return back



def transform_vars(var_list: list, data: dict) -> (list, list, list):
    """
    Evaluates all variables in a formula and returns lists with their respective LaTeX-variables
    or values and units or only values.

    Parameters
    ----------
    var_list : list
        The list of variables in a formula.
    data : dict
        The main dictionary with all inputed variables.

    Returns
    -------
    var_list : list
        A list to input into the formula showing all LaTeX-variables.
    tex_val : list
        A list to input into the formula showing all values and units.
    py_val : list
        A list to into into the formula with all values.

    """
    #TODO abhängig von größe der Zahl Standardgenauigkeit ändern oder in Exponentialdarstellung wechseln
    tex_commands = ("e", "pi", "sin", "cos", "tan", "sqrt", "arccos", "arcsin", "arctan", "arcsinh", "arccosh", "arctanh", "sinh", "cosh", "tanh")
    trigo_list = ("sinD", "cosD", "tanD", "arccosD", "arcsinD", "arctanD", "sinG", "cosG", "tanG", "arccosG", "arcsinG", "arctanG")
    py_funct = ("min", "max", "abs")
    tex_val = var_list[:]
    py_val = var_list[:]
    
    #TODO use enumarate, would replace right site of equal-sign
    for i in range(len(var_list)):
        if is_float(var_list[i]):
            continue
        elif var_list[i] in tex_commands:
            py_val[i] = "np." + var_list[i]
            if var_list[i] != "e":
                tex_val[i] = var_list[i] = "\\" + var_list[i]
        elif var_list[i] in trigo_list:
            py_val[i] = "trigo." + var_list[i]
            tex_val[i] = var_list[i] = "\\" + var_list[:-1]
        elif var_list[i] in py_funct:
            if var_list[i] == "abs":
                tex_val[i] = var_list[i] = ""
            else:
                tex_val[i] = var_list[i] = "\\" + var_list[i]
        elif var_list[i] in data:
            py_val[i] = data[var_list[i]]["res"]
            #TODO genauigkeit aus data-dict oder standard aus settings, siehe oben
            tex_val[i] = "".join(("\\SI{", str(data[var_list[i]]["res"]), "}{", data[var_list[i]]["tex_un"].replace("-", ""), "}"))
            var_list[i] = data[var_list[i]]["tex_var"]
        #elif:
            #TODO prüfen ob item in bibs-dict
            #pass
        else:
            #TODO raise Exception
            pass
        
    return var_list, tex_val, py_val



def vars_in_short(short_formula: str, var_list: list) -> str:
    """Inputs all variables from var_list into short_formula"""
    for var in var_list:
        short_formula = short_formula.replace("?", str(var), 1)
        
    return short_formula




def py_eval(formula: str) -> float:
    """Calculates the result of the formula."""
    return eval(formula)
    


def main(formula: str, data: dict) -> (float, str, str):
    """
    Calculates the result of a formula and its LaTeX-representations given all other variables.

    Parameters
    ----------
    formula : str
        The formula, which should be processed.
    data : dict
        A dictionary containing all other variables and their results.

    Returns
    -------
    py_res : float
        The result of the formula.
    tex_var : str
        The formula, where the variables are replaced by their LaTeX-representations.
    tex_val : str
        The formula, where the variables are replaced by their values and units.

    """
    short_formula, var_list = find_vars(formula)
    
    short_tex = formula_to_tex(short_formula)
    
    tex_vars, tex_vals, py_vals = transform_vars(var_list, data)
    
    py_res = py_eval(vars_in_short(short_formula, py_vals))
    tex_var, tex_val = vars_in_short(short_tex, tex_vars), vars_in_short(short_tex, tex_vals)
    
    return (py_res, tex_var, tex_val)
    
