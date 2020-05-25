def testfunc():
    print("This is a test function..")


class TestClass(object):
    def __init__(self, name):
        self.name = name
        print("This is a test Class..")

    def get_name(self):
        return self.name