from clint.textui import colored
from clint.textui import puts, indent
import datetime
import json
import os
from textwrap import TextWrapper

wrapper = TextWrapper(width=80, break_long_words=False)


def check_input(*args, help_text='>>'):
    # this function helps to automaticcally check if a user inputted what was expected
    # if an unexpected input is passed it raises a error
    # pass the values user must match to this function
    valid = False
    while not valid:
        user_choice = str(input(help_text)).lower()
        loop_end = False
        for arg in args:
            if user_choice == str(arg).lower():
                valid = True
                loop_end = True
                return user_choice
        if not loop_end:
            print(colored.red('Please enter a valid command'))


def display_gossips(raw_list=None, format_=None, start=0, end=10, user=None):
    has_posts = True
    with indent(4):
        if format_ == '1':
            # For all posts
            if len(raw_list) > 0:
                puts(colored.magenta('      ---------These are the latest Posts---------'))
                puts(colored.magenta('---------------------------------------------------------------------'))
            else:
                puts(colored.yellow('There Are Currently No Posts on devGossip'))
                has_posts = False

        elif format == '2':
            # For a range of posts
            puts(colored.green(f'These are the posts from GossipTag({start}) to GossipTag({end})'))
        raw_list.reverse()
        if user:
            if raw_list:
                puts(colored.magenta(f"      ---------These are Your latest posts, {user['username'].capitalize()}---------"))
                puts(colored.magenta(f"                  ------You Have Made {len(raw_list)} So Far------"))
            else:
                puts(colored.magenta(f"      ---------{user['username'].capitalize()}, You Have No Posts Yet--------"))
                has_posts = False
            puts(colored.magenta('---------------------------------------------------------------------'))
            for item in raw_list:
                if item['author'] == user['username']:
                    wow = 'wow' if len(item['wows']) else 'wows'
                    puts(f'GossipTag({item["id"]}) <-->  {colored.magenta(item["title"]).capitalize()}.   '
                         f"Author: {colored.blue(item['author'].capitalize())}."
                         f" Posted on: {colored.blue(item['date_posted'])} {len(item['wows'])} {wow}")
        else:
            for item in raw_list[start:end]:
                wow = 'wow' if len(item['wows']) else 'wows'
                puts(f'GossipTag({item["id"]}) <-->  {colored.magenta(item["title"]).capitalize()}.   '
                     f"Author: {colored.blue(item['author'].capitalize())}."
                     f" Posted on: {colored.blue(item['date_posted'])} {len(item['wows'])} {wow}")
        print()
        if has_posts:
            puts(colored.blue('View a particular post      -------> 1'))
            puts(colored.yellow('Go back To Main Menu        -------> 2'))
            value = check_input('1', '2', help_text=' ~~> ')
        else:
            puts(colored.yellow('Go back To Main Menu                    -------> 1'))
            check_input('1')
            # We set value as Two since the receiver of 'value' when sent takes 1 as view post and 2 as Go back
            value = 2

        return value


def create_gossip(user):
    username = user['username']
    title = input('Title of the Gossip: ').lower()
    print(colored.yellow('Topic(should\'nt be more than one word but can be): '))
    topic = input('Topic: ').lower()
    body = input("Type Your Gossip Here: ")
    date_posted = datetime.datetime.now().strftime("%A %H:%M")

    print(colored.yellow('Do you want to save this gossip'))
    user_choice = check_input('y', 'n', help_text='>>Yes(y) or No(n)  ')
    if user_choice == 'y':
        gossip = {
            'author': username,
            'title': title,
            'topic': topic,
            'body': body,
            'date_posted': date_posted,
            'wows': []
        }

        return gossip

