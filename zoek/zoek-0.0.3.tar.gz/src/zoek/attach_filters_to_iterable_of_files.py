import time
import operator

from zoek.filter_on_one_attribute import filter_on_one_attribute
from zoek._custom_operators import string_contains, string_begins_with


def attach_filters_to_iterable_of_files(files, depth, showpath, startswith,
                                        minsize, contains, datecreated, datemodified):
    if startswith:
        files = filter_on_one_attribute(generator=files,
                                        attributeType="name",
                                        condition_checker=string_begins_with,
                                        value=startswith)

    if contains:
        files = filter_on_one_attribute(generator=files,
                                        attributeType="name",
                                        condition_checker=string_contains,
                                        value=contains)

    if minsize:
        files = filter_on_one_attribute(generator=files,
                                        attributeType="st_size",
                                        condition_checker=operator.ge,
                                        value=minsize)

    if datecreated:
        timeNow = time.time()
        ageInUnix = timeNow - (abs(datecreated) * 60)
        files = filter_on_one_attribute(generator=files,
                                        attributeType="st_ctime",
                                        condition_checker=operator.ge if datecreated <= 0 else operator.lt,
                                        value=ageInUnix)

    if datemodified:
        if "ageInUnix" not in locals():
            timeNow = time.time()
            ageInUnix = timeNow - (abs(datemodified) * 60)

        files = filter_on_one_attribute(generator=files,
                                        attributeType="st_mtime",
                                        condition_checker=operator.ge if datemodified <= 0 else operator.lt,
                                        value=ageInUnix)

    return files
