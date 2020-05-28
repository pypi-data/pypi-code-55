import sqlite3
import sys
import re
import time


def home():
    databaseConnection()
    print("WELCOME TO JOB_HOUSE\nGET TO KNOW ABOUT THE LASTEST JOB OFFERS"
          " ALL IN YOUR FINGER TIPS")
    print("==" * 40)
    # print("LOGIN\nSIGNUP")
    while True:
        try:
            while True:
                selection = int(input("PRESS 1 FOR LOGIN\nPRESS 2 FOR SIGNUP\nPRESS 3 TO CLOSE APP\nENTER :  "))
                if selection == 1:
                    login()
                    break
                elif selection == 2:
                    register()
                    break
                elif selection == 3:
                    print("THANK YOU FOR USING JOB_HOUSE")
                    sys.exit()
                elif selection != 1 and selection != 2 and selection != 3:
                    print("INVALID SELECTION")
        except ValueError:
            print("INVALID ENTRY\nTRY AGAIN")

def latestPost():
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()
    latest_post = conn.execute("SELECT * FROM (SELECT * FROM USER_POSTS ORDER BY ID DESC LIMIT 10)ORDER BY ID DESC;")
    for row in latest_post.fetchall():
        lines = list(row)
        print("===" * 35)
        print('|| POSTED BY = ',lines[1])
        print('|| JOB TYPE = ',lines[2])
        print('|| JOB DESCRIPTION = ', lines[3])
        print('|| JOB LOCATION = ',lines[4])
        print('|| COMPANY NAME = ',lines[5])
        print('|| TIME POST = ', lines[6],'\n')

    conn.close()

def contentPage():
    try:
        while True:
            selection = int(input("\nSELECT 1 FOR TOP 10 FOR RECENT POST\nSELECT 2 TO VIEW ALL JOBS OFFERS"
                                  "\nSELECT 3 TO ADD JOB OFFERS AS AN EMPLOYER\nSELECT 4 TO SEARCH FOR JOB OFFERS"
                                  "\nSELECT 5 TO LOGOUT.\nENTER SELECTION :  "))
            if selection == 1:
                latestPost()
            elif selection == 2:
                viewpost()
            elif selection == 3:
                addpost()
            elif selection == 4:
                search()
            elif selection == 5:
                home()
            elif selection != 1 and selection != 2 and selection !=3 and selection != 4 and selection != 5:
                print("WRONG SELECTION\nTRY AGAIN.")
    except ValueError:
        print("INVALID ENTRY\nPLEASE TRY AGAIN")

def verifyuser(arr, username, password):
    i = 0
    while i < len(arr):
        if username == arr[i][4] and password == arr[i][5]:
            contentPage()
        i += 1
    return("NOT IN DATABASE")


def login():
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()

    mylist = []
    print("WELCOME TO THE LOGIN PAGE \nWRONG DETAILS WILL REQUIRE YOU ENTER YOUR DETAILS AGAIN")
    try:
        while True:
            username = input("\nUSERNAME : ")
            password = input("PASSWORD : ")


            query = conn.execute("SELECT * FROM (SELECT * FROM USERS ORDER BY ID DESC)ORDER BY ID DESC;")
            for row in query.fetchall():
                row2 = list(row)
                # print(row2)
                mylist.append(row2)
                verifyuser(mylist, username, password)
            if conn.execute("SELECT * FROM USERS U WHERE EXISTS(SELECT * FROM USERS WHERE USERNAME = ?  = U.USERNAME)ORDER BY ID",(username,)):
                print("MAKE SURE USERNAME AND PASSWORD CORRECT.")
            # elif conn.execute("SELECT * FROM USERS U WHERE NOT EXISTS(SELECT 1 FROM USERNAME WHERE ID = U.ID)ORDER BY ID"):
            #     print("ok go")
    except ValueError:
        print("INVALID INPUT")

        # conn.close()

def register():
    conn = sqlite3.connect("JOB_HOUSE.db")
    # print("database created successfully")
    cursor = conn.cursor()
    print("please fill in the needed details correctly\n"
          "Failure to do so would deny your access to the next part of the registration")

    NAME = input('FULL NAME: ').upper()
    try:
        while True:
            PHONE = input("PHONE NUMBER: ")
            number = PHONE
            if re.match(r'0[879][01]\d{8}', number):
                break
            else:
                print('This is not a valid phone number')
    except ValueError:
        print("invalid details.")

    try:
        while True:
            EMAIL = input("EMAIL  : ")
            address = EMAIL
            if re.match(r'(\D\S+@\S+\.[com]+)$', address):
                break
            else:
                print("INVALID EMAIL ADDRESS, Type Again")
    except ValueError:
        print("invalid details")

    USER_NAME = input("YOUR USERNAME : ").upper()
    PASSWORD = input("PASSWORD :  ").upper()

    dataStorage= "INSERT INTO USERS(NAME, PHONE, EMAIL, USERNAME, PASSWORD) VALUES(?,?,?,?,?)"
    conn.execute(dataStorage,(NAME,PHONE,EMAIL,USER_NAME,PASSWORD))
    conn.commit()
    conn.close()
    print("Registration successful")
    print("redirecting to the login page")
    print("==" * 40)
    login()