#on construction
def gossip_detail(user, data, personal_gossips=False, default_tag=None):
    if personal_gossips:
        data['gossips'] = [gossip for gossip in data['gossips'] if user['username'] == gossip['author']]
        puts(colored.yellow(f'please note that, gossipTags of another user\'s gossip is\'nt allowed'))
        puts(colored.yellow(f'To view others users gossips in detail, go to "view latest gossips in the main menu"'))
    if default_tag:
        gossip_tag = int(default_tag)
    else:
        gossip_tag = int(input('     Please Input The Target gossip\'s gossipTag: '))

    for gossip in data['gossips']:
        if gossip['id'] == gossip_tag:
            with indent(7, quote='|'):
                wow = 'wow' if len(gossip['wows']) == 0 else 'wows'
                print()
                puts(f"\t\t{colored.magenta(gossip['title'].capitalize())} "
                     f"Posted on {colored.cyan(gossip['date_posted'])}"
                     f" by {colored.green(gossip['author'])}. This Post Has {len(gossip['wows'])} {wow}")
                puts(90 * '-')
                #body_data = gossip['body'] if len(gossip['body']) < 70 else gossip['body'][:70] + '\n' + 2 * '\t' + gossip['body'][70:]
                puts(colored.cyan(f"{wrapper.fill(gossip['body'])}"))
                puts(colored.magenta(90 * '-'))
            # we check to see if current user is the author of the gossip before allowing access to deleting it
            if user['username'] == gossip['author']:
                puts(colored.blue('To Go Back To Main Menu(press 1)'))
                puts(colored.red("To Delete Post(press 2)"))
                puts(colored.cyan('To View The Comments in This Gossip Thread(Press 3)'))
                if user['username'] in gossip['wows']:
                    puts(colored.red('To UnWow This Gossip(Press 4)'))
                    value = check_input('1', '2', '3', '4', help_text=' ~~>  ')
                else:
                    puts(colored.green('To Wow This Gossip(Press 5)'))
                    value = check_input('1', '2', '3', '5',  help_text=' ~~>  ')
            else:
                puts(colored.blue('To Go Back To Main Menu(press 1)'))
                puts(colored.cyan('To View The Comments in This Gossip Thread(Press 3)'))
                if user['username'] in gossip['wows']:
                    puts(colored.red('To UnWow This Gossip(Press 4)'))
                    value = check_input('1', '3', '4', help_text=' ~~>  ')
                else:
                    puts(colored.green('To Wow This Gossip(Press 5)'))
                    value = check_input('1', '3', '5', help_text=' ~~>  ')
            if value == '4' or value == '5':
                with open('gossips.txt', 'r') as file:
                    existing_gossips = json.load(file)
                    for gossip_post in existing_gossips['gossips']:
                        if gossip['id'] == gossip_post['id']:
                            if value == '4':
                                gossip_post['wows'].remove(user['username'])
                                puts(colored.red('\n'+5*'\t' + 'You Have UnWowed this Post'))
                            elif value == '5':
                                gossip_post['wows'].append(user['username'])
                                puts(colored.green('\n'+5*'\t' + 'You Have Wowed this Post'))
                with open('gossips.txt', 'w') as file:
                    json.dump(existing_gossips, file)
                gossip_detail(user, existing_gossips, default_tag=gossip['id'])
            return {'gossip': gossip, 'value': value}
    else:
        if personal_gossips:
            puts(f"{colored.yellow('Sorry, You do not own a gossip with That Gossip Tag.')}")
        else:
            puts(f"{colored.yellow('Sorry, a gossip with that Tag does not exist.')}")
        value = check_input('1', help_text='To Go Back To Main Menu(press 1)  ')
        return {'value': value}


def delete_gossip(highest_gossip_id, gossips_list, gossip):
    # This function takes in the list of gossips,
    # and the particular gossip to be deleted.
    # It also requires the highest_gossip_id to be passed.
    puts(colored.red(f"Are You sure You Want To Delete {gossip['title']}, This Action is Irreversible"))
    delete = check_input('y', 'n', help_text='Yes, I\'m Sure(y)/No, Don\'t Delete(n) ')
    if delete == 'y':
        highest_gossip_id = highest_gossip_id
        # A list comprehension to re-input all gossips(dicts) excluding the
        # the gossip which was pass
        gossips_list = [g for g in gossips_list if g.get('id') != gossip['id']]
        with open('gossips.txt', 'w') as file:
            json.dump({'gossips': gossips_list,
                       'highest_gossip_id': highest_gossip_id}, file)
            puts(colored.green('That gossip has been successfully deleted'))


def check_file_existence(filename, data):
    """ This function helps to check if a file exists, If it doesnt, the file is created
    and is instantiated with the data variable to avoid errors when reading or writing with json
    If it does exist, but is empty, it is also instantiated with the passed data variable
    Note: all this does is set the base data structure of the file, which will be used to hold objects.
    it isn't meant for adding objects to the file"""
    data_ = data
    if os.path.exists(filename):
        # check if file is empty
        # if it is we make the base data structure a list
        # so as to avoid errors when reading from file with json
        if os.path.getsize(filename) == 0:
            with open(filename, 'w') as file:
                json.dump(data_, file)
                # check if there is any gossip in the database
        elif os.path.getsize(filename) > 0:
            return True
    else:
        with open(filename, 'w+') as file:
            json.dump(data_, file)


