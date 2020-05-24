import names


def get_name():
    new_name = names.get_full_name()
    print(f'{new_name} {len(new_name)}')


get_name()