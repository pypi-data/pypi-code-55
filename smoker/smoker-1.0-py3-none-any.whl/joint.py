class Joint:
    def __init__(self, flower_name, size):
        self.flower_name = flower_name
        self.size = size

    def lightIt(self):
        size = self.size
        while size > 3:
            print(f"smoked: {size}")
            size -= 1
        else:
            print("save butt")

morning = Joint("chala", 35)
morning.lightIt()