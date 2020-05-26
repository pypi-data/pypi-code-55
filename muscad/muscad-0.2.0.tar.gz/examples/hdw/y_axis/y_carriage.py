from examples.hdw import config
from muscad import Cube, E, EE, Part, TT, Hull, Volume, Fillet
from muscad.vitamins.bearings import LinearBearing
from muscad.vitamins.belts import Belt
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod


class YCarriage(Part):
    y_bearing = (
        ~LinearBearing.LM12UU(hollow=False)
        .add_rod_clearance()
        .bottom_to_front()
        .align(center_x=0, center_y=0, center_z=0)
        .debug()
    )

    x_rod_top = (
        ~Rod.d8(50)
        .bottom_to_right()
        .align(
            left=y_bearing.center_x - E,
            center_y=y_bearing.center_y,
            center_z=y_bearing.center_z + config.X_RODS_DISTANCE / 2,
        )
        .debug()
    )

    x_rod_bottom = ~x_rod_top.z_mirror(0)

    front_x_pulley = (
        ~Pulley.placeholder(18, 10.3)
        .add_bolt(
            Bolt.M3(25).add_nut(-2, side_clearance_size=20, angle=0),
            center_z=3,
        )
        .add_clearance(20, 270)
        .add_clearance(20, 0)
        .align(
            center_x=y_bearing.center_x
            + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER
            + 10,
            center_y=y_bearing.center_y + 10,
            top=y_bearing.center_z + config.X_PULLEYS_Z_OFFSET,
        )
    )

    back_x_pulley = ~front_x_pulley.y_mirror(y_bearing.center_y)

    pulleys_holder = Volume(
        left=y_bearing.center_x,
        right=front_x_pulley.right - E,
        back=back_x_pulley.back + E,
        front=front_x_pulley.front - E,
        top=x_rod_top.bottom - 1,
        bottom=x_rod_bottom.top + 1,
    ).fillet_width()

    body = Volume(
        left=y_bearing.center_x,
        right=front_x_pulley.left - 1,
        back=back_x_pulley.back + E,
        front=front_x_pulley.front - E,
        top=x_rod_top.top + 5,
        bottom=x_rod_bottom.bottom - 5,
    ).fillet_width(r=10, front=True)

    y_clamp_bolt_top_front = (
        ~Bolt.M3(16)
        .add_nut(placement=-E, side_clearance_size=30, angle=90)
        .y_rotate(90)
        .align(
            right=10, center_y=body.front - 4.5, center_z=y_bearing.top + 2.4
        )
    )

    y_clamp_bolt_top_back = ~y_clamp_bolt_top_front.y_mirror(
        y_bearing.center_y
    )
    y_clamp_bolt_bottom_front = ~y_clamp_bolt_top_front.z_mirror(
        y_bearing.center_z
    )
    y_clamp_bolt_bottom_back = ~y_clamp_bolt_top_back.z_mirror(
        y_bearing.center_z
    )

    clamp_clearance_bottom = ~Cube(body.width + EE, body.depth, 1.5).align(
        left=body.left - E, front=body.center_y, bottom=x_rod_bottom.bottom
    )

    clamp_clearance_up = ~clamp_clearance_bottom.z_mirror(y_bearing.center_z)

    clamp_bolt_up = (
        ~Bolt.M3(12)
        .add_nut(-E, side_clearance_size=30, angle=90)
        .upside_down()
        .align(center_x=body.center_x, center_y=body.back + 9, top=body.top)
    )

    clamp_bolt_down = ~clamp_bolt_up.z_mirror(y_bearing.center_z)

    y_belt_outer_clearance = ~Volume(
        center_x=y_bearing.center_x
        + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER
        - 5,
        width=8,
        back=body.back - 1,
        front=body.front + 1,
        height=12,
        bottom=y_bearing.center_z + config.Y_PULLEYS_Z_OFFSET,
    )

    y_belt_inner_clearance = ~Volume(
        center_x=y_bearing.center_x
        + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER
        + 5,
        width=8,
        back=body.back - 1,
        front=body.front + 1,
        height=12,
        bottom=y_bearing.center_z + config.Y_PULLEYS_Z_OFFSET,
    )

    def __stl__(self):
        return self.back_to_bottom()


