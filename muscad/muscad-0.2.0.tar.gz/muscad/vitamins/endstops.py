from muscad import Circle, Cube, Cylinder, Part
from muscad.utils.surface import Surface
from muscad.vitamins.bolts import Bolt


class OptoSwitch(Part):
    base = Cube(24.5, 3.5, 6.4)
    left_side = Cube(4.45, 11.3, 6.3).align(
        left=base.left + 6.63, back=base.back, bottom=base.bottom
    )
    right_side = Cube(4.45, 11.3, 6.3).align(
        right=base.right - 6.63, back=base.back, bottom=base.bottom
    )

    left_hole = (
        ~Cylinder(d=3, h=4.5)
        .bottom_to_front()
        .align(
            center_x=base.left + 2.75,
            center_y=base.center_y,
            center_z=base.center_z,
        )
    )
    right_hole = (
        ~Cylinder(d=3, h=4.5)
        .bottom_to_front()
        .align(
            center_x=base.right - 2.75,
            center_y=base.center_y,
            center_z=base.center_z,
        )
    )


class OpticalEndstop(Part):
    base = Cube(33, 1.6, 10.5).color("red")
    switch = (
        OptoSwitch()
        .align(right=base.right - 0.1, back=base.front, center_z=base.center_z)
        .color("grey")
    )
    connector = (
        Cube(5.8, 7, 10.5)
        .align(left=base.left - 0.2, front=base.back, center_z=base.center_z)
        .color("white")
        .misc()
    )
    led = (
        Cube(2, 0.7, 1.5)
        .align(center_x=4.5, back=base.front, center_z=base.center_z)
        .color("blue")
    )
    left_hole = (
        ~Cylinder(d=3, h=4.5)
        .bottom_to_front()
        .align(
            center_x=switch.left + 2.75,
            center_y=base.center_y,
            center_z=base.center_z,
        )
    )
    right_hole = (
        ~Cylinder(d=3, h=4.5)
        .bottom_to_front()
        .align(
            center_x=switch.right - 2.75,
            center_y=base.center_y,
            center_z=base.center_z,
        )
    )

    def add_bolts(self, bolt):
        self.left_bolt = (
            bolt.bottom_to_front()
            .align(
                center_x=self.left_hole.center_x,
                front=self.switch.base.front,
                center_z=self.left_hole.center_z,
            )
            .misc()
        )
        self.right_bolt = (
            bolt.bottom_to_front()
            .align(
                center_x=self.right_hole.center_x,
                front=self.switch.base.front,
                center_z=self.right_hole.center_z,
            )
            .misc()
        )
        return self


class BIQUEndstop(Part):
    body = Surface.free(
        Circle(d=7).align(center_x=-10), Circle(d=7).align(center_x=10)
    ).z_linear_extrude(bottom=0, top=1)
    endstop = Cube(13, 6, 4).align(
        center_x=body.center_x, back=body.front, bottom=body.top
    )


class MechanicalSwitchEndstop(Part):
    def init(self, cable_len=10):
        self.enstop = Cube(13, 6.5, 6)
        self.cables = (
            Cube(13, cable_len, 6)
            .align(
                center_x=self.enstop.center_x,
                front=self.enstop.back,
                center_z=self.enstop.center_z,
            )
            .misc()
        )

    def add_bolts(self, bolt=Bolt.M2(10), left=True, right=True):
        if left:
            self.left_bolt = bolt.align(
                center_x=self.enstop.center_x - 6.5 / 2,
                center_y=self.enstop.back + 1.5,
                center_z=self.enstop.center_z,
            ).misc()
        if right:
            self.right_bolt = bolt.align(
                center_x=self.enstop.center_x + 6.5 / 2,
                center_y=self.enstop.back + 1.5,
                center_z=self.enstop.center_z,
            ).misc()
        return self


class InductionSensor(Part):
    def init(self, diameter, lenght):
        self.sensor = Cylinder(d=diameter, h=lenght)

    @classmethod
    def LJ12A3(cls):
        return cls(12, 60)


if __name__ == "__main__":
    OpticalEndstop().render_to_file(openscad=False)
