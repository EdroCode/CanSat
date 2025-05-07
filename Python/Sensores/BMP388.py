import smbus2
import time
import struct

# BMP388 Registers
BMP388_ADDR = 0x76  # I2C Address for BMP388
BMP388_REG_DATA = 0x04  # Register for reading data (Temperature, Pressure, and Altitude)
BMP388_REG_CTRL_MEAS = 0x01  # Control register for measurement
BMP388_REG_STATUS = 0x03  # Status register

class BMP388Sensor:
    def __init__(self, address=BMP388_ADDR):
        self.address = address
        self.bus = smbus2.SMBus(1)  # Bus 1 is usually the default on Raspberry Pi
        self.failed = False

        # Initialize the sensor
        try:
            self.initialize_sensor()
        except Exception as e:
            self.failed = True
            print(f"[ERRO] Falha ao inicializar BMP388: {e}")

    def initialize_sensor(self):
        # Initialize the BMP388 sensor for temperature and pressure measurement
        self.write_register(BMP388_REG_CTRL_MEAS, 0x44)  # Set normal mode for temperature and pressure
        time.sleep(0.1)  # Delay for the sensor to initialize properly

    def read_register(self, reg):
        try:
            return self.bus.read_byte_data(self.address, reg)
        except Exception as e:
            print(f"[ERRO] Falha ao ler o registrador {hex(reg)}: {e}")
            return None

    def write_register(self, reg, value):
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as e:
            print(f"[ERRO] Falha ao escrever no registrador {hex(reg)}: {e}")

    def read_data(self):
        # Read the raw data (temperature, pressure, and altitude) from the BMP388
        try:
            data = self.bus.read_i2c_block_data(self.address, BMP388_REG_DATA, 6)

            # Data format: 3 bytes for pressure, 3 bytes for temperature
            pressure_raw = struct.unpack('>I', bytes([0] + data[0:3]))[0]  # Convert to 24-bit pressure
            temp_raw = struct.unpack('>I', bytes([0] + data[3:6]))[0]  # Convert to 24-bit temperature

            # Process the temperature and pressure raw data
            pressure = pressure_raw / 100  # Pressure in hPa (Pascal / 100)
            temperature = temp_raw / 100  # Temperature in Celsius (100x the actual temperature)
            altitude = self.calculate_altitude(pressure)

            return temperature, pressure, altitude
        except Exception as e:
            print(f"[ERRO] Falha ao ler os dados do BMP388: {e}")
            return None, None, None

    def calculate_altitude(self, pressure):
        # Altitude calculation based on pressure
        # Assuming standard atmospheric pressure (1013.25 hPa)
        sea_level_pressure = 1013.25
        altitude = 44330 * (1 - (pressure / sea_level_pressure) ** 0.1903)
        return altitude

    def read(self):
        # Get the sensor's temperature, pressure, and altitude
        return self.read_data()


if __name__ == "__main__":
    bmp = BMP388Sensor()

    if not bmp.failed:
        while True:
            temperature, pressure, altitude = bmp.read()
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Pressure: {pressure:.2f} hPa")
            print(f"Altitude: {altitude:.2f} meters")
            time.sleep(1)
