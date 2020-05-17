#Library
import pandas as pd
import camelot
import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, Integer, String, VARCHAR
import psycopg2

def pdfextrat(url="http://www.fsvs.ks.edu.tw/ezfiles/0/1001/img/58/206002.pdf",page=34):
    tables=camelot.read_pdf(url, pages=str(page),flavor="stream")
    print("Analysis Alchole PDF.....")
    print(tables[0])
    print(tables[0].parsing_report)
    table_df = tables[0].df
    return table_df

def table_transform(table_df):
    rule = ["題序", "一", "二", "三", "四", "五"]
    index, team = [], ""
    for num, i in enumerate(table_df.iloc[:, 0]):
        if "組別" in i:
            team = i.replace("組別 ", "")
        if i in rule:
            index.append(num)

    index[0] = index[0] + 2

    alc_dict = {
        "Team": [],
        "Drinkname": [],
        "Ingredients": [],
        "Method": [],
        "Garnish": [],
        "Glassware": []
        }

    for n, first in enumerate(index):
        dr, ing, me, gar, glass = "", "", "", "", ""
        second = 0
        if first == index[len(index) - 1]:
            second = len(table_df) - 1
        else:
            second = index[n + 1]
        for i in range(first, second):
            if len(table_df.columns) == 10:
                dr += table_df.iloc[i, 1]
                ing += table_df.iloc[i, 2]
                me += table_df.iloc[i, 3]
                gar += table_df.iloc[i, 6]
                glass += table_df.iloc[i, 7] + table_df.iloc[i, 8] + table_df.iloc[i, 9]
            elif len(table_df.columns) == 9:
                dr += table_df.iloc[i, 1]
                ing += table_df.iloc[i, 2]
                me += table_df.iloc[i, 3]
                gar += table_df.iloc[i, 5]
                glass += table_df.iloc[i, 6] + table_df.iloc[i, 7] + table_df.iloc[i, 8]
            elif len(table_df.columns) == 8:
                dr += table_df.iloc[i, 1]
                ing += table_df.iloc[i, 2]
                me += table_df.iloc[i, 3]
                gar += table_df.iloc[i, 4]
                glass += table_df.iloc[i, 5] + table_df.iloc[i, 6] + table_df.iloc[i, 7]
            elif len(table_df.columns) == 7:
                dr += table_df.iloc[i, 1]
                ing += table_df.iloc[i, 2]
                me += table_df.iloc[i, 4]
                gar += table_df.iloc[i, 5]
                glass += table_df.iloc[i, 6]
            else:
                dr += table_df.iloc[i, 1]
                ing += table_df.iloc[i, 2]
                me += table_df.iloc[i, 3]
                gar += table_df.iloc[i, 4]
                glass += table_df.iloc[i, 5]
        alc_dict["Team"].append(team)
        alc_dict["Drinkname"].append(dr)
        alc_dict["Ingredients"].append(ing)
        alc_dict["Method"].append(me)
        alc_dict["Garnish"].append(gar)
        alc_dict["Glassware"].append(glass)

    alc_df = pd.DataFrame(alc_dict)
    return alc_df

def multiplepage(page_start, page_end, url="http://www.fsvs.ks.edu.tw/ezfiles/1/1001/img/58/206002.pdf"):
    alldf = pd.DataFrame()
    for i in range(page_start, page_end + 1):
        table_df = pdfextrat(url, i)
        try:
            df1 = table_transform(table_df)
            alldf = pd.concat([alldf, df1])
            alldf.index = range(0, len(alldf))
        except:
            print("Error: can not transform this page {}, maybe it is not formula page".format(i))
    return alldf

def to_postgresql(inputdata, user, password, host, port, db):
    try:
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        meta = sqlalchemy.MetaData(bind=con, reflect=True)
        quiz = Table('BartenderQuiz', meta,
                      Column('Team', VARCHAR(10)),
                      Column('Drinkname', String),
                      Column('Ingredients', String),
                      Column('Method', String),
                      Column('Garnish', String),
                      Column('Glassware', String)
                    )
        meta.create_all(con)
        for i in range(0, len(inputdata)):
            row = quiz.insert().values(Team=inputdata.iloc[i, 0], Drinkname=inputdata.iloc[i, 1],
                                       Ingredients=inputdata.iloc[i, 2], Method=inputdata.iloc[i, 3],
                                       Garnish=inputdata.iloc[i, 4], Glassware=inputdata.iloc[i, 5])
            con.execute(row)
        return "Success"
    except:
        return "Error: Mabye your input is wrong"