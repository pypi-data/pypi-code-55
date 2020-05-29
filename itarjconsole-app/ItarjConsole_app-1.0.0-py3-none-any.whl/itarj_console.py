import sys
import json
import os

def main():
    '''Introductory message to users'''
    print(
        '''
        Welcome to Itarj CLI Application.
        Home to check authenticity of an advertise jobs
        Get started by signing up.
        Enjoy as you explore the application
        
        1. Create account
        2. Login
        3. Search job by keyword
        4. View registered jobs
        5. Exit
        '''
    )
    users_choice = input('>>> ')
    if users_choice == '1':
        return registration()
    elif users_choice == '2':
        return login()
    elif users_choice == '3':
        return keywords()
    elif users_choice == '4':
        return job_list()
    elif users_choice == '5':
        return exit()
    print('Please enter a valid number')
    return main()

def registration():
    #### Register a user ####
    print('Welcome!\nRegister to get started\n')
    inputdata = {} # Container that will hold user details before writing to a file

    fullname = input('Full name:  ')
    email = input('Email address: ').lower()
    phone_number = input('Phone number: ')
    password = input('Password: ')
    # append to users dictionary
    inputdata['users'] = {}
    inputdata['users'][email] = {}
    inputdata['users'][email].update({
        'Fullname': fullname,
        'Phonenumber': phone_number,
        'Password': password
    })
    # appending to a file
    if os.path.isfile('data.txt'):
        with open('data.txt', 'r') as users_file:
            dataFile = json.load(users_file)
        # Check if email already exists
        if email in dataFile['users'].keys():
            print ('------------   Can not register this email. Email already in use. -----------------')
            return login()

        dataFile['users'].update(inputdata['users'])
        with open('data.txt', 'w') as users_file:
            json.dump(dataFile, users_file, indent=4)

    else:
        with open('data.txt', 'w') as users_file:
            json.dump(inputdata, users_file, indent=4)
    login()

def login():
    ''' Check if a user has registered and login the user after authentication''' 
    print('''----  Don't have an account yet?  ------\n
    --------    1. Create account           ------ \n
    --------    2. Continue to login          ------ \n
    --------    3. Search job by keyword(s)        .........\n
    --------    4. View registered jobs         ------- \n
    --------    5. Exit the application         ------------''')
    user_response = input('>>> ')
    if user_response == '1':
        return registration()
    elif user_response == '3':
        return keywords()
    elif user_response == '4':
        return job_list()
    elif user_response == '5':
        return quit()
    
    with open('data.txt') as users_file:
        data = json.load(users_file)
        Email = input("Email: ").lower()
        Password =input("Password: ")
        userEmailList = list(data['users'].keys())
        if Email not in userEmailList:
            print ('Email is not registered.')
            return login()
        fooPassword = data['users'][Email]['Password']
        if fooPassword == Password:
            x = Email
            y = fooPassword
            x == y  is True   
            print (f"Welcome! {Email}")
            print('''
    --------    1. Search job by keyword           ------ \n\n
    --------    2. Register a job          ------ \n\n
    --------    3. View registered jobs        .........\n\n
    --------    4. Exit the application         ------------
            ''')
            keyword_post = input('>>> ')
            if keyword_post == '1':
                return keywords()
            elif keyword_post == '2':
                return register_job()
            elif keyword_post == '3':
                return job_list()
            return quit()
        else:
            print('-------------------------      Invalid password.        -------------------------')
            print('')
            return login()

def register_job():
    '''Promp user to register a job'''
    jobs = {}
    company = input('Company name: ')
    title = input('Job title: ')
    detail = input('Job details: ')
    deadline = input('Job deadline: ')
    # append to data dictionary
    jobs['Post'] = []
    jobs['Post'].append({
        'Company': company,
        'Title': title,
        'Detail': detail,
        'Deadline': deadline
    })
    # appending to a file
    if os.path.isfile('jobs.txt'):
        with open('jobs.txt', 'r') as users_file:
            dataFile = json.load(users_file)
        dataFile['Post'].append(jobs['Post'][0])
        with open('jobs.txt', 'w') as users_file:
            json.dump(dataFile, users_file, indent=4)
            print('Job registered successfully')
        print('''
        ------ 1. Register again ------
        ------ 2. Search for registered job ------
        ------ 3. Logout ------
        ------ 4. View registered jobs ------
            ''')
        user_choice = input('>>> ')
        if user_choice == '1':
            return register_job()
        elif user_choice == '2':
            return keywords()
        elif user_choice == '3':
            return quit() 
        elif user_choice == '4':
            return job_list()
    else:
        with open('jobs.txt', 'w') as users_file:
            json.dump(jobs, users_file, indent=4)
            
def job_list():
    ''' Display list of registered jobs '''
    with open('jobs.txt') as users_file:
        jobs = json.load(users_file)
        for job in jobs['Post']:
            print(job)
    print('''
    --------    1. Go back to main menu    ------ 
            ''')
    choice = input('>>> ')
    if choice == '1':
        return main()

def keywords():
    ''' 
    Users can only search jobs by job title.
    '''
    print('Enter job title')
    print('')
    search_job = input('>>> ')
    with open('jobs.txt') as users_file:
        jobs = json.load(users_file)
        for job in jobs['Post']: # Check if job is registered.
            if job['Title'] == search_job:
                print('The following results matched your search.')
                print('')
                print(job)
                # Return user to main menu
                print(''' ----- 1. Go back to main menu -----''')
                main_menu = input('>>> ')
                if main_menu == '1':
                    return main()
            else:
                print('')
                print('Job not found')
                print('')
                print('''
    --------    1. Search again    ------ \n\n
    --------    2. View registered jobs    .........\n\n
    --------    3. Exit the application     ------------
            ''')
                user_choice = input('>>> ')
                if user_choice == '1':
                    return keywords()
                elif user_choice == '2':
                    return job_list()
                return quit()        
def quit():
    return sys.exit



main()






