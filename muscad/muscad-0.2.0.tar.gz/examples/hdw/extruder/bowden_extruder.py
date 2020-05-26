from muscad import Cylinder, E, distance_between, T, TT, Volume, Part
from muscad.vitamins.bearings import RotationBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.steppers import StepperMotor


class ExtruderStepperHolder(Part):
    y_extrusion = ~Extrusion.e3030(100).bottom_to_front().debug()
    stepper = (
        ~StepperMotor.nema17(
            gearbox_height=24,
            shaft_diameter=9,
            bolt=Bolt.M3(10, head_clearance=4)
            .add_nut(-1, side_clearance_size=20)
            .upside_down(),
        )
        .add_bolts(
            Bolt.M3(12).upside_down(), holes=(0, 3), depth=-22, spacing=34
        )
        .bottom_to_front()
        .align(right=y_extrusion.left - 1, bottom=y_extrusion.bottom - 4)
        # .debug()
    )

    stepper_holder = (
        Volume(
            right=y_extrusion.left,
            left=stepper.left,
            front=stepper.body.back - T,
            back=stepper.back - 9,
            bottom=stepper.bottom,
            top=stepper.top,
        )
        .fillet_depth(4, bottom=True)
        .fillet_depth(4, top=True, left=True)
    )

    attachment = (
        Volume(
            left=stepper_holder.right - E,
            right=y_extrusion.right - 2,
            back=stepper_holder.back,
            center_y=stepper_holder.front,
            bottom=y_extrusion.top + T,
            top=stepper_holder.top,
        )
        .fillet_height(4, right=True)
        .fillet_height(4, front=True, left=True)
    )

    bolt_top_back = (
        ~Bolt.M6(12)
        .upside_down()
        .align(
            center_x=y_extrusion.center_x,
            center_y=stepper_holder.center_y,
            center_z=y_extrusion.top,
        )
    )
    bolt_top_front = ~bolt_top_back.y_mirror(stepper_holder.front)

    extruder_holder = Volume(
        left=stepper_holder.left - 10,
        right=stepper_holder.center_x,
        back=stepper_holder.back,
        depth=10,
        bottom=stepper_holder.bottom,
        top=stepper_holder.top,
    ).fillet_depth(4, left=True)

    bracket_bolt = (
        ~Bolt.M4(20, head_clearance=20)
        .add_nut(-E, angle=90)
        .bottom_to_back()
        .align(
            center_x=extruder_holder.left + 6,
            front=extruder_holder.front + E,
            center_z=extruder_holder.top - 6,
        )
    )

    plate_bolt = (
        ~Bolt.M3(12)
        .add_nut(-E, angle=90)
        .bottom_to_back()
        .align(
            center_x=extruder_holder.left + 6,
            front=extruder_holder.front + E,
            center_z=extruder_holder.bottom + 6,
        )
    )


