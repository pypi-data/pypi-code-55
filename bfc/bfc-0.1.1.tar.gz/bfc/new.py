from os import walk

def dirWalk():
    root = '.'
    for dir_, subdir, files in walk(root):
        print(f'dir: {dir_}')
        for name in files:
            print(f'  {name}')

if __name__ == '__main__':
    dirWalk()

