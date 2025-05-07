import smbus2
import time

MPU9250_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
MAG_ADDRESS = 0x0C  # AK8963 magnetometer (only in MPU9250)
AK8963_CNTL = 0x0A
AK8963_ASAX = 0x10
AK8963_ST1 = 0x02
AK8963_XOUT_L = 0x03

class MPU9250Sensor:
    def __init__(self, address=MPU9250_ADDRESS):
        self.address = address
        self.bus = smbus2.SMBus(1)
        self.failed = False
        self.has_magnetometer = False  # <--- Adicionado aqui

        try:
            self.initialize_sensor()
        except Exception as e:
            self.failed = True
            print(f"[ERRO] Falha ao inicializar MPU9250: {e}")

    def write_byte(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def read_i2c_word(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def initialize_sensor(self):
        self.write_byte(PWR_MGMT_1, 0x00)  # Wake up
        time.sleep(0.1)

        self.write_byte(0x1C, 0x00)  # ACCEL_CONFIG
        self.write_byte(0x1B, 0x00)  # GYRO_CONFIG

        # Ativar bypass I2C para comunicar com magnetómetro externo
        self.write_byte(USER_CTRL, 0x00)          # Desativa I2C master interno
        time.sleep(0.01)
        self.write_byte(INT_PIN_CFG, 0x02)        # Ativa bypass I2C
        time.sleep(0.01)

        # Tentar comunicar com o magnetómetro AK8963
        try:
            who_am_i = self.bus.read_byte_data(MAG_ADDRESS, AK8963_WHO_AM_I)
            if who_am_i == 0x48:
                self.bus.write_byte_data(MAG_ADDRESS, AK8963_CNTL, 0x00)
                time.sleep(0.01)
                self.bus.write_byte_data(MAG_ADDRESS, AK8963_CNTL, 0x16)  # Mode 2
                time.sleep(0.01)
                self.has_magnetometer = True
                print("[INFO] Magnetómetro AK8963 detetado.")
            else:
                print(f"[INFO] Magnetómetro respondeu, mas WHO_AM_I = 0x{who_am_i:X}")
        except Exception:
            print("[INFO] Magnetómetro não detetado. Pode ser um MPU6500 ou clone.")


    def read_accel_gyro(self):
        accel_x = self.read_i2c_word(ACCEL_XOUT_H)
        accel_y = self.read_i2c_word(ACCEL_XOUT_H + 2)
        accel_z = self.read_i2c_word(ACCEL_XOUT_H + 4)
        gyro_x = self.read_i2c_word(ACCEL_XOUT_H + 8)
        gyro_y = self.read_i2c_word(ACCEL_XOUT_H + 10)
        gyro_z = self.read_i2c_word(ACCEL_XOUT_H + 12)

        # Convert to G and degrees/sec
        accel_scale = 16384.0  # Â±2g
        gyro_scale = 131.0     # Â±250Â°/s

        return (
            gyro_x / gyro_scale,
            gyro_y / gyro_scale,
            gyro_z / gyro_scale,
            accel_x / accel_scale,
            accel_y / accel_scale,
            accel_z / accel_scale
        )

    def read_magnetometer(self):
        if not self.has_magnetometer:
            return (None, None, None)

        # Check data ready
        try:
            if self.bus.read_byte_data(MAG_ADDRESS, AK8963_ST1) & 0x01:
                data = self.bus.read_i2c_block_data(MAG_ADDRESS, AK8963_XOUT_L, 6)
                x = self._twos_complement(data[1] << 8 | data[0])
                y = self._twos_complement(data[3] << 8 | data[2])
                z = self._twos_complement(data[5] << 8 | data[4])
                return (x * 0.15, y * 0.15, z * 0.15)  # Convert to microteslas
            else:
                return (None, None, None)
        except Exception as e:
            print(f"[ERRO] MagnetÃ³metro: {e}")
            return (None, None, None)

    def _twos_complement(self, val, bits=16):
        if val & (1 << (bits - 1)):
            val = val - (1 << bits)
        return val

    def read(self):
        try:
            gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = self.read_accel_gyro()
            mag_x, mag_y, mag_z = self.read_magnetometer()
            return gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z
        except Exception as e:
            print(f"[ERRO] Falha ao ler MPU9250: {e}")
            return (None,) * 9


if __name__ == "__main__":
    mpu = MPU9250Sensor()
    if not mpu.failed:
        while True:
            values = mpu.read()
            print(f"GiroscÃ³pio: {values[:3]}")
            print(f"AcelerÃ´metro: {values[3:6]}")
            print(f"MagnetÃ´metro: {values[6:]}")
            print("---")
            time.sleep(1)
