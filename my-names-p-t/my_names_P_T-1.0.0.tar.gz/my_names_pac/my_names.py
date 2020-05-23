import names


def get_names():
    new_name = names.get_full_name()
    print(f'{new_name} {len(new_name)}')

get_names()