def viewpost():
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()

    view_post = conn.execute("SELECT * FROM (SELECT * FROM USER_POSTS ORDER BY ID DESC)ORDER BY ID DESC;")
    for row in view_post.fetchall():
        lines = list(row)
        print("===" * 40)
        print('|| POSTED BY = ',lines[1])
        print('|| JOB TYPE = ',lines[2],''*50)
        print('|| JOB DESCRIPTION = ', lines[3])
        print('|| JOB LOCATION = ',lines[4])
        print('|| COMPANY NAME = ',lines[5])
        print('|| TIME POST = ', lines[6],'\n')

    conn.close()

def addpost():
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()
    print("\nADD A JOB POSTS")
    name = input("YOUR NAME : ").upper()
    jobtype = input("JOB TYPE : ").upper()
    jobdescription = input("JOB DESCRIPTION :  ")
    location = input("COMPANY LOCATION : ").upper()
    companyname = input("COMPANY NAME : ").upper()
    timeposted = time.asctime(time.localtime(time.time()))

    dataStorage= "INSERT INTO USER_POSTS(NAME, JOBTYPE," \
                 " JOBDESCRIPTION, LOCATION, COMPANYNAME, TIMEPOSTED) VALUES(?,?,?,?,?,?)"
    conn.execute(dataStorage,(name,jobtype,jobdescription,location,companyname,timeposted))
    conn.commit()
    conn.close()
def search():
    try:
        while True:
            selection = int(input("PRESS 1 TO SEARCH BY JOB TYPE\nPRESS 2 TO SEARCH BY LOCATION"
                              "\nPRESS 3 TO SEARCH BY COMPANY NAME"))
            if selection == 1:
                print("\nPS.\nIF JOB TYPE DOES NOT EXIST NOTHING WILL BE PRINTED OUT")
                jobtype = str(input("ENTER JOB TYPE : "))
                searchByJob(jobtype)
            elif selection == 2:
                print("\nPS.\nIF LOCATION DOES NOT EXIST NOTHING WILL BE PRINTED OUT")
                location = str(input("ENTER LOCATION : "))
                searchLocation(location)
            elif selection == 3:
                print("\nPS.\nIF COMPANY NAME DOES NOT EXIST NOTHING WILL BE PRINTED OUT")
                companyName = str(input("ENTER COMPANY NAME : "))
                searchCompanyName(companyName)
            elif selection != 1 and selection != 2 and selection != 3:
                print("WRONG SELECTION\nTRY AGAIN PLEASE")
            break
    except ValueError:
        print("INVALID ENTRY\nTRY AGAIN")

def searchLocation(var_iput):
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()
    try:
        search_result = conn.execute("SELECT * FROM USER_POSTS WHERE LOCATION = ?;",(var_iput,))
        for row in search_result:
            lines = list(row)
            print("===" * 35)
            print('POSTED BY = ',lines[1])
            print('JOB TYPE = ',lines[2])
            print('JOB DESCRIPTION = ', lines[3])
            print('JOB LOCATION = ',lines[4])
            print('COMPANY NAME = ',lines[5])
            print('TIME POST = ', lines[6],'\n')
    except conn.execute("SELECT * FROM USER_POSTS WHERE NOT EXISTS"
                        "(SELECT ISNULL 'DATA DOES NOT EXIST')",(var_iput,)):
        print("LOCATION DOES NOT EXIST.")


    conn.close()

def searchCompanyName(var_input):
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()
    search_result = conn.execute("SELECT * FROM USER_POSTS WHERE COMPANYNAME = ? ",(var_input,))
    for row in search_result:
        lines = list(row)
        print("===" * 35)
        print('POSTED BY = ',lines[1])
        print('JOB TYPE = ',lines[2])
        print('JOB DESCRIPTION = ', lines[3])
        print('JOB LOCATION = ',lines[4])
        print('COMPANY NAME = ',lines[5])
        print('TIME POST = ', lines[6],'\n')

    conn.close()


def searchByJob(var_input):
    conn = sqlite3.connect("JOB_HOUSE.db")
    cursor = conn.cursor()
    search_result = conn.execute("SELECT * FROM USER_POSTS WHERE JOBTYPE = ? ",(var_input,))
    for row in search_result:
        lines = list(row)
        print("===" * 35)
        print('POSTED BY = ',lines[1])
        print('JOB TYPE = ',lines[2])
        print('JOB DESCRIPTION = ', lines[3])
        print('JOB LOCATION = ',lines[4])
        print('COMPANY NAME = ',lines[5])
        print('TIME POST = ', lines[6],'\n')

    conn.close()

def databaseConnection():
    conn = sqlite3.connect("JOB_HOUSE.db")
    # print("database Connected Succesfully")
    cursor = conn.cursor()

    query =cursor.execute("CREATE TABLE IF NOT EXISTS USERS"
                          "(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "NAME  TEXT  NOT NULL,"
                          "PHONE CHAR(11) NOT NULL,"
                          "EMAIL CHAR(50) NOT NULL,"
                          "USERNAME CHAR(30) NOT NULL,"
                          "PASSWORD CHAR(20) NOT NULL)")


    query2 = cursor.execute("CREATE TABLE IF NOT EXISTS USER_POSTS(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "NAME TEXT NOT NULL,"
                            "JOBTYPE TEXT NOT NULL,"
                            "JOBDESCRIPTION TEXT NOT NULL,"
                            "LOCATION TEXT NOT NULL,"
                            "COMPANYNAME TEXT NOT NULL,"
                            "TIMEPOSTED TEXT NOT NULL)")

    conn.close()

home()
