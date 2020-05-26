from muscad import Volume, Square, Cube


def test_volume():
    LEFT = -12
    RIGHT = 10
    BACK = -22
    FRONT = 20
    BOTTOM = -33
    TOP = 30

    ref = Volume(
        left=LEFT, right=RIGHT, back=BACK, front=FRONT, bottom=BOTTOM, top=TOP
    )

    assert ref.left == LEFT
    assert ref.right == RIGHT
    assert ref.back == BACK
    assert ref.front == FRONT
    assert ref.bottom == BOTTOM
    assert ref.top == TOP

    front_to_top = ref.front_to_top()
    assert front_to_top.left == LEFT
    assert front_to_top.right == RIGHT
    assert front_to_top.back == -TOP
    assert front_to_top.front == -BOTTOM
    assert front_to_top.bottom == BACK
    assert front_to_top.top == FRONT

    bottom_to_left = ref.bottom_to_left()
    assert bottom_to_left.left == BOTTOM
    assert bottom_to_left.right == TOP
    assert bottom_to_left.back == BACK
    assert bottom_to_left.front == FRONT
    assert bottom_to_left.bottom == -RIGHT
    assert bottom_to_left.top == -LEFT

    front_to_right = ref.front_to_right()
    assert front_to_right.left == BACK
    assert front_to_right.right == FRONT
    assert front_to_right.back == -RIGHT
    assert front_to_right.front == -LEFT
    assert front_to_right.bottom == BOTTOM
    assert front_to_right.top == TOP

    upside_down = ref.upside_down()
    assert upside_down.left == LEFT
    assert upside_down.right == RIGHT
    assert upside_down.back == -FRONT
    assert upside_down.front == -BACK
    assert upside_down.bottom == -TOP
    assert upside_down.top == -BOTTOM

    upside_down_y = ref.upside_down(True)
    assert upside_down_y.left == -RIGHT
    assert upside_down_y.right == -LEFT
    assert upside_down_y.back == BACK
    assert upside_down_y.front == FRONT
    assert upside_down_y.bottom == -TOP
    assert upside_down_y.top == -BOTTOM

    front_to_back = ref.front_to_back()
    assert front_to_back.left == -RIGHT
    assert front_to_back.right == -LEFT
    assert front_to_back.back == -FRONT
    assert front_to_back.front == -BACK
    assert front_to_back.bottom == BOTTOM
    assert front_to_back.top == TOP

    front_to_bottom = ref.front_to_bottom()
    assert front_to_bottom.left == LEFT
    assert front_to_bottom.right == RIGHT
    assert front_to_bottom.back == BOTTOM
    assert front_to_bottom.front == TOP
    assert front_to_bottom.bottom == -FRONT
    assert front_to_bottom.top == -BACK

    bottom_to_right = ref.bottom_to_right()
    assert bottom_to_right.left == -TOP
    assert bottom_to_right.right == -BOTTOM
    assert bottom_to_right.back == BACK
    assert bottom_to_right.front == FRONT
    assert bottom_to_right.bottom == LEFT
    assert bottom_to_right.top == RIGHT

    front_to_right = ref.front_to_right()
    assert front_to_right.left == BACK
    assert front_to_right.right == FRONT
    assert front_to_right.back == -RIGHT
    assert front_to_right.front == -LEFT
    assert front_to_right.bottom == BOTTOM
    assert front_to_right.top == TOP

    back_to_right = ref.back_to_right()
    assert back_to_right.left == -FRONT
    assert back_to_right.right == -BACK
    assert back_to_right.back == LEFT
    assert back_to_right.front == RIGHT
    assert back_to_right.bottom == BOTTOM
    assert back_to_right.top == TOP

    back_to_bottom = ref.back_to_bottom()
    assert back_to_bottom.left == LEFT
    assert back_to_bottom.right == RIGHT
    assert back_to_bottom.back == -TOP
    assert back_to_bottom.front == -BOTTOM
    assert back_to_bottom.bottom == BACK
    assert back_to_bottom.top == FRONT

    left_to_bottom = ref.left_to_bottom()
    assert left_to_bottom.left == -TOP
    assert left_to_bottom.right == -BOTTOM
    assert left_to_bottom.back == BACK
    assert left_to_bottom.front == FRONT
    assert left_to_bottom.bottom == LEFT
    assert left_to_bottom.top == RIGHT

    left_to_top = ref.left_to_top()
    assert left_to_top.left == BOTTOM
    assert left_to_top.right == TOP
    assert left_to_top.back == BACK
    assert left_to_top.front == FRONT
    assert left_to_top.bottom == -RIGHT
    assert left_to_top.top == -LEFT

    left_to_front = ref.left_to_front()
    assert left_to_front.left == BACK
    assert left_to_front.right == FRONT
    assert left_to_front.back == -RIGHT
    assert left_to_front.front == -LEFT
    assert left_to_front.bottom == BOTTOM
    assert left_to_front.top == TOP

    left_to_back = ref.left_to_back()
    assert left_to_back.left == -FRONT
    assert left_to_back.right == -BACK
    assert left_to_back.back == LEFT
    assert left_to_back.front == RIGHT
    assert left_to_back.bottom == BOTTOM
    assert left_to_back.top == TOP

    right_to_bottom = ref.right_to_bottom()
    assert right_to_bottom.left == BOTTOM
    assert right_to_bottom.right == TOP
    assert right_to_bottom.back == BACK
    assert right_to_bottom.front == FRONT
    assert right_to_bottom.bottom == -RIGHT
    assert right_to_bottom.top == -LEFT

    right_to_top = ref.right_to_top()
    assert right_to_top.left == -TOP
    assert right_to_top.right == -BOTTOM
    assert right_to_top.back == BACK
    assert right_to_top.front == FRONT
    assert right_to_top.bottom == LEFT
    assert right_to_top.top == RIGHT

    right_to_front = ref.right_to_front()
    assert right_to_front.left == -FRONT
    assert right_to_front.right == -BACK
    assert right_to_front.back == LEFT
    assert right_to_front.front == RIGHT
    assert right_to_front.bottom == BOTTOM
    assert right_to_front.top == TOP

    right_to_back = ref.right_to_back()
    assert right_to_back.left == -FRONT
    assert right_to_back.right == -BACK
    assert right_to_back.back == LEFT
    assert right_to_back.front == RIGHT
    assert right_to_back.bottom == BOTTOM
    assert right_to_back.top == TOP

    X = 26
    Y = 34
    Z = 45
    translated = ref.translate(x=X, y=Y, z=Z)
    assert translated.left == LEFT + X
    assert translated.right == RIGHT + X
    assert translated.back == BACK + Y
    assert translated.front == FRONT + Y
    assert translated.bottom == BOTTOM + Z
    assert translated.top == TOP + Z


def test_modifiers():
    ref = Square(1, 1)
    rendered = ref.render()
    assert ref.root().render() == f"!{rendered}"
    assert ref.disable().render() == f"*{rendered}"
    assert ref.debug().render() == f"#{rendered}"
    assert ref.background().render() == f"%{rendered}"
    assert ref.background().remove_modifier().render() == rendered


def test_sum():

    assert (
        str(sum(Cube(1, 1, x) for x in range(2)))
        == """union() {
  cube(size=[1, 1, 0], center=true);
  cube(size=[1, 1, 1], center=true);
}"""
    )