class YCarriageLeft(YCarriage):

    belt_fix_clearance_front = (
        ~Volume(
            left=YCarriage.y_belt_inner_clearance.left,
            width=20,
            back=YCarriage.body.front - 16,
            front=YCarriage.body.front + E,
            bottom=YCarriage.y_belt_inner_clearance.bottom,
            top=YCarriage.y_belt_inner_clearance.top,
        )
        .fillet_depth(1, right=True)
        .fillet_width(1, back=True)
    )


class YCarriageRight(YCarriage):

    fan_fix_clearance = ~Volume(
        left=YCarriage.body.right,
        right=YCarriage.pulleys_holder.right + 1,
        back=YCarriage.pulleys_holder.front - 4.5,
        front=YCarriage.pulleys_holder.front + 1,
        bottom=YCarriage.y_belt_inner_clearance.bottom,
        top=YCarriage.pulleys_holder.top + E,
    )
    fan_fix_fillet = (
        ~Fillet(YCarriage.pulleys_holder.width)
        .bottom_to_right()
        .align(
            left=YCarriage.body.right,
            front=fan_fix_clearance.back + E,
            top=YCarriage.pulleys_holder.top + E,
        )
    )
    belt_fix_clearance_front = ~Volume(
        left=YCarriage.y_belt_outer_clearance.left - 12,
        right=YCarriage.y_belt_outer_clearance.right,
        back=YCarriage.body.front - 10,
        front=YCarriage.body.front + E,
        bottom=YCarriage.y_belt_outer_clearance.bottom,
        top=YCarriage.y_belt_outer_clearance.top,
    ).fillet_depth(1, left=True)
    belt_fix_clearance_back = ~Volume(
        left=YCarriage.y_belt_outer_clearance.left - 12,
        right=YCarriage.y_belt_outer_clearance.right,
        back=YCarriage.body.back + 10,
        front=YCarriage.body.back - E,
        bottom=YCarriage.y_belt_outer_clearance.bottom,
        top=YCarriage.y_belt_outer_clearance.top,
    ).fillet_depth(1, left=True)
    y_fix_bolt = (
        ~Bolt.M3(25)
        .add_nut(-E, inline_clearance_size=20)
        .bottom_to_front()
        .align(
            center_x=YCarriage.y_belt_outer_clearance.center_x - 9,
            center_y=YCarriage.body.center_y,
            center_z=YCarriage.y_belt_outer_clearance.center_z,
        )
    )

    x_belt_clearance = ~Volume(
        center_x=YCarriage.y_bearing.center_x
        + config.Y_ROD_CENTER_TO_STEPPER_SHAFT_CENTER
        - 5,
        width=8,
        back=YCarriage.body.back - 1,
        front=YCarriage.body.front + 1,
        height=12,
        top=YCarriage.front_x_pulley.top,
    )


