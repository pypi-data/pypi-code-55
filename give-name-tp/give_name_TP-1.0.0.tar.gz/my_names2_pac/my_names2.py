import names
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gender", help="returning random male with specified gender", choices=['male','female'])

args = parser.parse_args()



def get_names_2():
    if args.gender == 'male':
        new_name = names.get_full_name('male')
    elif args.gender == 'female':
        new_name = names.get_full_name('female')
    else:
        new_name = names.get_full_name()

    print(f'{new_name} {len(new_name)}')


get_names_2()