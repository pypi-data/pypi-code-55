from examples.hdw import config
from muscad import E, Part, T, Hull, Cylinder, middle_of, Volume
from muscad.vitamins.bearings import BushingLinearBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.endstops import InductionSensor
from muscad.vitamins.extruders import E3Dv6Extruder
from muscad.vitamins.fans import Blower, Fan
from muscad.vitamins.pulleys import Pulley
from muscad.vitamins.rods import Rod


class XCarriage(Part):
    x_top_rod = (
        ~Rod.d8(100)
        .bottom_to_right()
        .align(center_x=0, center_y=0, center_z=config.X_RODS_DISTANCE / 2)
    )
    x_bottom_rod = ~x_top_rod.z_mirror()

    x_bearing_top_right = (
        ~BushingLinearBearing.SC8UU(T=0.15)
        .add_rod_clearance(100, slide={"y": 10}, T=1)
        .front_to_left()
        .bottom_to_front()
        .align(
            left=x_top_rod.center_x + 0.5,
            center_y=x_top_rod.center_y,
            center_z=x_top_rod.center_z,
        )
    )
    x_bearing_bottom = (
        ~BushingLinearBearing.SC8UU(T=0.15)
        .add_rod_clearance(100)
        .front_to_left()
        .bottom_to_front()
        .align(
            center_x=0,
            center_y=x_bottom_rod.center_y,
            center_z=x_bottom_rod.center_z,
        )
    )
    x_bearing_top_left = ~x_bearing_top_right.x_mirror()

    body = Volume(
        left=x_bearing_top_left.left + E,
        right=x_bearing_top_right.right - E,
        back=x_bearing_bottom.front + E,
        depth=8,
        bottom=x_bearing_bottom.bottom + E,
        top=x_bearing_top_left.top - E,
    ).fillet_depth()

    center_pulleys_bolt = (
        ~Bolt.M3(16)
        .add_nut(-E, inline_clearance_size=10)
        .bottom_to_back()
        .align(center_x=0, front=body.front - 1, center_z=0)
    )

    extruder = (
        ~E3Dv6Extruder()
        .align(center_x=0, center_y=body.front + 30, top=10)
        .debug()
    )
    extruder_holder = Volume(
        center_x=body.center_x,
        width=40,
        back=body.front,
        front=extruder.center_y - 3,
        center_z=body.center_z,
        height=11,
    ).fillet_depth()

    blower = (
        ~Blower.blower50x50x15()
        .front_to_back()
        .bottom_to_front()
        .align(
            right=body.center_x + 9,
            back=body.front + T,
            bottom=extruder_holder.top,
        )
        .debug()
    )

    left_blower_holder = Volume(
        left=blower.front_bolt.left - 1,
        right=body.left + 2,
        depth=4,
        front=body.front,
        bottom=blower.front_bolt.bottom - 1,
        top=blower.front_bolt.top + 1,
    ).fillet_depth(r=6, left=True)

    cable_holder = Volume(
        left=blower.back_bolt.left - 2,
        right=blower.back_bolt.right + 12,
        back=x_bearing_bottom.front,
        front=body.front,
        bottom=body.top - E,
        height=50,
    ).fillet_depth(r=6, top=True)

    cable_hole_bottom_left = (
        ~Volume(
            right=body.right + E,
            width=10,
            bottom=body.bottom + 3,
            height=10,
            back=body.back - 1,
            front=body.front + 1,
        )
        .fillet_depth(left=True)
        .chamfer_depth(right=True)
    )
    cable_hole_bottom_right = ~cable_hole_bottom_left.x_mirror()

    fan = (
        ~Fan.fan40x40x20(bolts=False)
        .add_bolts(bolt=Bolt.M3(25).add_nut(-E), spacing=32, holes=(2, 3))
        .add_bolts(bolt=Bolt.M3(40), spacing=32, holes=(0, 1))
        .bottom_to_front()
        .align(
            center_x=extruder_holder.center_x,
            back=extruder_holder.front + 13,
            top=extruder_holder.top,
        )
    )

    extruder_clamp_bolt_right = (
        ~Bolt.M3(12)
        .add_nut(-E, side_clearance_size=20, angle=90)
        .bottom_to_front()
        .align(
            center_x=extruder.center_x - 16,
            center_y=extruder_holder.front,
            center_z=extruder_holder.center_z + 1.3,
        )
    )
    extruder_clamp_bolt_left = ~extruder_clamp_bolt_right.x_mirror()

    def __stl__(self):
        return self.back_to_bottom()


class XAxisPulleys(Part):
    _carriage = XCarriage().disable()

    center_pulleys_bolt = _carriage.center_pulleys_bolt
    top_bearing = _carriage.x_bearing_top_left
    bottom_bearing = _carriage.x_bearing_bottom

    left_pulley = (
        ~Pulley.placeholder(15, 10.3)
        .add_clearance(20, angle=90)
        .align(
            right=bottom_bearing.left - 0.5,
            center_y=bottom_bearing.center_y,
            top=-1,
        )
    )

    right_pulley = ~left_pulley.x_mirror()

    left_pulley_shaft = (
        ~Bolt.M3(20)
        .add_nut(-1, angle=90)
        .upside_down()
        .align(
            center_x=left_pulley.center_x,
            center_y=left_pulley.center_y,
            top=top_bearing.bottom - T,
        )
    )
    right_pulley_shaft = ~left_pulley_shaft.x_mirror()

    body = Volume(
        left=_carriage.body.left,
        right=_carriage.body.right,
        front=_carriage.body.back - T,
        back=left_pulley.back - 2,
        bottom=left_pulley_shaft.bottom + 2,
        top=left_pulley_shaft.top,
    ).fillet_width(back=True, bottom=True)

    def __stl__(self):
        return self.bottom_to_back()


