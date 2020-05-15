# -*- coding: utf-8 -*-
"""
Created on Sat May  2 21:06:53 2020

@author: stefa
"""


def is_float(number: str) -> bool:
    """Checks if the input-string can be converted ta a valid number."""
    try:
        float(number)
    except:
        return False
    else:
        return True
    
    
#TODO chars as tuple 
def search_char(string: str, pos: int, chars: list) -> int:
    """
    Searches for the index of the next char out of the chars-list.

    Parameters
    ----------
    string : str
        A formula.
    pos : int
        The index, at which searching should be started.
    chars : list
        A list containing strings.

    Returns
    -------
    int
        The index of the next char or if there is no char found the lenght of the string.

    """
    indices = []
    for char in chars:
        try:
            indices.append(string.index(char, pos))
        except:
            pass
    
    if indices == []:
        return len(string)
    else:
        return min(indices)



def search_bracket(string: str, pos: int, direction: int) -> int:
    """
    searches the corresponding opening or closing bracket

    Parameters
    ----------
    string : str
        A formula.
    pos : int
        The Index of the bracket, at which searching should be started.
    direction : int
        The direction at which should be searched.

    Returns
    -------
    int
        Index of the corresponding bracket.

    """
    numcorr, numdiff = 0, 0
    newpos = pos
    if direction == -1:
        while True:
            index = string.rfind("(", 0, newpos)
            # if index == -1:
            #     raise Exception
            numdiff += string.count(")", index, newpos)
            if numdiff == numcorr:
                return index
            numcorr += 1
            newpos = index
                
    elif direction == 1:
        newpos += 1
        while True:
            index = string.find(")", newpos)
            numdiff += string.count("(", newpos, index)
            if numdiff == numcorr:
                return index
            numcorr += 1
            newpos = index + 1




