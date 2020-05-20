import datetime

from blessed import Terminal

term = Terminal()

LANGUAGES = ['Any language','Afrikaans', 'Albanian', 'Azerbaijani', 'Bashkir', 'Belarusian', 'Bengali', 'Bulgarian', 'Catalan',
        'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Finnish', 'French', 'Georgian',
        'German', 'Greek', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indigenous', 'Indonesian', 'Italian',
        'Japanese', 'Kazakh', 'Kirghgiz', 'Korean', 'Latin', 'Latvian', 'Lithuanian', 'Malayalam', 'Marathi',
        'Mongolian', 'Nepali', 'Norwegian', 'Persian', 'Polish', 'Portugese', 'Romanian', 'Russian', 'Sanskrit',
        'Serbian', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Swedish', 'Tajik', 'Tatar', 'Turkish',
        'Ukranian', 'Urdu', 'Uzbek', 'Vietnamese']

class Menu():

    def __init__(self, items):
        self.items = items
        self.itemSelected = 0

    def showItems(self, itemSelected=0):
        '''Draws the Menu'''

        print(term.home + term.clear + term.move_xy(0,0))
        for i,item in enumerate(self.items):
            if i == self.itemSelected:
                print(item.title + ":" + term.move_x(term.width//3) +
                        term.black_on_cyan
                        + "< " + item.options[item.optionSelected] + " >"+ term.normal)
            else:
                print(item.title +":"+ term.move_x(term.width//3) +
                        "< " + item.options[item.optionSelected] + " >")

    def changeOption(self, direction):
        '''Change the option of an Item'''

        print(term.home + term.clear)
        currOption = self.items[self.itemSelected].optionSelected
        if direction == "right":
            if currOption == len(self.items[self.itemSelected].options)-1:
                    self.items[self.itemSelected].optionSelected = 0
            else:
                    self.items[self.itemSelected].optionSelected += 1
        elif direction == "left":
            if currOption == 0:
                    self.items[self.itemSelected].optionSelected =len(self.items[self.itemSelected].options)-1
            else:
                self.items[self.itemSelected].optionSelected -= 1
        self.showItems()

    def scroll(self,direction):
        '''Scrolls through the Items of the Menu'''
        print(term.home + term.clear)

        if direction == "down":
            if self.itemSelected == len(self.items)-1:
                self.itemSelected = 0
            else:
                self.itemSelected += 1

        elif direction == "up":
            if self.itemSelected == 0:
                self.itemSelected = len(self.items)-1
            else:
                self.itemSelected -= 1
        self.showItems()

    def getAll(self):
        '''Returns a dictionnary with ids of the Items as keys
        and the string of the option as the value. Called before
        exiting the menu.
        '''
        result = {}
        for e in self.items:
            result[e.id] = e.options[e.optionSelected]

        return result


class Item():
    
    def __init__(self, title, options,itemId):
        self.title = title
        self.options = options
        self.id = itemId
        self.optionSelected = 0


    def setToDefault(self):
        '''Sets the option selected to default
        (the first option'''
        self.optionSelected = 0

