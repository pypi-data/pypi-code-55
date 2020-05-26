from muscad import Cube, E, EE, Part, Volume
from muscad.vitamins.bearings import RotationBearing
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.extrusions import Extrusion
from muscad.vitamins.steppers import StepperMotor


class ZStepperMount(Part):
    def __stl__(self):
        return self.upside_down()

    extrusion = (
        ~Extrusion.e3030(100)
        .x_rotate(90)
        .align(left=0, center_y=0, top=0)
        .debug()
    )
    stepper = ~StepperMotor.nema17(bolt=Bolt.M3(8).upside_down()).align(
        center_x=extrusion.left - 22, center_y=0, top=extrusion.top
    )

    bearing = ~RotationBearing.b605zz().align(
        center_x=stepper.center_x,
        center_y=stepper.center_y,
        bottom=stepper.top + 2,
    )
    stepper_box = Volume(
        left=stepper.left - 3,
        right=extrusion.left,
        back=stepper.back - 8,
        front=stepper.front + 8,
        bottom=extrusion.bottom + 4,
        top=bearing.top - E,
    ).fillet_height(r=5, left=True, front=True, back=True)

    stepper_clearance = ~Volume(
        left=stepper_box.left - 1,
        right=stepper_box.right + 1,
        back=stepper_box.back + 4,
        front=stepper_box.front - 4,
        bottom=stepper_box.bottom - 10,
        top=stepper_box.top - 8,
    ).fillet_width(r=4, top=True, front=True, back=True)

    side_bolt_front = (
        ~Bolt.M6(10)
        .slide(y=20)
        .y_rotate(90)
        .align(
            center_x=extrusion.left - 2,
            center_y=stepper.front + 15,
            center_z=extrusion.center_z,
        )
    )

    side_bolt_back = (
        ~Bolt.M6(10)
        .slide(y=-20)
        .y_rotate(90)
        .align(
            center_x=extrusion.left - 2,
            center_y=stepper.back - 15,
            center_z=extrusion.center_z,
        )
    )

    top_bolt_front = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=extrusion.center_x,
            center_y=side_bolt_front.center_y - 3,
            center_z=extrusion.top + 2,
        )
    )
    top_bolt_center = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=extrusion.center_x,
            center_y=stepper.center_y,
            center_z=extrusion.top + 2,
        )
    )
    top_bolt_back = (
        ~Bolt.M6(10)
        .upside_down()
        .align(
            center_x=extrusion.center_x,
            center_y=side_bolt_back.center_y + 3,
            center_z=extrusion.top + 2,
        )
    )

    body = (
        Volume(
            left=extrusion.left - 6,
            right=extrusion.right - 4,
            back=top_bolt_back.back - 2,
            front=top_bolt_front.front + 2,
            bottom=extrusion.bottom + 4,
            top=extrusion.top + 7,
        )
        .fillet_width(r=5, bottom=True, front=True, back=True)
        .fillet_depth(r=5, top=True, left=True)
        .fillet_height(r=5, right=True, front=True, back=True)
    )

    tilted_clearance = (
        ~Cube(
            stepper_clearance.width, stepper_box.depth + EE, stepper_box.height
        )
        .align(
            right=10,
            center_y=extrusion.center_y,
            top=stepper_clearance.top - 25,
        )
        .y_rotate(35)
    )


if __name__ == "__main__":
    ZStepperMount().render_to_file(openscad=False)
