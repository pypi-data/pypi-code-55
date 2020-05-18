#!/usr/bin/env python3

# © 2020, Midgard
# License: LGPL-3.0-or-later

from ipo import ipo, list, str, sort, take, skip, before, \
	from_csv, to_csv, print as ipoprint, starmap



# Chaining without adding data yet. And this ipo will be useful for the later examples, too. Bam!
print_as_list = list | str | ipoprint

# Ipo makes data flows much easier to follow
[5, 2, 3, 1, 4] | sort           | print_as_list  # [1, 2, 3, 4, 5]
[5, 2, 3, 1, 4] | take(3)        | print_as_list  # [5, 2, 3, 1, 4]
[5, 2, 3, 1, 4] | sort | take(3) | print_as_list  # [1, 2, 3]
[5, 2, 3, 1, 4] | take(3) | sort | print_as_list  # [2, 3, 5]

# Compare to the original!
sort(take([5, 2, 3, 1, 4], 3))

print()



# Ipo is ideally suited for working with CSV data
"""
#Tension,Current
12,1
8,2
220,6
""".strip().split() | from_csv | skip(1) | \
	starmap(lambda v, a: (v, a, float(v) * float(a))) | to_csv | \
	before(["#Tension,Current,Power"]) | ipoprint