class YBeltFixFront(Part):
    _carriage = YCarriageRight()
    belt = (
        ~Belt.GT2(60, 10, scale=1.1)
        .front_to_right()
        .align(
            center_x=_carriage.y_belt_outer_clearance.center_x,
            back=_carriage.back - 10,
            center_z=_carriage.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    body = Volume(
        left=_carriage.y_belt_outer_clearance.left + TT,
        right=_carriage.y_belt_outer_clearance.right - TT,
        back=_carriage.center_y + 2,
        front=_carriage.front,
        bottom=_carriage.y_belt_outer_clearance.bottom + TT,
        top=_carriage.y_belt_outer_clearance.top - TT,
    )

    bolt = _carriage.y_fix_bolt

    bolt_holder = Hull(
        Volume(
            depth=10 - TT,
            front=body.front,
            left=body.left - 12 + TT,
            right=body.right,
            bottom=body.bottom,
            top=body.top,
        ).fillet_depth(1, left=True)
    )

    def __stl__(self):
        return self.upside_down()


class YBeltFixBack(Part):
    _carriage = YCarriageRight()
    belt = (
        ~Belt.GT2(60, 10, scale=1.1)
        .front_to_right()
        .align(
            center_x=_carriage.y_belt_outer_clearance.center_x,
            back=_carriage.back - 10,
            center_z=_carriage.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    body = Volume(
        left=_carriage.y_belt_outer_clearance.left + TT,
        right=_carriage.y_belt_outer_clearance.right - TT,
        front=_carriage.center_y - 2,
        back=_carriage.back,
        bottom=_carriage.y_belt_outer_clearance.bottom + TT,
        top=_carriage.y_belt_outer_clearance.top - TT,
    )

    bolt = _carriage.y_fix_bolt

    bolt_holder = Hull(
        Volume(
            depth=10 - TT,
            back=body.back,
            left=body.left - 12 + TT,
            right=body.right,
            bottom=body.bottom,
            top=body.top,
        ).fillet_depth(1, left=True)
    )

    def __stl__(self):
        return self.upside_down()


class YBeltFixLeft(Part):

    _carriage = YCarriageLeft()
    belt = (
        ~Belt.GT2(60, 10, scale=1.1)
        .front_to_left()
        .align(
            center_x=_carriage.y_belt_inner_clearance.center_x,
            back=_carriage.back - 10,
            center_z=_carriage.y_belt_outer_clearance.center_z - 1.5,
        )
        .debug()
    )

    bolt = ~_carriage.front_x_pulley.debug()

    body = Volume(
        left=_carriage.y_belt_inner_clearance.left + TT,
        right=_carriage.y_belt_inner_clearance.right - TT,
        front=_carriage.front,
        back=_carriage.center_y + 2,
        bottom=_carriage.y_belt_outer_clearance.bottom + TT,
        top=_carriage.y_belt_outer_clearance.top - TT,
    )

    bolt_holder = Hull(
        Volume(
            depth=16 - TT,
            front=body.front,
            left=body.left,
            right=_carriage.right,
            bottom=body.bottom,
            top=body.top,
        )
        .fillet_depth(1, left=True)
        .fillet_width(1, back=True)
    )

    def __stl__(self):
        return self.upside_down()


class YClamp(Part):
    _carriage = ~YCarriage()

    y_bearing = _carriage.y_bearing
    bolts = (
        _carriage.y_clamp_bolt_bottom_front
        + _carriage.y_clamp_bolt_bottom_back
        + _carriage.y_clamp_bolt_top_front
        + _carriage.y_clamp_bolt_top_back
    )

    body = Volume(
        left=_carriage.y_bearing.left - 5,
        right=_carriage.left,
        bottom=bolts.bottom - 1,
        top=bolts.top + 1,
        front=_carriage.front,
        back=_carriage.back,
    ).fillet_width()

    def __stl__(self):
        return self.left_to_bottom()


if __name__ == "__main__":
    YCarriageRight().render_to_file(openscad=False)
    YCarriageLeft().render_to_file(openscad=False)
    (
        YCarriageRight().background()
        + YBeltFixFront()
        + YBeltFixBack()
        + YClamp()
    ).render_to_file("y_carriage_assembled", openscad=False)
    # (
    #    YCarriage()
    #    .backward(100)
    #    .up(5)
    #    .rightward(15)
    # + XYStepperMount.right_side()
    # + XYIdler().backward(150).up(10)
    # + XCarriage().backward(100).rightward(100)
    # ).render_to_file(openscad=False)

    YBeltFixFront().render_to_file(openscad=False)
    YBeltFixBack().render_to_file(openscad=False)
    YClamp().render_to_file(openscad=False)

    # (YCarriage.left_side() + YBeltFixLeft()).render_to_file(openscad=False)

    YBeltFixLeft().render_to_file(openscad=False)
