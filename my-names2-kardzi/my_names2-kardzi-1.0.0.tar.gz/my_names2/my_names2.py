import names


def get_names2():
    new_name = names.get_full_name() # te metofy wzielismy z PyPi googlając opję names
    print(f'{new_name} {len(new_name)}')

get_names2()