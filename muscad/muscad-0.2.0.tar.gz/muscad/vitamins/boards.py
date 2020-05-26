from muscad import Part, Union
from muscad.utils.volume import Volume


class Board(Part):
    def init(self, width, depth, height=2, misc_height=20):
        self.board = Volume(
            center_x=0,
            width=width,
            center_y=0,
            depth=depth,
            center_z=0,
            height=height,
        )
        self.components = Volume(
            center_x=0,
            width=width,
            center_y=0,
            depth=depth,
            bottom=self.board.top,
            height=misc_height,
        )
        self.bolts = Union().misc()

    def add_bolt(self, bolt, x, y):
        if x < 0:
            x = self.board.right + x
        else:
            x = self.board.left + x

        if y < 0:
            y = self.board.front + y
        else:
            y = self.board.back + y
        self.bolts.add_child(bolt.align(center_x=x, center_y=y))
        return self

    @classmethod
    def mks_sbase(cls, bolt=None):
        board = cls(146.5, 95)
        if bolt:
            board.add_bolt(bolt, 4, 4)
            board.add_bolt(bolt, 4, -4)
            board.add_bolt(bolt, -4, -4)
            board.add_bolt(bolt, -4, 4)
        return board

    @classmethod
    def smps300rs(cls, bolt=None):
        board = cls(100, 100)
        if bolt:
            board.add_bolt(bolt, 4, 4)
            board.add_bolt(bolt, 4, -4)
            board.add_bolt(bolt, -4, -4)
            board.add_bolt(bolt, -4, 4)
        return board
