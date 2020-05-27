# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:37:34 2020

@author: jazzn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:56:58 2020

@author: jazzn
"""

import sys
import random
import io
import base64
import pandas as pd
import chempy as cp
import requests

def superLoc(df,idx,*cols):
    if isinstance(idx,int):
        return tuple([df.loc[idx,col] for col in cols])
    elif isinstance(idx,list):
        return tuple([[df.loc[indx,col] for indx in idx] for col in cols])

def convert2img(url,sizeX=200,sizeY=200):
    return f"""<p><img src="{url}" alt="" width="{sizeX}" /></p>"""

def convert2sci(x,CS=3):
    CS = int(sorted([2,CS,10])[1])
    mantisse,puiss = f"""{x:.10e}""".split("e")
    mantisse=mantisse[:mantisse.index('.')+CS+1]
    multiply = 	u"\u00D7"
    if int(puiss)==0:
        return f"""{mantisse}"""
    else:
        return f"""{mantisse}{multiply}10<sup>{int(puiss)}</sup>"""   
    
def convertDegreDec2DegMin(dd,opt=None,typ="GPS"):
    """
    params : 
        dd : deg decima Ex : 122.3658°
        opt = "Lat" | "Lon" | None
        typ = "GPS" | "dms" | "dms_str" | "dm" | "dm_str"
    Converti des degré décimaux Ex -19.4840833333° au format GPGGA
        return ('1929.0450', 'S')
    """
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    minuts = minutes + seconds/60
    deg = abs(degrees)
    if is_positive:
        if opt == 'Lat':
            L = "N"
        else:
            L = "E"
    else:
        if opt == "Lat":
            L = "S"
        else:
            L = "W"
    if typ == "GPS":
        if opt == None:
            return f"{deg*100+minutes:.4f}"
        else:
            return f"{deg*100+minutes:.4f}",L
    elif typ == "dms":
        return degrees,minutes,seconds
    elif typ == "dms_str":
        return f"""{degrees:.0f}° {minutes:.0f} min {seconds:.2f} s """
    elif typ == "dm":
        return degrees,minuts
    elif typ == "dm_str":
        return f"{degrees:.0f}° {minuts:.4f} min"
        
        
        
def convert2coloredBox(color):
    return f"""<div style="background-color: {color} ; padding: 10px; border: 1px solid green;">"""

def convert2chemFormula(formula):
    return cp.Substance.from_formula(formula).unicode_name

def convert2chem3D(cid,width=300,height=200):
    return f"""<iframe style="width: {width}px; height: {height}px;" frameborder="0" src="https://embed.molview.org/v1/?mode=balls&cid={cid}&bg=white"></iframe>"""
def alea(mmin,mmax,precision):
    p = 10**-precision
    return round(random.uniform(mmin/p,mmax/p))*p

def get_wiki_main_pic_url(title):
    response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={'action': 'query','prop':'pageimages','format':'json','piprop':'original','titles':title,'formatversion':2})
    try:
        return response.json()['query']['pages'][0]['original']['source']
    except:
        print(f"{title} url no found")
        return None

def convert_question_2_MC(html_text,typ="MC"):
    """Exemple de multichoix :
        |3     3_^12   15_3     15_12   12|
        delimitation par pipe
        bonne réponse précédé de ^
        separation des réponses _
    """
    new_text = ""
    f = open('testClozeMC.html','w')
    f.write(html_text)
    f.close()
    with open('testClozeMC.html', "r") as f:
        for line in f.readlines():
            if "|" in line:
                idx_i = line.index("|",0)
                idx_f = line.index("|",idx_i+1)
                text = line[idx_i+1:idx_f]
                a_reply = text.split('_')
                a_reply_final = []
                g_reply_final = []
                for rep in a_reply:
                    if "^" in rep:
                        a_reply_final.append(rep.replace("^",""))
                        g_reply_final.append(rep.replace("^",""))
                    else:
                        a_reply_final.append(rep)
                random.shuffle(a_reply_final)
                text_final = line[:idx_i]+multi_qr(g_reply_final,a_reply_final,typ=typ)+line[idx_f+1:]
                new_text += text_final
            else:
                new_text += line
    return new_text

def generate_xml(func,nb,cat=None,stype="random"):
    name = func.__name__
    cat = name if cat == None else cat
    questions = []
    if stype == "random":
        parameters = [random.randint(0,nb) for i in range(nb)]
    elif stype == "toto":
        parameters = range(nb)
    elif stype == "list":
        parameters = nb #nb est une liste
    for param in parameters:
        r = func(param)
        if r is not None:
            questions.append(func(param))
    file = open(name + ".xml","w",encoding="utf8")
    moodle_xml(name,questions,cloze_question,category = f'{cat}/', iostream = file)
    file.close()
    print("Questions were saved in " + name + ".xml, that can be imported into Moodle")
     
def num_q(x,p=0.001,sci = False,score=1):
    """Return formatted string for numerical question, that can be included into
    cloze type moodle question.
    x ... correct answer, p ... precision
    """
    if sci:
        return "{"+f"{score}:NUMERICAL:={x:e}:{p}~{x:e}:{10*p}"+"}"
    else:
        return "{"+f"{score}:NUMERICAL:={x}:{p}~{x}:{10*p}"+"}" 

def str_q(x,score=1):
    return "{"+f"{score}:SHORTANSWER:="+"%s}" %(x)

num_qr = lambda x,y,score=1:num_q(x,x*y,score=score)

def multi_qr(list_good_reply,list_reply,score = 1,typ="MC"):
    if isinstance(list_good_reply,str):
        list_good_reply = [list_good_reply]
    list_reply = list(set(list_good_reply+list_reply))
    resultat = []
    for rep in list_reply:
        if rep in list_good_reply:
            resultat.append((rep,100))
        else:
            resultat.append((rep,0))
    return multi_q(resultat,score=score,typ=typ)

def multi_q(answers,score = 1,typ="MC"):
    """Return formatted string for multichoice question, that can be included into
    cloze type moodle question.
    answers is a list of pairs (question, percent)
    """
    if typ == "MC":
        zboub = "MCS"
    elif typ == "MCV":
        zboub = "MCVS"
    else:
        zboub = "MCHS"
    q  = "{"+f"{score}:{zboub}:"
    for i in answers:
        q = q+f"~%{i[1]}%{i[0]}\n"
    q = q+"}"
    return q

def multichoice_question(answers, name):
    """
    XML string for moodle multiple choice question.
    answers ... a list of pairs (answer,fraction),
              fraction tells how much percent is worth the answer 
    name ... name of the question
    """
    q  = """<question type="multichoice">
    <name>
      <text> %s </text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Odkljukaj pravilne izjave!<br></p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>false</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <correctfeedback format="html">
      <text>Odgovor je pravilen.</text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text>Odgovor je delno pravilen.</text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text>Odgovor je nepravilen.</text>
    </incorrectfeedback>
    <shownumcorrect/>""" %name
    for answer in answers:
        q = q + """
        <answer fraction="%f" format="html">
        <text><![CDATA[%s]]></text>
          <feedback format="html">
            <text></text>
          </feedback>
        </answer>
        """ % (answer[1],answer[0])
    q = q + "</question>"
    return q

def cloze_question(tekst, name, feedback=''):
    """
    XML string for moodle cloze question.
    tekst ... string with question in cloze format. (see
         https://docs.moodle.org/29/en/Embedded_Answers_(Cloze)_question_type )
    name ... name of the question
    """
    q = """
  <question type="cloze">
    <name>
        <text>%s</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[%s]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text>%s</text>
    </generalfeedback>
    <penalty>0.2000000</penalty>
    <hidden>0</hidden>
  </question>
        """ % (name,tekst,feedback)
    return q

def moodle_xml(name, questions, template_fun, category = '',iostream=sys.stdout):
    """Write moodle xml file to be imported into Moodle.
    name ... name of the category, where the questions will be put
    questions ... list of strings containing xml code for the questions
    template_fun ... cloze_question or multichoice_question
    category ... optional upper category (default '')
    iostream ... file handle or other IOStream (default STDOUT)
    """
    iostream.write("""
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
    <text>$course$/""" + category + name + """</text>

    </category>
  </question>
    """)
    for i in range(len(questions)):
        iostream.write(template_fun(questions[i], name+str(i)))
    iostream.write("</quiz>")
    
class Jokers:
    def __init__(self,var,nb,stype,converters={}):
        assert len(stype)==len(var)*nb,f"incorrect lenght stype lenght -> {len(stype)} | vars -> {len(var)*nb}"
        assert ("0" in stype or "1" in stype),f"stype {stype} ne doit contenir que 0 ou 1"
        self.var = var
        self.nb = nb
        self.stype = stype
        self.converters = converters
        listvar = []
        for v in var:
            for idx in range(1,nb+1):
                listvar.append(v+str(idx))
        self.list_var = listvar
        self.get_joker_dict()

    def get_joker_dict(self):
        """définit un dict des variables
        Exemple "{'e1': 0, 'e2': 0, 'e3': 0, 'r1': 0, 'r2': 1, 'r3': 1, 'p1': 0, 'p2': 1, 'p3': 1}"
        """
        self.dic_var = {v:int(s) for v,s in zip(self.list_var,list(self.stype))}
        return str(self.dic_var)
    
    def set_joker_value(self,var,func,*params):
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                r = func(*params)
                result += f"{v}={r}\n"
        return result


        
    def set_joker_alpha_value_by_list(self,var,lst,fill_default=""):
        """retourne une chaine définissane les variables var1 utilisable avec un exec
        Ex : r1 = 'toto'
            r2 = 'tata'
        """
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        assert len(lst)>=self.nb,"La liste est trop petite par rapport aux variables"
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                fnct = self.converters.get(var,lambda x:x)
                r = fnct(lst[idx])
                if "'" in r:
                    result += f"""{v}="{r}"\n"""
                elif '"' in r:
                    result += f"""{v}='{r}'\n"""
                else:
                    result += f"""{v}='{r}'\n"""
            idx += 1
        return result
    
    def set_joker_numeric_value_by_list(self,var,lst,output_format=None,fill_default=""):
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                fnct = self.converters.get(var,lambda x:x)
                if lst[idx] != fill_default:
                    r = fnct(lst[idx])
                    if output_format == None:
                        result += f"{v}={r}\n"
                    else:
                        toto = format(r,output_format)
                        result += f"{v}= '{toto}'\n"
                else:
                    result += f"{v}= '{fill_default}'\n"
            idx += 1
        return result
    
    def set_joker_numeric_value_by_function(self,var,func_exp):
        def sfunc(f_exp,var):
            jokers = self.var.replace(var[0],"")
            new_f_exp = f_exp
            for j in list(jokers):
                new_f_exp = new_f_exp.replace('_'+j[0],j[0]+v[1])
            return new_f_exp
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 0:
                r = sfunc(func_exp,v)
                result += f"{v}={r}\n"
        return result
    
    def set_joker_multichoice_response_by_list(self,var,g_lst,a_lst,score=1,typ="MC"):
        idx, result , d = 0,"",{}
        for v,typs in self.dic_var.items():
            if v[0] == var:
                d[v] = typs
        for v,typs in d.items():
            if v[0] == var and typs == 1:
                g_reply = g_lst[idx]
                result += f"{v}='{g_reply}'\n"
                result += f"""{v} = multi_qr({v},{a_lst},score={score},typ="{typ}")\n"""
            idx += 1
        return result
        
    def set_joker_short_response_by_list(self,var,lst):
        idx = 0
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                fnct = self.converters.get(var,lambda x:x)
                r = fnct(lst[idx])
                result += f"{v}='{r}'\n"
                result += f"{v} = str_q({v})\n"
            idx += 1
        return result
    
    def set_joker_numeric_response_by_function(self,var,func_exp,precision=0.01,fill_default=""):
        def sfunc(f_exp,var):
            jokers = self.var.replace(var[0],"")
            new_f_exp = f_exp
            for j in list(jokers):
                new_f_exp = new_f_exp.replace('_'+j[0],j[0]+v[1])
            return new_f_exp
        result = ""
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                r = sfunc(func_exp,v)
                result += f"{v}={r}\n"
                result += f"{v} = num_qr({v},{precision})\n"
        return result
    
    def set_joker_numeric_response_by_list(self,var,lst,rtyp="num",precision=0.01,fill_default=""):
        result = ""
        if len(lst)<self.nb:
            lst += [fill_default for _ in range(self.nb-len(lst))]
        idx = 0
        d = {}
        for v,typ in self.dic_var.items():
            if v[0] == var:
                d[v] = typ
        for v,typ in d.items():
            if v[0] == var and typ == 1:
                r = lst[idx]
                if r != fill_default:
                    result += f"{v}={r}\n"
                    result += f"{v} = num_qr({v},{precision})\n"
                else:
                    result += f"{v}='{r}'\n"
            idx += 1
        return result
    
    def set_jokers_numeric_value_and_response_by_list(self,var,lst,precision=0.01,output_format=None):
        txt0 = self.set_joker_numeric_value_by_list(var,lst,output_format=output_format)
        txt1 = self.set_joker_numeric_response_by_list(var,lst,precision=precision)
        return txt0+txt1