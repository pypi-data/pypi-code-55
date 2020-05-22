foreground = {
    'black': '\033[30m',
    'grey': '\033[90m',
    'dark_red': '\033[31m',
    'red': '\033[91m',
    'green': '\033[32m',
    'light_green': '\033[92m',
    'yellow': '\033[33m',
    'light_yellow': '\033[93m',
    'blue': '\033[34m',
    'light_blue': '\033[94m',
    'purple': '\033[35m',
    'pink': '\033[95m',
    'cyan': '\033[36m',
    'light_cyan': '\033[96m',
    'white': '\033[37m',
    'light_white': '\033[97m',
}

background = {
    'black': '\033[40m',
    'grey': '\033[100m',
    'dark_red': '\033[41m',
    'red': '\033[101m',
    'green': '\033[42m',
    'light_green': '\033[102m',
    'yellow': '\033[43m',
    'light_yellow': '\033[103m',
    'blue': '\033[44m',
    'light_blue': '\033[104m',
    'purple': '\033[45m',
    'pink': '\033[105m',
    'cyan': '\033[46m',
    'light_cyan': '\033[106m',
    'white': '\033[47m',
    'light_white': '\033[107m',
}

foreground_id = {
    '0': '\033[30m',
    '1': '\033[90m',
    '2': '\033[31m',
    '3': '\033[91m',
    '4': '\033[32m',
    '5': '\033[92m',
    '6': '\033[33m',
    '7': '\033[93m',
    '8': '\033[34m',
    '9': '\033[94m',
    '10': '\033[35m',
    '11': '\033[95m',
    '12': '\033[36m',
    '13': '\033[96m',
    '14': '\033[37m',
    '15': '\033[97m',
    
}

background_id = {
    '0': '\033[40m',
    '1': '\033[100m',
    '2': '\033[41m',
    '3': '\033[101m',
    '4': '\033[42m',
    '5': '\033[102m',
    '6': '\033[43m',
    '7': '\033[103m',
    '8': '\033[44m',
    '9': '\033[104m',
    '10': '\033[45m',
    '11': '\033[105m',
    '12': '\033[46m',
    '13': '\033[106m',
    '14': '\033[47m',
    '15': '\033[107m',
}


def colored(text, fg=None, bg=None, clear_last=True, **kwargs):
    if fg != None:
        try:
            text = foreground_id[str(fg)] + str(text)
        except:
            text = foreground[fg] + str(text)
    if bg != None:
        try:
            text = background_id[str(bg)] + str(text)
        except:
            text = background[bg] + str(text)
    if clear_last == True:
        text = str(text) + '\033[0m'
    return text


def cprint(text, fg=None, bg=None, clear_last=True, **kwargs):
    print(colored(text, fg, bg, clear_last))

def init():
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

init()

def test(text):
    for i in range(16):
        print(colored(text, fg = i, bg = "0"),colored(text, fg = i, bg = "1"),colored(text, fg = i, bg = "2"),colored(text, fg = i, bg = "3"),colored(text, fg = i, bg = "4"),colored(text, fg = i, bg = "5"),colored(text, fg = i, bg = "6"),colored(text, fg = i, bg = "7"),colored(text, fg = i, bg = "8"),colored(text, fg = i, bg = "9"),colored(text, fg = i, bg = "10"),colored(text, fg = i, bg = "11"),colored(text, fg = i, bg = "12"),colored(text, fg = i, bg = "13"),colored(text, fg = i, bg = "14"),colored(text, fg = i, bg = "15"),colored(text, fg = i, bg = "0"))


if __name__ == "__main__":
    test("a")