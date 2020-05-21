def get_bno():
    import board
    import busio
    import adafruit_bno055
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    data = {
        'temperature': sensor.temperature,
        'acceleration': sensor.acceleration,
        'gyro': sensor.gyro,
        'magnetic': sensor.magnetic,
        'euler': sensor.euler,
        'quaternion': sensor.quaternion,
        'linear_acceleration': sensor.linear_acceleration,
        'gravity': sensor.gravity,
    }
    return data