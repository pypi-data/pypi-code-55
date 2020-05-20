def string_between(string: str, from_str: str, to_str: str) -> str:
    try:
        return string.split(from_str)[1].split(to_str)[0]
    except:
        return None