class ExtruderClamp(Part):

    _carriage = XCarriage()
    _extruder_holder = _carriage.extruder_holder

    extruder = _carriage.extruder

    left_bolt = _carriage.extruder_clamp_bolt_left
    right_bolt = _carriage.extruder_clamp_bolt_right

    fan = _carriage.fan
    clamp = (
        Volume(
            left=_extruder_holder.left,
            right=_extruder_holder.right,
            back=_extruder_holder.front + 0.5,
            front=fan.back - T,
            bottom=_extruder_holder.bottom,
            top=_extruder_holder.top,
        )
        .fillet_depth(bottom=True)
        .fillet_depth(top=True, left=True)
    )

    fan_holder = Hull(
        Cylinder(d=4, h=34).align(
            right=clamp.right - 5, back=clamp.back, top=clamp.center_z
        ),
        Cylinder(d=4, h=34).align(
            left=clamp.left + 5, back=clamp.back, top=clamp.center_z
        ),
        Volume(
            left=clamp.left,
            right=clamp.right,
            front=clamp.front,
            depth=1,
            top=clamp.center_z,
            height=35,
        ),
    )

    tunnel = ~Hull(
        Volume(
            center_x=clamp.center_x,
            width=32,
            back=clamp.front,
            front=clamp.front + 1,
            top=clamp.bottom + 2,
            bottom=clamp.bottom - 32,
        ).fillet_depth(8, top=True),
        Volume(
            left=clamp.left + 8,
            right=clamp.right - 8,
            back=clamp.back - 1,
            front=clamp.back,
            top=clamp.bottom,
            bottom=clamp.bottom - 32,
        ).fillet_depth(8, top=True),
    )

    sensor_holder_up = (
        Volume(
            left=clamp.right - E,
            width=18,
            depth=18,
            front=clamp.front,
            top=clamp.top,
            height=9,
        )
        .fillet_height(6, right=True)
        .fillet_height(6, back=True, left=True)
    )

    sensor_holder_down = sensor_holder_up.z_mirror(
        middle_of(sensor_holder_up.top, fan_holder.bottom)
    )

    sensor_holder_down_holder = Volume(
        right=sensor_holder_down.left + E,
        center_x=clamp.center_x,
        front=sensor_holder_down.front,
        back=clamp.back,
        bottom=sensor_holder_down.bottom,
        top=sensor_holder_down.top,
    ).fillet_height(back=True)
    sensor = (
        ~InductionSensor.LJ12A3()
        .align(
            center_x=sensor_holder_up.center_x,
            center_y=sensor_holder_up.center_y,
            bottom=extruder.bottom + 4,
        )
        .debug()
    )

    def __stl__(self):
        return self.front_to_bottom()


class Tunnel(Part):
    _carriage = ~XCarriage()
    _center_x = _carriage.extruder_holder.center_x
    tunnel = Volume(
        left=_carriage.blower.blower.left + T,
        right=_carriage.blower.blower.right - T,
        back=_carriage.body.front + T,
        front=_carriage.blower.blower.front - T,
        top=_carriage.extruder_holder.center_z,
        bottom=_carriage.bottom,
    ) - Volume(
        left=_carriage.blower.blower.left + 1,
        right=_carriage.blower.blower.right - 1,
        back=_carriage.body.front + 1,
        front=_carriage.blower.blower.front - 1,
        top=_carriage.extruder_holder.center_z + E,
        bottom=_carriage.bottom - E,
    )

    blower = Hull(
        Volume(
            center_x=_center_x,
            width=30,
            front=_carriage.extruder.center_y - 7,
            depth=5,
            bottom=_carriage.extruder.bottom + 1,
            height=E,
        ),
        Volume(
            left=tunnel.left,
            right=tunnel.right,
            back=tunnel.back,
            front=tunnel.front,
            top=tunnel.bottom,
            height=E,
        ),
    ) - Hull(
        Volume(
            center_x=_center_x,
            width=28,
            front=_carriage.extruder.center_y - 7,
            depth=3,
            bottom=_carriage.extruder.bottom,
            height=E,
        ),
        Volume(
            left=tunnel.left + 1,
            right=tunnel.right - 1,
            back=tunnel.back + 1,
            front=tunnel.front - 1,
            top=tunnel.bottom + E,
            height=E,
        ),
    )

    bolt_left = (
        ~Bolt.M3(10)
        .bottom_to_front()
        .align(
            center_x=tunnel.left - 4,
            center_y=_carriage.body.front,
            center_z=_carriage.bottom + 20,
        )
    )
    bolt_holder_left = (
        Volume(
            center_x=bolt_left.center_x,
            right=tunnel.left + E,
            back=_carriage.body.front + T,
            depth=3,
            center_z=bolt_left.center_z + 2,
            height=15,
        )
        .chamfer_depth(8, top=True, left=True)
        .fillet_depth(bottom=True, left=True)
    )

    bolt_right = ~bolt_left.x_mirror(center=tunnel.center_x)
    bolt_holder_right = bolt_holder_left.x_mirror(center=tunnel.center_x)


if __name__ == "__main__":
    XCarriage().render_to_file(openscad=False)
    XAxisPulleys().render_to_file(openscad=False)

    (XCarriage() + XAxisPulleys() + ExtruderClamp() + Tunnel()).render_to_file(
        "extruder_assembled", openscad=False
    )

    ExtruderClamp().render_to_file(openscad=False)

    Tunnel().render_to_file(openscad=False)
