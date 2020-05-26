from muscad import Circle, Hull, Object, Square, calc


class Surface:
    """
    Helpers to create 2D surfaces
    """

    @classmethod
    def square(
        cls,
        left: float = None,
        center_x: float = None,
        right: float = None,
        back: float = None,
        center_y: float = None,
        front: float = None,
        width: float = None,
        depth: float = None,
    ):
        """
        Makes a square surface
        """
        left, center_x, right, width = calc(left, center_x, right, width)
        back, center_y, front, depth = calc(back, center_y, front, depth)
        return Square(width, depth).align(left=left, back=back)

    @classmethod
    def free(cls, *children):
        return Hull(*children)

    @classmethod
    def custom_corners(
        cls,
        fl: Object,
        fr: Object,
        br: Object,
        bl: Object,
        left: float = None,
        center_x: float = None,
        right: float = None,
        back: float = None,
        center_y: float = None,
        front: float = None,
        width: float = None,
        depth: float = None,
    ):
        """
        Makes a square surface with any 2D primitive as corners
        """
        left, center_x, right, width = calc(left, center_x, right, width)
        back, center_y, front, depth = calc(back, center_y, front, depth)
        return Hull(
            fl.align(left=left, front=front),
            fr.align(right=right, front=front),
            br.align(right=right, back=back),
            bl.align(left=left, back=back),
        )

    @classmethod
    def rounded_corners(
        cls,
        fl: float = 0,
        fr: float = 0,
        br: float = 0,
        bl: float = 0,
        **kwargs,
    ):
        """
        Makes a square surface with rounded corners. Each corner can have a different radius
        """
        return cls.custom_corners(
            fl=Circle(fl) if fl > 0 else Square(1, 1),
            fr=Circle(fr) if fr > 0 else Square(1, 1),
            br=Circle(br) if br > 0 else Square(1, 1),
            bl=Circle(bl) if bl > 0 else Square(1, 1),
            **kwargs,
        )

    @classmethod
    def regular_rounded_corners(cls, d: float, **kwargs: float):
        """
        Makes a square surface with regular rounded corners.
        :param d:
        :param kwargs:
        :return:
        """
        return cls.rounded_corners(d, d, d, d, **kwargs)

    @classmethod
    def circle_from_3_points(cls, x1, y1, x2, y2, x3, y3):
        """
        Draws a circle from 3 points.
        :param x1: first point X coordinate
        :param y1: first point Y coordinate
        :param x2: second point X coordinate
        :param y2: second point Y coordinate
        :param x3: third point X coordinate
        :param y3: third point Y coordiante
        :return: a Surface that is a Circle touching the 3 points
        """
        temp = x2 ** 2 + y2 ** 2
        bc = (x1 ** 2 + y1 ** 2 - temp) / 2
        cd = (temp - x3 ** 2 - y3 ** 2) / 2
        det = (x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2)

        if abs(det) < 1.0e-6:
            raise ValueError("Unable to draw a circle from those 3 points")

        cx = (bc * (y2 - y3) - cd * (y1 - y2)) / det
        cy = ((x1 - x2) * cd - (x2 - x3) * bc) / det

        diameter = ((cx - x1) ** 2 + (cy - y1) ** 2) ** 0.5 * 2
        return Circle(d=diameter).align(center_x=cx, center_y=cy)
