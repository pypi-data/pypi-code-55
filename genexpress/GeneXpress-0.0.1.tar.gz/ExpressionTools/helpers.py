import os
import re
import math



def checkdir_mkdir(base, extension, *args):
    if args == ():
        path = os.path.join(base, extension)
    else:
        path = os.path.join(base, extension, *args)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def search_num_range(lower_bound: int, upper_bound: int, data: list, end=True):
    if not isinstance(lower_bound, int) \
       and not isinstance(lower_bound, float)\
       and not isinstance(lower_bound, str)\
       or not isinstance(upper_bound, int)\
       and not isinstance(upper_bound, float)\
       and not isinstance(upper_bound, str)\
       or not isinstance(data, list):
        raise TypeError
    if upper_bound == lower_bound:
        return None
    # TODO: add stuff for use case single digit to double digit (patient1 - patient12)
    upper_bound = int(upper_bound)
    lower_bound = int(lower_bound)
    if upper_bound < lower_bound:
        temp = lower_bound
        lower_bound = upper_bound
        upper_bound = temp
        del temp
    # check on same order of magnitude
    # TODO: raise error if lengths are not equal or numbers are equal
    lower_str = [i for i in str(lower_bound)]
    upper_str = [i for i in str(upper_bound)]
    leading_digits = ""
    for idx, num in enumerate(lower_str):
        if num == upper_str[idx]:
            leading_digits = leading_digits + num
        else:
            diff_idx = int(idx)
            break
    if lower_bound < 10 and upper_bound < 10:
        regex = r"(.*\D[%s-%s]" % (lower_str[0], upper_str[0])
        pattern = regex + r")"
    elif lower_bound < 10:
        lower_re = rf"(.*\D[{lower_str[0]}-9])"
        uppers = [r"[0-"+num+r"]" for num in upper_str[:-1]]
        upper_re = rf"(.*\D%s[0-{upper_str[-1]}]" % "".join(uppers)
        upper_re = upper_re.replace("\'", "")
        pattern = r"|".join([lower_re, upper_re]) + r")"
    elif len(str(upper_bound)) != len(str(lower_bound)):
        return None
    elif upper_str[-2] == lower_str[-2]:
        regex = rf"(.*{leading_digits}[{lower_str[-1]}-{upper_str[-1]}])"
        pattern = regex + r")"

    elif lower_bound > 99:
        anchor = "$"
        lower_re = rf"(.*{leading_digits}{lower_str[diff_idx]}[{lower_str[-1]}-9]{anchor})"
        upper_re = rf"(.*{leading_digits}{upper_str[diff_idx]}[0-{upper_str[-1]}]{anchor})"
        if upper_bound - lower_bound > 10:
            middle_re = rf"(.*{leading_digits}[{str(int(lower_str[diff_idx])+1)}-{str(int(upper_str[diff_idx])-1)}][0-9])"
            pattern = r"|".join([lower_re, middle_re, upper_re]) + r")"
        else:
            pattern = r"|".join([lower_re, upper_re])+ r")"

    else:
        anchor = "$"
        if lower_str[0] == upper_str[0]:
            pattern = rf".*{lower_str[0]}[{lower_str[1]}-{upper_str[1]}]" + r")"
        else:
            lower_re = rf"(.*{lower_str[0]}[{lower_str[1]}-9]{anchor})"
            upper_re = rf"(.*{upper_str[0]}[0-{upper_str[1]}]{anchor})"
            pattern = r"|".join([lower_re, upper_re]) + r")"

    if end:
        pattern = re.compile(r"(" + pattern + r")$")
    else:
        pattern = re.compile(r"^("+pattern + r")")

    return list(filter(pattern.match, data))


def search_list_of_strings(search_terms, series_to_search):
    if isinstance(search_terms, list):
        search_str = ""
        for term in search_terms:
            if term == search_terms[0]:
                search_str = r"(" + term + r")|("
            elif term == search_terms[-1]:
                search_str = search_str + term + r")"
            else:
                search_str = search_str + term + r")|("
        grouped = series_to_search.str.contains(r'%s' % search_str)
    else:
        search_str = r'%s' % search_terms
        grouped = series_to_search.str.contains(search_str)
    return grouped.astype(bool)
