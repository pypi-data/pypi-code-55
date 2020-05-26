from muscad import Volume, E, MirroredPart


class SDCardUSBKeyHolder(MirroredPart, x=True):
    _sd_hole = Volume(width=24.8, depth=2.8, height=13)
    _usb_hole = Volume(width=13, depth=4.2, height=13)
    _usb_c_hole = Volume(width=9, depth=3, height=7).fillet_height(1)
    _half_usb_hole = Volume(width=13, depth=3, height=13)
    _micro_sd_hole = Volume(width=13, depth=1, height=9)

    def init(
        self,
        nb_sd_rows,
        nb_usb_rows,
        nb_usb_c_rows,
        nb_halfusb_rows=0,
        micro_sd=True,
        sd_spacing=3,
        usb_spacing=6.5,
        usb_c_spacing=5,
        half_usb_spacing=5,
        micro_sd_spacing=8,
        margin=3,
    ):
        for i in range(nb_sd_rows):
            sd_holes_front = i * (self._sd_hole.depth + sd_spacing)
            self.add_child(
                self._sd_hole.align(left=6, front=sd_holes_front, top=0,)
            )

        for i in range(nb_usb_rows):
            usb_holes_front = self.front + (self._usb_hole.depth + usb_spacing)
            self.add_child(
                self._usb_hole.align(
                    left=usb_spacing, front=usb_holes_front, top=0,
                )
            )

        for i in range(nb_usb_c_rows):
            usb_c_holes_front = self.front + (
                self._usb_c_hole.depth + usb_c_spacing
            )
            self.add_child(
                self._usb_c_hole.align(
                    left=(self._usb_hole.width - self._usb_c_hole.width) / 2
                    + usb_spacing,
                    front=usb_c_holes_front,
                    top=0,
                )
            )

        for i in range(nb_halfusb_rows):
            half_usb_holes_front = self.front + (
                self._half_usb_hole.depth + half_usb_spacing
            )
            self.add_child(
                self._half_usb_hole.align(
                    left=usb_spacing, front=half_usb_holes_front, top=0
                )
            )

        if micro_sd:
            for micro_sd_front in range(
                int(sd_holes_front + margin + micro_sd_spacing),
                int(self.front),
                micro_sd_spacing,
            ):
                self.add_child(
                    self._micro_sd_hole.align(
                        left=usb_spacing + self._usb_hole.width + usb_spacing,
                        front=micro_sd_front,
                        bottom=self.bottom + 1,
                    )
                )

        self.add_hole(
            Volume(
                left=0,
                right=self.right + margin,
                center_y=self.center_y,
                depth=self.depth + 2 * margin,
                height=self.height + margin,
                top=self.top - E,
            )
            .fillet_height(1, right=True)
            .fillet_depth(2, right=True, top=True)
        )
        self.revert()

        self.add_hole(
            Volume(
                back=sd_holes_front + margin,
                front=self.front + E,
                left=usb_spacing + self._usb_hole.width + usb_spacing / 2,
                right=self.right + E,
                height=self._micro_sd_hole.height - 3,
                top=self.top + E,
            ).chamfer_depth(6, left=True, bottom=True)
        )


if __name__ == "__main__":
    holder = SDCardUSBKeyHolder(
        nb_sd_rows=4, nb_usb_rows=5, nb_usb_c_rows=2, nb_halfusb_rows=1
    )
    holder.render_to_file("sd_usb_holder", openscad=False)
