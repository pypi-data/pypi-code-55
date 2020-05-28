# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:44:01 2019

@author: jazzn
"""
import os
from datetime import datetime
import pandas as pd
from pyzik.pandly import f_input
from prettytable import PrettyTable
import requests
import wget
import pathlib

class Ethercalc:
    def __init__(self,calc_id,csv_header="test_info;date;name;group;question;result;attempt",typ="FRAMA"):
        """
        input :
            calc_id: str
            csv_header: str (default) "test_info;name;group;time;question;result;attempt"
            typ: str "FRAMA" for framacalc| "ETHER" for Ethercalc
        """
        self.id = calc_id
        self.csv_header = csv_header
        typs = ["FRAMA","ETHER"]
        assert typ in typs,f"typ mal définit ...avaiable {typs} "
        self.typ = typ
        if typ == "FRAMA":
            self.url_start = "https://lite.framacalc.org/"
            self.sep = "|"
        elif typ == "ETHER":
            self.url_start = "https://ethercalc.org/"
            self.sep=";"
            
    def post(self,text):
        if self.typ == "FRAMA":
            text = self.sep.join(text.split(";"))          
        headers = {'Content-Type': 'text/csv',}
        response = requests.post(f'{self.url_start}_/{self.id}', headers=headers, data=text)
        if "202" in str(response):
            print(f"up...{text}")
    
    def extract_csv(self):
        url = self.url_start+self.id+".csv"
        self.csv_file = wget.download(url)
        df = pd.read_csv(self.csv_file,sep=self.sep)
        df["ID"] = df["name"]+" "+df["group"]
        return df

class Score:
    def __init__(self,name,group,test_info,calc_id,**d):
        assert name != '','name non null'
        assert group != '','group non null'
        assert test_info !='','test_info non null'
        self.name = name
        self.group = group
        self.test_info = test_info
        self.ether = Ethercalc(calc_id,**d)

    def up(self,question,response,attempt=-1):
        date = datetime.now().strftime('%d-%b-%Y_%H:%M:%S')
        text = f"{self.test_info};{date};{self.name};{self.group};{question};{response};{attempt}\n"
        self.ether.post(text.replace(" ","_"))
        
    def uprint(self,response,question,attempt=-1):
        assert isinstance(response,str),"Response must be str ..."
        self.up(question,response,attempt)
        
    def set_deco(self):
        def decorated(func):
            def wrapper(*args,**kwargs):
                currentQ = kwargs.get('question','')
                attempt = kwargs.get('attempt',-1)
                response = func(*args,**kwargs)
                if currentQ != '':
                    self.up(currentQ,response,attempt=attempt)
                else:
                    print("No question set ... no update")
                return response
            return wrapper
        return decorated
    



#def generate_all(path='T:',test_info='TP01',dest_file='evalfinal_'):
#    final_file = path+'\\'+dest_file+test_info+'.xlsx'
#    df_tot = pd.DataFrame()
#    print('list of files ...')
#    for file in os.listdir(path):
#        if (test_info in file) and file.endswith('.csv'):
#            print(path+'\\'+file)
#            try:
#                df = pd.read_csv(path+'\\'+file,sep=';',skiprows=4,encoding = "utf-8")
#            except:
#                try:
#                    df = pd.read_csv(path+'\\'+file,sep=';',skiprows=4,encoding = "ISO-8859-1", engine='python')
#                except:
#                    print("erreur")
#            df['group']=file.rstrip('.csv')
#            df_tot = df_tot.append(df,ignore_index=True)
#            print(df_tot)
#    df_tot
#    chk = True
#    print('Excel file to be generated ..'+final_file)
#    if os.path.isfile(final_file):
#        chk = f_input("Excel File already exists, want a new ?",output='str',choice=['y','n']) == 'y'
#    if chk:
#        df_tot.to_excel(final_file)
#        print("excel file create ...")
#        generate_score(path,test_info,dest_file)
#    return df_tot
    
def generate_score(df,test_info="TP01",path=None,dest_file='evalfinal_'):
    if path == None:
        path = str(pathlib.Path().absolute())
    final_file = path+'\\'+dest_file+test_info+'.txt'
    groups = set(df['ID'].tolist())
    chk = True
    if os.path.isfile(final_file):
        chk = f_input("Txt File already exists, want a new ?",output='str',choice=['y','n']) == 'y'
    if chk:
        f = open(final_file, 'w')  # open file in append mode
    else:
        print("cancel ...")
        return None
    df.sort_values(by=['question','date'],inplace=True)

    for gr in groups:
        f.write("*"*80+'\n'+gr.rstrip('.csv')+'\n'*3) 
        t = PrettyTable()
        t.add_column('question',df.loc[df['ID']==gr]['question'].values)
        t.add_column('date',df.loc[df['ID']==gr]['date'].values)
        t.add_column('result',df.loc[df['ID']==gr]['result'].values)
        t.add_column('attempt',df.loc[df['ID']==gr]['attempt'].values)
        f.write(t.get_string())
        f.write('\n'*3)
    f.close()