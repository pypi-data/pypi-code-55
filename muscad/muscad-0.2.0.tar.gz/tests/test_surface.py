from muscad import Circle, Square, Surface, Union


def test_heart_xy():
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_mirror(keep=True)
        .z_linear_extrude(bottom=-1, top=3)
    )

    assert (
        str(heart)
        == """translate(v=[0, 0, -1]) 
linear_extrude(height=4, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
}"""
    )


def test_spade_xy():
    spade = (
        (
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            )
            + Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            )
        )
        .x_mirror(keep=True)
        .z_linear_extrude(bottom=-1, top=4)
    )

    assert (
        str(spade)
        == """translate(v=[0, 0, -1]) 
linear_extrude(height=5, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
}"""
    )


def test_heart_xz():
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_mirror(keep=True)
        .y_linear_extrude(back=3, front=6)
    )

    assert (
        str(heart)
        == """translate(v=[0, 6, 0]) 
rotate(a=[90, 0, 0]) 
linear_extrude(height=3, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
}"""
    )


def test_spade_y():
    spade = (
        Union(
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            ),
            Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            ),
        )
        .x_mirror(keep=True)
        .y_linear_extrude(10, center_y=3)
    )

    assert (
        str(spade)
        == """translate(v=[0, 8.0, 0]) 
rotate(a=[90, 0, 0]) 
linear_extrude(height=10, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
}"""
    )


def test_heart_x():
    heart = (
        Surface.free(
            Circle(d=20).align(right=3, front=30),
            Circle(d=2).align(center_x=0, back=0),
        )
        .x_mirror(keep=True)
        .x_linear_extrude(5)
    )

    assert (
        str(heart)
        == """translate(v=[2.5, 0, 0]) 
rotate(a=[0, 270, 0]) 
linear_extrude(height=5, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
  hull() 
  {
    translate(v=[-7.0, 20.0, 0]) 
    circle(d=20, $fn=157);
    translate(v=[0.0, 1.0, 0]) 
    circle(d=2, $fn=15);
  }
}"""
    )


def test_spade_x():
    spade = (
        (
            Surface.free(
                Circle(d=20).align(right=0, back=5),
                Circle(d=2).align(center_x=0, front=35),
            )
            + Surface.free(
                Circle(d=2).align(right=5, back=0),
                Square(1, 15).align(left=0, back=0),
            )
        )
        .x_mirror(keep=True)
        .x_linear_extrude(9, left=-3)
    )

    assert (
        str(spade)
        == """translate(v=[6, 0, 0]) 
rotate(a=[0, 270, 0]) 
linear_extrude(height=9, center=false, convexity=10, twist=0.0, scale=1.0) 
{
  mirror(v=[1, 0, 0]) 
  {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
  union() {
    hull() 
    {
      translate(v=[-10.0, 15.0, 0]) 
      circle(d=20, $fn=157);
      translate(v=[0.0, 34.0, 0]) 
      circle(d=2, $fn=15);
    }
    hull() 
    {
      translate(v=[4.0, 1.0, 0]) 
      circle(d=2, $fn=15);
      translate(v=[0.5, 7.5, 0]) 
      square(size=[1, 15], center=true);
    }
  }
}"""
    )
