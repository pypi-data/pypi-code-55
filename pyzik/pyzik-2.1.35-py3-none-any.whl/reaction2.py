# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:17:41 2019

@author: jazzn
"""

from chempy import ReactionSystem
from IPython.core.display import HTML

class Reaction:
    def __init__(self,react,quantite):
        assert isinstance(react,str)
        for qte in quantite:
            assert qte>=0,f"les quantités initiales doivent être positives ou nulles"
        self.r = ReactionSystem.from_string(react)
        self.__list = list(self.r.substance_names())
        assert len(self.__list) == len(quantite),"Il y a trop ou pas assez de quantités initiales !!!"
        act_coef,typ=[],[]
        for coefR,coefP in zip(self.r.active_reac_stoichs()[0],self.r.active_prod_stoichs()[0]):
            act_coef.append(coefR+coefP)
            typ.append('p' if coefR==0 else 'r')
        self.__coef = dict(zip(self.__list,act_coef))
        self.__qte_ini = dict(zip(self.__list,quantite))
        self.__typ = dict(zip(self.__list,typ))
        self.__reactants = [subst for subst in self.__list if self.__typ[subst]=='r']
        
    def display(self):
        return HTML(self.r.html())
    
    def __check(self,substance):
        assert substance in self.__list,f"{substance} n'est pas dans la réaction"
    
    def coef(self,substance):
        self.__check(substance)
        return self.__coef[substance]
    
    def qte_ini(self,substance):
        self.__check(substance)
        return self.__qte_ini[substance]
    
    def get_reactant_list(self):
        return self.__reactants
    
    def typ(self,substance):
        self.__check(substance)
        return self.__typ[substance]
    
    def get_esp_list(self):
        return self.__list
