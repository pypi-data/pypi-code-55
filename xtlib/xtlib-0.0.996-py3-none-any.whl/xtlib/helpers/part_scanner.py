# part_scanner.py: works like a scanner for a list of parts

class PartScanner():
    def __init__(self, parts):
        self.parts = parts
        self.index = 0
        self.part = None

    def scan(self):
        if self.index < len(self.parts):
            self.part = self.parts[self.index]
            self.index += 1
        else:
            self.part = None

        return self.part
    
    def peek(self):
        if self.index < len(self.parts):
            part = self.parts[self.index]
        else:
            part = None

        return part