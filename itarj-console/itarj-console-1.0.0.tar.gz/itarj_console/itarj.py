import sys
import re
import time


def is_this_a_real_job():
    # allow user add a new fake job alert
    def add_fake_job():
        print("Please provide the following:")

        while True:
            company_name = input("Company/Job name: ").lower()
            company_address = input("Company address: ").lower()
            if len(company_name) < 2 or len(company_address) < 2:
                print("Name and address must be at least 3 characters long")
            else:
                break
        job_description = input("job description/experience: ").lower()
        print("Your entry has been registered successfully. Please see the details below...")
        time.sleep(2)
        print(f'\nName: {company_name}, \nAddress: {company_address}, \nDescription: {job_description}')

        # append user's job alert entry into itarj.txt
        with open('itarj.txt', 'a') as add_new:
            add_new.write('Company/job name : ' + company_name + ', ')
            add_new.write('Company Address : ' + company_address + ', ')
            add_new.write('Job Description/Experience : ' + job_description + '\n')

        time.sleep(2)
        user_options()

    def login():
        username = input("Enter your username: \n")
        username = username.lower()
        password = input("Enter your password(password is case-sensitive): \n")
        # password = str(password)

        with open("users.txt", "r") as log_in:
            user_exists = log_in.readlines()
            for line in user_exists:
                line = line.strip().split(',')

                if (username == line[0]) and (password == line[1]):
                    print("login successful!")
                    add_fake_job()

            else:
                print("Invalid username or password!")
                user_login()

    def sign_up():
        new_username = input("Enter your username: \n").lower()

        while True:
            new_email = input("Enter your email: \n")

            if not re.match(r"A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z", new_email,
                            re.IGNORECASE):
                print("invalid format. Enter a valid email address")
                time.sleep(1)
            else:
                break

        while True:
            new_password = input("Enter your password(at least 5 char): \n")
            if len(new_password) < 5:
                print("Password must be at least 5 characters long!")
                time.sleep(1)
            else:
                break

        with open("users.txt", "a") as new_account:
            new_account.write(new_username + ',')
            new_account.write(new_password + ',')
            new_account.write(new_email + '\n')

        print("Registration successful! \n")
        time.sleep(1)
        add_fake_job()

    def user_login():
        user = 0

        while True:
            try:
                while (user < 1) or (user > 4):
                    print(''' Choose one of the following options:
                    1. Login
                    2. Sign up
                    3. Back to menu
                    4. Close program
                    ''')
                    user = int(input('>'))
                break
            except ValueError:
                print("Invalid selection! You can only type in a number.")
                time.sleep(1)
        if user == 1:
            login()

        elif user == 2:
            sign_up()

        elif user == 3:
            user_options()

        elif user == 4:
            print("Goodbye")
            time.sleep(2)
            sys.exit()

    def job_is_real():
        print("For clarity sake, please supply the following:")
        company_name = input("company name: ")
        company_address = input("address: ")
        job_prove = input('Please supply your prove that the job is real here: \n> ')

        with open('prove.txt', 'a') as prove:
            prove.write('Company name: ' + company_name + '. ')
            prove.write('Company address: ' + company_address + '. ')
            prove.write('Prove of being legit:' + job_prove)

        print("Please wait...")
        time.sleep(2)
        print(
            "Your prove has been recorded successfully. \nPlease note: Acceptance would take a while as an admin would "
            "have to validate your entry first")
        time.sleep(3)
        user_options()

    def view_fake_job():
        print("Please enter a keyword to search for a job advert or company")
        keyword_searched = input('> ').lower()

        with open('itarj.txt', 'r') as search_job:
            jobs = search_job.readlines()
            for line in jobs:
                if re.search(keyword_searched, line):
                    print(line.title())
                    time.sleep(2)

                    fake_job_is_real = input(
                        "Do you believe this entry is false and can you prove it? Yes/No \n>").lower()

                    if fake_job_is_real == 'yes':
                        job_is_real()

                    elif fake_job_is_real == 'no':
                        user_options()

                    else:
                        print("You entered a wrong option.")
                        time.sleep(2)
                        user_options()

            else:
                print(
                    'This job does not exist in our log at the time. Is this a fake job and would you like to '
                    'register it? Yes/No\n')
                register_job = input('> ').lower()
                if register_job == 'yes':
                    user_login()

                elif register_job == 'no':
                    user_options()

                else:
                    print("Invalid response!")
                    user_options()

    print(
        'Welcome to ITARJ - Is This A Real Job. A console app that helps you keep track of fake recruitment '
        'agencies/job alerts to avoid scam.')

    def user_options():
        to_do = 0
        print(''' 
             1. Add/Register a new job listing 
             2. View existing fake jobs 
             3. Close the program:''')

        while True:
            try:
                while (to_do < 1) or (to_do > 3):
                    to_do = int(input("Please select a number from the above menu... \n> "))
                break
            except ValueError:
                print("Invalid selection! You can only type in a number.")
                time.sleep(1)

        if to_do == 1:
            user_login()

        elif to_do == 2:
            view_fake_job()

        elif to_do == 3:
            print("Goodbye")
            time.sleep(2)
            sys.exit()

    user_options()


is_this_a_real_job()
