import bext, random

w, h = bext.size()
w -= 1

for i in range(100):
    for x in range(w):
        for y in range(h):
            bext._goto_win32_api(x,y)
            print('ab'[i%2], end='')

for i in range(100):
    for x in range(w):
        for y in range(h):
            bext._goto_control_code(x,y)
            print('xy'[i%2], end='')
