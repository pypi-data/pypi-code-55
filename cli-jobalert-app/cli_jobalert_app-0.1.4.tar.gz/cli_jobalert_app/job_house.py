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

    # RUNNING A INSERT STATEMENT MANUALLY TO TEST OUT THE DATABASE..
    Sqlite_insert_query = """INSERT INTO USER_POSTS(NAME, JOBTYPE, JOBDESCRIPTION, LOCATION, COMPANYNAME, TIMEPOSTED)
                           VALUES (?,?,?,?,?,?) """

    records_to_insert = [('SHOLA','ICT Officer (SAP MM Deployment and Support)'
                      ,'We are looking for a UI/UX Designer to turn our'
                       'software into easy-to-use products for our clients',
                      'LAGOS','Oawtechnologies', time.asctime(time.localtime(time.time()))),
                     ('TUNDE','Sales Rep',
                      'Our company is looking for a Sales Representative to be responsible for '
                      'generating leads and meeting sales goals. Duties will include '
                      'sales presentations and product demonstrations, as well as negotiating '
                      'contracts with potential clients.',
                      'LAGOS','Oawtechnologies',time.asctime(time.localtime(time.time()))),
                     ('ADEBISI','Tech Project Manager',
                      'We are looking for a detail-oriented Technical Project '
                      'Manager to oversee all project operations from inception '
                      'to execution. The Technical Project Manager is responsible for maintaining '
                      'budgets, enforcing deadlines and supervising team members','LAGOS',
                      'Oawtechnologies',time.asctime(time.localtime(time.time()))),
                     ('SANDRA','Backend Developer - Remote',
                      'We are looking for an experienced Back-end developer to join our IT team. '
                      'You will be responsible for the server side of our web applications. '
                      'If you have excellent programming skills and a passion for developing applications or '
                      'improving existing ones, we would like to meet you.','LAGOS',
                      'Oawtechnologies', time.asctime(time.localtime(time.time()))),
                     ('KOLA','Creative Graphic Designer',
                      'Illustrating concepts by designing examples of art arrangement,'
                      ' size, type size and style and submitting them for approval','LAGOS',
                      'Ryteprint',time.asctime(time.localtime(time.time()))),
                     ('SHULAMITE','Social media / Sales Intern (Female Preffered)',
                      'Erocraves is looking for an enthusiastic social media/sales '
                      'intern who will contribute to increasing the company sales.',
                      'LAGOS','Erocraves',time.asctime(time.localtime(time.time()))),
                     ('TOBI','Sales & Marketing Executive',
                      'Hoduns Foods Ventures is looking to recruit suitably qualified'
                      ' candidate to fill the position of Sales & Marketing Executive',
                      'LAGOS','Hoduns Foods Ventures', time.asctime(time.localtime(time.time()))),
                     ('JASON','Farm Manager',
                      'We are searching for a Farm Manager with good business sense to join our team.',
                      'Abeokuta & Ogun State','V&l limited',time.asctime(time.localtime(time.time()))),
                     ('DURELO','Executive Director',
                      'Seeking executive director responsible for overseeing the administration,'
                      ' programs and strategic plan of the organization.',
                      'LAGOS','GACO INDUSTRIES LIMITED',time.asctime(time.localtime(time.time()))),
                     ('FAVOR','Director of Information Technology',
                      'Seeking an IT director with leadership skills, project management '
                      'skills. At least 5 years experience with executive management position',
                      'LAGOS','GACO INDUSTRIES LIMITED', time.asctime(time.localtime(time.time()))),
                     ('TAYO','Office Assistant',
                      'We are currently recruiting for this position',
                      'ABUJA','KINABS INFINITI NIG LTD',time.asctime(time.localtime(time.time()))),
                     ('ABRAHAM','Front End Developer',
                      'Design, develop and test (unit, integration, component and system) '
                      'assigned tasks in accordance with the agreed architecture, solution design',
                      'LAGOS','Cognetiks Consulting',time.asctime(time.localtime(time.time()))),
                     ('LINDA','VP, Operations',
                      'We are currently seeking a highly-motivated professional'
                      ' to (1) develop, review, and implement new processes, designed to support '
                      'sustainable growth; and (2) oversee all elements of live (client) workflow execution.',
                      'LAGOS','Anonymous Employer', time.asctime(time.localtime(time.time()))),
                     ('SUZY','Front End Developer',
                      'Experienced Front End Developer required to develop web and mobile applications',
                      'LAGOS','Anonymous Employer',time.asctime(time.localtime(time.time()))),
                     ('WILLIAMS','UI / UX Designer',
                      'UI/UX Designer needed. If you have a portfolio of professional design '
                      'projects that includes work with web/mobile applications, '
                      'we’d like to meet you.',
                      'LAGOS','Anonymous Employer',time.asctime(time.localtime(time.time()))),
                     ('CHARLES','Coordinating Desk Officer',
                      'We are currently recruiting for this position',
                      'ABUJA',
                      'Deutsche Gesellschaft fuer Internationale Zusammenarbeit (GIZ) GmbH',
                      time.asctime(time.localtime(time.time()))),
                     ('REMILEKUN','Sales Manager',
                      'Seeking for an ambitious, innovative, forward-thinking and highly'
                      ' motivated individual who will move the company forward with strong leadership,'
                      ' committed people management and a commercial focus on project sourcing,'
                      ' delivery and profitability','LAGOS',
                      'RyteGate Construction & Technologies Ltd.',time.asctime(time.localtime(time.time()))),
                     ('ISABELLA','Special Advisor to ECOWAS Commission',
                      'We are currently recruiting for this position','ABUJA',
                      'Deutsche Gesellschaft fuer Internationale Zusammenarbeit (GIZ) GmbH',
                      time.asctime(time.localtime(time.time()))),
                     ('BRANDY','Quality Control / Technical Officer',
                      'Quality control and technical officer position in a '
                      'manufacturing company based at Lagos/Ibadan expressway.',
                      'LAGOS','STOVA INDUSTRIES LIMITED', time.asctime(time.localtime(time.time()))),
                     ('GABRIEL','Back-end Developer',
                      'Responsible for analysis, design (UML), development and testing '
                      'of AET internal products and also be accountable for building'
                      ' RESTful web-facing applications and optimized logic to facilitate'
                      ' the organizations interaction with its client.',
                      'LAGOS','ActivEdge Technologies Limited',time.asctime(time.localtime(time.time()))),
                     ('YVONNE','BIOMEDICAL ENGINEER',
                      'The Biomedical Engineer would be responsible for the design,'
                      ' development and implementation of biomedical equipment'
                      ' and care delivery systems as well as the provision of support'
                      ' in the delivery of Medical IT solutions to clients.','LAGOS',
                      'Medcourt Pharmacy',time.asctime(time.localtime(time.time()))),
                     ('AGNES','Sales Manager','We are currently recruiting for this position',
                      'LAGOS','Bemas Technologies Limited',time.asctime(time.localtime(time.time()))),
                     ('FAMOUS','Content Creator/Writer (Internship)',
                      'We are looking for a Content Creator to write and publish '
                      'various types of pieces for our company’s web pages,'
                      ' like articles, ebooks and social media','KWARA','Anter Technologies',
                      time.asctime(time.localtime(time.time()))),
                     ('HELEN','Marketing Manager',
                      'This position has overall oversight and responsibility for,'
                      ' marketing and generating revenue by increasing sales through'
                      ' successful application of marketing strategies and coordinating the'
                      ' marketing & Sales force of the firm.','LAGOS','Anonymous Employer'
                      ,time.asctime(time.localtime(time.time()))),
                     ('DAVID','Social Media Manager (Internship)',
                      'We are currently hiring for this position.',
                      'KWARA','Anter Technologies', time.asctime(time.localtime(time.time()))),
                     ('CHUCK','Civil/Structural Engineer',
                      'Vacancy For Civil/Structural Engineer at Haserv Enigeering Limited',
                      'LAGOS','Haserv Engineering Limited',time.asctime(time.localtime(time.time()))),
                     ('RAMOND','PMP Instructor',
                      'We are seeking Project Management instructors and consultants'
                      ' to work on an independent contractor basis.',
                      'LAGOS','Anonymous Employer',time.asctime(time.localtime(time.time()))),
                     ('UNICE','SQL Server Instructor','To teach both weekdays and weekends SQL Server courses.',
                      'LAGOS','Anonymous Employer', time.asctime(time.localtime(time.time()))),
                     ('TOYIN','Certified Cisco Academy Instructor',
                      'The successful candidate will be required to teach introductory and advanced'
                      ' computer networking courses in Cisco technologies and cybersecurity.',
                      'LAGOS','Anonymous Employer',time.asctime(time.localtime(time.time()))),
                     ('KEZZY','Database Engineer',
                      'Database engineers write new database programs and maintain'
                      ' existing programs to ensure they can handle the flow of traffic.',
                      'LAGOS','Insight Apex Group of Companies',time.asctime(time.localtime(time.time()))),]

    data = conn.executemany(Sqlite_insert_query, records_to_insert)
    conn.commit()


    conn.close()

home()