class BowdenExtruder(Part):
    _stepper_holder = ~ExtruderStepperHolder()

    stepper = _stepper_holder.stepper
    bracket_bolt = _stepper_holder.bracket_bolt
    plate_bolt = _stepper_holder.plate_bolt

    drive_gear = (
        Cylinder(d=12.6, h=11)
        .bottom_to_front()
        .align(
            center_x=stepper.center_x,
            front=_stepper_holder.back - 4,
            center_z=stepper.center_z,
        )
        .debug()
    )
    FILAMENT_Y_OFFSET = (drive_gear.width + 1.75) / 2 - 0.5

    plate = Volume(
        left=stepper.left - 10,
        right=stepper.right,
        depth=5,
        front=_stepper_holder.back,
        bottom=stepper.bottom,
        top=stepper.top,
    ).fillet_depth(4)

    central_hole = (
        ~Cylinder(d=16, h=20)
        .bottom_to_front()
        .align(
            center_x=stepper.center_x,
            center_z=stepper.center_z,
            front=_stepper_holder.back - E,
        )
    )

    filament = (
        ~Cylinder(h=plate.height + 2, d=4)
        .align(
            center_x=stepper.center_x - FILAMENT_Y_OFFSET,
            center_y=plate.back - 7.5,
            center_z=stepper.center_z,
        )
        .debug()
    )
    bearing = (
        ~RotationBearing.b608zz()
        .bottom_to_back()
        .align(
            right=drive_gear.left - 1,
            back=drive_gear.back,
            center_z=filament.center_z,
        )
        .debug()
    )
    bearing_fix = (
        Cylinder(
            d=bearing.inner.width - T,
            h=distance_between(plate.back, bearing.back + T),
        )
        .bottom_to_back()
        .align(
            center_x=bearing.center_x,
            front=plate.back,
            center_z=bearing.center_z,
        )
    )
    bearing_bolt = (
        ~Bolt.M5(16)
        .bottom_to_back()
        .align(
            center_x=bearing.center_x,
            back=bearing.back - 5,
            center_z=bearing.center_z,
        )
        .debug()
    )

    bearing_clearance = ~(
        Cylinder(d=bearing.width + 3.5, h=bearing.height + 3)
        .bottom_to_back()
        .align(
            center_x=bearing.center_x,
            front=bearing.front - T,
            center_z=bearing.center_z,
        )
        - bearing_fix
    )

    pneumatic = ~Cylinder(d=5.7, h=5).align(
        center_x=filament.center_x,
        center_y=filament.center_y,
        top=plate.top + E,
    )

    filament_tunnel = Volume(
        left=pneumatic.left - 2,
        width=12,
        front=plate.back,
        back=pneumatic.back - 2,
        top=plate.top,
        bottom=plate.bottom,
    ).fillet_height(back=True)

    central_clearance = ~Volume(
        left=filament_tunnel.left - E,
        right=filament_tunnel.right + E,
        back=filament_tunnel.back - E,
        front=plate.back,
        bottom=central_hole.bottom,
        top=central_hole.top,
    )

    tightener = Volume(
        right=filament_tunnel.center_x,
        width=12,
        front=plate.back,
        back=filament_tunnel.back,
        bottom=plate.bottom,
        top=central_clearance.bottom,
    )

    bracket_tightening_bolt = (
        ~Bolt.M3(16)
        .add_nut(-2, side_clearance_size=8, angle=180)
        .bottom_to_left()
        .slide(z=2)
        .align(
            right=filament.left - 2,
            center_y=tightener.center_y,
            center_z=tightener.bottom + 3.5,
        )
    )


class ExtruderBracket(Part):
    _bowden_extruder = BowdenExtruder()

    bearing_clearance = _bowden_extruder.bearing_clearance
    bracket_bolt = _bowden_extruder.bracket_bolt
    tightening_bolt = _bowden_extruder.bracket_tightening_bolt
    bearing_bolt = _bowden_extruder.bearing_bolt

    body = Volume(
        left=_bowden_extruder.left,
        right=_bowden_extruder.filament_tunnel.left - 3,
        front=_bowden_extruder.plate.back - TT,
        depth=12,
        bottom=_bowden_extruder.bottom,
        top=_bowden_extruder.top,
    ).fillet_depth(4, left=True)

    tightener_clearance = ~Volume(
        right=body.right + E,
        left=_bowden_extruder.tightener.left - 4,
        front=body.front + E,
        back=body.back - E,
        bottom=body.bottom - T,
        top=bearing_clearance.bottom + 3,
    ).fillet_depth(2, left=True, top=True)


if __name__ == "__main__":
    ExtruderStepperHolder().render_to_file(openscad=False)
    BowdenExtruder().render_to_file(openscad=False)
    ExtruderBracket().render_to_file()

    (
        ExtruderStepperHolder().color("green")
        + BowdenExtruder().color("blue")
        + ExtruderBracket()
    ).render_to_file("bowden_extruder_assembled", openscad=False)