def register():
    # Here user is prompted for registration details which are then saved to database
    with indent(4):
        puts(colored.blue('Thank you for choosing devGossip. Here, your privacy is our number ONE concern.'))
        puts(colored.blue('Please fill in your details below and lets get you started.'))
    username = input('Please Enter Your Username: ')
    password = input('Please Enter You password: ')
    date_joined = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # check if register.txt has been created yet,
    # if not, we create it and instantiate the data as list so it can be read with json
    data = []
    check_file_existence('register.txt', data)
    # Here the details are saved into the database
    with open('register.txt') as file:
        used = False
        users = json.load(file)
        # we use four here, since file size after setting base data structure of file is four
        # so, to be sure it contains no real user data we use four
        if os.path.getsize('register.txt') > 4:
            for user_ in users:
                if user_['username'] == username:
                    used = True
        if not used:
            user = {
                'username': username,
                'password': password,
                'date_joined': date_joined,
            }
            users.append(user)

            with open('register.txt', 'w+') as file:
                json.dump(users, file)
            return user


def login(username, password):
    data = [{}]
    if check_file_existence('register.txt', data):
        with open('register.txt', 'r+') as file:
            if os.path.getsize('register.txt') > 4:
                users = json.load(file)
                for user in users:
                    if user['username'] == username and user['password'] == password:
                        return user
                else:
                    puts(colored.red('Username/Password Does not exist.', bold=True))
            else:
                puts(colored.yellow('     -------No Users In The Database, Be The first To register--------'))
    else:
        puts(colored.yellow('     -------No Users In The Database, Be The first To register--------'))


def list_gossip_comments(comment_list):
    puts(colored.magenta('                                        These Are The Comments On This Thread So Far'))
    puts(colored.cyan('          ----------------------------------------------------------------------------------------------------'))
    for comment in comment_list:
        with indent(4):
            puts(colored.green(f"\n                                           By {comment['comment_author']} {colored.black('on')} "
                               f"{colored.magenta(comment['date_posted'])}"))
            puts(colored.yellow('             ----------------------------------------------------------------------------------------'))
            wrapper.initial_indent = 3 * ' \t'
            wrapper.subsequent_indent = 3 * ' \t'
            puts(colored.cyan(f"{wrapper.fill(comment['comment_body'])}"))


def gossip_thread(gossipTag, user):
    check_file_existence('gossip_thread.txt', data=[])
    with open('gossip_thread.txt', 'r') as file:
        gossip_threads = json.load(file)
        for thread in gossip_threads:
            if thread['thread_id'] == gossipTag:
                comments = thread['comments']
                list_gossip_comments(comments)
                break
        else:
            puts(colored.yellow('This Gossip Hasn\'t Formed a Thread Yet, Be The First To Comment On It'))
        with indent(2):
            puts(colored.green('To comment On This Post, Press 1'))
            puts(colored.cyan('To Go Back To Main Menu, Press 2'))
        user_choice = check_input('1', '2', help_text=' ~~> ')
        return user_choice


def comment_on_gossip(gossipTag, user):
    comment_body = input('Type Your Comment: ')

    date_posted = date_posted = datetime.datetime.now().strftime("%A %H:%M")
    comment_author = user['username']
    comment_data = {
        'comment_body': comment_body,
        'date_posted': date_posted,
        'comment_author': comment_author
    }
    check_file_existence('gossip_thread.txt', data=[])
    with open('gossip_thread.txt', 'r') as file:
        existing_threads = json.load(file)
        # checks if a thread exists for the gossip, if it is,
        # we append a comment to the threads comment section
        # If not , we create a new thread with the gossip's gossipTag
        for thread in existing_threads:
            if thread['thread_id'] == gossipTag:
                thread['comments'].append(comment_data)
                break
        else:
            existing_threads.append({
                'thread_id': gossipTag,
                'comments': [comment_data]
            })
    with open('gossip_thread.txt', 'w') as file:
        json.dump(existing_threads, file)