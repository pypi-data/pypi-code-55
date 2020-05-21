def get_bme():
    import board
    import busio
    import adafruit_bme680
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    data = {
        'temperature': sensor.temperature,
        'gas': sensor.gas,
        'humidity': sensor.humidity,
        'pressure': sensor.pressure
    }
    return data
