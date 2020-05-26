from clint.textui import colored
from clint.textui import puts, indent
import json
from functions import login
from functions import register
from functions import gossip_detail
from functions import check_input
from functions import create_gossip
from functions import delete_gossip
from functions import check_file_existence
from functions import display_gossips
from functions import list_gossip_comments
from functions import gossip_thread
from functions import comment_on_gossip


def app():
    print(colored.magenta('   ~~~ Welcome to devGossip. Where juicy stories lie but a click away. ~~~'))
    puts(colored.magenta('----------------------------------------------------------------------------'))

    def logged_out_menu():
        with indent(3):
            puts(colored.cyan('register  ------>     1'))
            puts(colored.cyan('login     ------>     2'))
            puts(colored.red('quit app  ------>     3'))

        user_choice = check_input('1', '2', '3', help_text='    >~~ ')
        if user_choice == '1':
            user = register()
            if user:
                print(colored.green('You Have Been Successfully Registered.'))
            else:
                print(colored.yellow('Sorry, that username is already taken'))
                logged_out_menu()
            main_menu(user, just_joined=True)
        elif user_choice == '2':
            puts(colored.blue('   Please input your details below.'))
            username = input('          Username: ')
            password = input('          Password: ')
            user = login(username, password)
            if user:
                main_menu(user, just_logged_in=True)
            else:
                logged_out_menu()
        elif user_choice == '3':
            exit()

    def main_menu(user, just_joined=False, just_logged_in=False):
        with indent(5):
            if just_joined:
                puts(colored.blue(f'Welcome, {colored.magenta(user["username"])}'
                                  f". {colored.blue('As a new user, What would You like to do first?')}"))
            elif just_logged_in:
                print()
                puts(colored.green(f"       Welcome Back, {user['username']}"))
                print(colored.green('---------------------------------------------------'))
        with indent(3):
            puts(colored.magenta('         ------Main Menu-----'))
            puts(colored.cyan('To view latest gossips          -----> 1'))
            puts(colored.cyan('To create a gossip              -----> 2'))
            puts(colored.cyan('To check gossips you\'ve made    -----> 3'))
            puts(colored.blue('Log out                         -----> 4'))
            print(colored.magenta(55 * '-'))

        user_choice = check_input('1', '2', '3', '4', help_text='    ~~>')
        if user_choice == '1':
            base_data_structure = {'gossips': []}
            is_file = check_file_existence('gossips.txt', base_data_structure)
            if is_file:
                with open('gossips.txt', 'r') as file:
                    data = json.load(file)
                    gossip_count = len(data['gossips'])
                    with indent(2, quote='>'):
                        puts(colored.green(f"Number of gossips ever made on devGossip: {gossip_count}"))
                        puts(colored.yellow("Please Note That To Get A specific Post You need the GossipTag"))
                        if gossip_count > 9:
                            puts(colored.blue("For latest Ten gossips           ----> press 1"))
                        else:
                            puts(colored.blue(f"For latest {gossip_count} gossips             ----> press 1"))
                        puts(colored.blue("To get a range of gossips        ----> press 2"))
                        puts(colored.blue("To get a specific post           ----> press 3"))
                        puts(colored.magenta(70 * '-'))

                    gossips_display_choice = check_input('1', '2', '3', help_text='  ~~~> ')
                    if gossips_display_choice == '1':
                        value = display_gossips(data['gossips'], gossips_display_choice)
                        if value == '1':
                            context = gossip_detail(user, data)
                            print(context)
                            if context.get('gossip'):
                                if context['value'] == '1':
                                    main_menu(user)
                                elif context['value'] == '2':
                                    delete_gossip(data['highest_gossip_id'],
                                                  data['gossips'],
                                                  context['gossip'])
                                    main_menu(user)
                                elif context['value'] == '3':
                                    # we set a while True loop so if user choice is 1,
                                    # the comment is added and the user is taken back to the gossip thread
                                    while True:
                                        user_choice = gossip_thread(context['gossip']['id'], user)
                                        if user_choice == '1':
                                            comment_on_gossip(context["gossip"]["id"], user)
                                        else:
                                            main_menu(user)

                            else:
                                main_menu(user)
                        else:
                            main_menu(user)
                    elif gossips_display_choice == '2':
                        puts(colored.blue(f"You can pick from 1 and {gossip_count}"))
                        puts(colored.yellow(
                            f"If your starting value is not valid, This will default to the latest gossip"))
                        try:
                            start_point = int(input('Value of starting Point: '))
                            if not (start_point > 0 and  start_point <= gossip_count):
                                puts(colored.red(f'That was not a valid starting point, sorry'))
                                puts(colored.blue(f'Starting point is now set as One'))
                                start_point = 0
                        except ValueError:
                            puts(colored.red(f'That was not a valid starting point, sorry'))
                            puts(colored.blue(f'Starting point is now set as One'))
                            start_point = 0
                        start_point = start_point - 1 if start_point > 0 else start_point
                        puts(colored.yellow(f"Your closing value should be valid(i.e: must be a number,"
                                            f" not be lesser than start value and not greater than amount of gossips in the database)"))
                        try:
                            end_point = int(input('Value of ending Point: '))
                        except ValueError:
                            if (gossip_count - start_point) > 10:
                                end_point = 9 + start_point
                            else:
                                end_point = gossip_count
                            puts(colored.red(f'That was not a valid closing point, sorry'))
                            puts(colored.red(f'Closing is now set to {end_point}'))
                        if end_point < start_point or end_point > gossip_count:
                            puts(colored.red(f'That was not a valid closing point, sorry'))
                            if (gossip_count - start_point) > 10:
                                puts(colored.blue(f'Closing point is now set to '
                                                  f'{10 + start_point}'))
                                end_point = 9 + start_point
                            else:
                                puts(colored.yellow(f'Since there are only {gossip_count} gossips made'))
                                puts(colored.blue(f'Closing point is now set to '
                                                  f'{gossip_count}'))
                                end_point = gossip_count
                        end_point = end_point + 1

                        value = display_gossips(data['gossips'],
                                        gossips_display_choice, start=start_point, end=end_point)
                        if value == '1':
                            context = gossip_detail(user, data)
                            if context.get('gossip'):
                                if context['value'] == '1':
                                    main_menu(user)
                                elif context['value'] == '2':
                                    delete_gossip(data['highest_gossip_id'],
                                                  data['gossips'],
                                                  context['gossip'])
                                    main_menu(user)
                                elif context['value'] == '3':
                                    # we set a while True loop so if user choice is 1,
                                    # the comment is added and the user is taken back to the gossip thread
                                    while True:
                                        user_choice = gossip_thread(context['gossip']['id'], user)
                                        if user_choice == '1':
                                            comment_on_gossip(context["gossip"]["id"], user)
                                        else:
                                            main_menu(user)
                            else:
                                main_menu(user)
                        else:
                            main_menu(user)
                    elif gossips_display_choice == '3':
                        context = gossip_detail(user, data)
                        if context.get('gossip'):
                            if context['value'] == '1':
                                main_menu(user)
                            elif context['value'] == '2':
                                delete_gossip(data['highest_gossip_id'],
                                              data['gossips'],
                                              context['gossip'])
                                main_menu(user)
                            elif context['value'] == '3':
                                user_choice = gossip_thread(context['gossip']['id'], user)
                                if user_choice == '1':
                                    comment_on_gossip(context["gossip"]["id"], user)
                                    gossip_thread(context["gossip"]["id"], user)
                                else:
                                    main_menu(user)
                        else:
                            main_menu(user)

            else:
                puts(colored.yellow("There are no gossips yet"))
                main_menu(user)

        elif user_choice == '2':
            gossip = create_gossip(user)
            if gossip:
                base_data_structure = {'gossips': []}
                check_file_existence('gossips.txt', base_data_structure)
                with open('gossips.txt', 'r') as file:
                    existing_gossips = json.load(file)

                    # check if the gossips.txt has a 'highest_gossip_id' key.
                    # If not, instantiate it with value of Zero
                    if not existing_gossips.get('highest_gossip_id'):
                        existing_gossips['highest_gossip_id'] = 0
                    latest_id = existing_gossips['highest_gossip_id'] + 1
                    gossip['id'] = latest_id
                    existing_gossips['gossips'].append(gossip)
                    existing_gossips['highest_gossip_id'] = latest_id
                with open('gossips.txt', 'w') as file:
                    json.dump(existing_gossips, file)
            main_menu(user)
        elif user_choice == '3':
            check_file_existence('gossips.txt', {'gossips':[]})
            with open('gossips.txt', 'r') as file:
                data = json.load(file)
                gossip_list = data['gossips']
                value = display_gossips(gossip_list, user=user)
                if value == '1':
                    context = gossip_detail(user, data, personal_gossips=True)
                    if context.get('gossip'):
                        if context['value'] == '1':
                            main_menu(user)
                        elif context['value'] == '2':
                            delete_gossip(data['highest_gossip_id'],
                                          data['gossips'],
                                          context['gossip'])
                        elif context['value'] == '3':
                            # we set a while True loop so if user choice is 1,
                            # the comment is added and the user is taken back to the gossip thread
                            while True:
                                user_choice = gossip_thread(context['gossip']['id'], user)
                                if user_choice == '1':
                                    comment_on_gossip(context["gossip"]["id"], user)
                                else:
                                    main_menu(user)

                    else:
                        main_menu(user)
                else:
                    main_menu(user)
        elif user_choice == '4':
            logged_out_menu()

    logged_out_menu()


app()

