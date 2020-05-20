import math

from blessed import Terminal

term = Terminal()

h="─"
v="│"
tr="┐"
br="┘"
tl="┌"
bl="└"


class Box:
    
    def __init__(self,width=20,height=20,x=0,y=0):
        self.width = width
        self.height = height
        self.x=x
        self.y=y

        self.cursor_x = self.x + 1
        self.cursor_y = self.y + 1

        self.content=""

    def draw(self,color="white"):
        '''Draws the borders of the box'''
        #top
        print(term.move_xy(self.x,self.y) + getattr(term, color) + tl + h*(self.width-2)+
                tr + term.normal)
        
        #sides
        for i in range(self.height-2):
            print(term.move_xy(self.x,self.y+i+1) + getattr(term, color) + v)
            print(term.move_xy(self.x+self.width-1,self.y+i+1) +
                    getattr(term,color)+ v + term.normal)
        
        #bottom
        print(term.move_xy(self.x,self.y+self.height-1) + getattr(term,color)+ bl +
                h*(self.width-2) + br + term.normal)

    def write(self,msg,color="white"):
        '''Appends the content of msg in the box and wraps the words. The
        function can accept newline characters. If a word does not fit in the
        width of the box, the function won't write anything.
        Returns None if the message couldn't be appended
        '''
        lines = msg.splitlines()

        newlines = len(lines)
        chars = 0
        for line in lines:
            chars += len(line)
        newlines += math.ceil(chars / (self.width-2))
        if self.cursor_y+newlines > self.height+2:
            return None
        
        for i,line in enumerate(lines):
            line = line.split()
            for word in line:
                if len(word) + 2 > self.x+self.width:
                    return None
                if self.cursor_x+ len(word) +2> self.x+self.width:
                    self.cursor_x = self.x+1
                    self.cursor_y += 1
                if self.cursor_y <= self.y + self.height-2:
                    print(term.move_xy(self.cursor_x,self.cursor_y) +
                            getattr(term,color) + word)
                    self.cursor_x += len(word) + 1
                else:
                    return None
            self.cursor_y += 1
            self.cursor_x = self.x+1
        
        return msg

    def clear(self):
        '''Fills the the box with spaces and resets cursor'''
        for i in range(self.height-2):
            print(term.move_xy(self.x+1,self.y+1+i) + " "*(int(self.width)-2))

        self.cursor_x = self.x+1
        self.cursor_y = self.y+1


class SearchBox(Box):

    def __init__(self,width=20,x=0,y=0):
        super().__init__(width,3,x,y)
        self.content = ""

    def write(self,msg,color="white"):
        '''Writes the message to the search box. When the box is full, the
        content is sliced like a normal search box
        '''
        self.content += msg
        self.clear()
        if len(self.content) < self.width-1:
            print(term.move_xy(self.x+1,self.y+1)+self.content)
        else:
            print(term.move_xy(self.x+1,self.y+1)+self.content[len(self.content)-self.width+2:])


    def backspace(self):
        '''Removes the last character'''
        self.content = self.content[:-1]
        self.write("")
    
    def clearContent(self):
        '''Clears the content of the search box'''
        self.content=""
