import smbus
import time

# MPU6500 Registers
MPU_ADDR = 0x68  # Default I2C address of MPU6500

# I2C bus
bus = smbus.SMBus(1)

# Wake up the MPU6500
bus.write_byte_data(MPU_ADDR, 0x6B, 0x00)  # Write 0 to power management register to wake up the sensor





# Function to read accelerometer data
def read_accel_data():
    accel_x = bus.read_word_data(MPU_ADDR, 0x3B) / 16384.0
    accel_y = bus.read_word_data(MPU_ADDR, 0x3D) / 16384.0
    accel_z = bus.read_word_data(MPU_ADDR, 0x3F) / 16384.0
    return accel_x, accel_y, accel_z

# Function to read gyroscope data
def read_gyro_data():
    gyro_x = bus.read_word_data(MPU_ADDR, 0x43) / 131.0
    gyro_y = bus.read_word_data(MPU_ADDR, 0x45) / 131.0
    gyro_z = bus.read_word_data(MPU_ADDR, 0x47) / 131.0
    return gyro_x, gyro_y, gyro_z


# Function to calibrate accelerometer
def calibrate_accel():
    accel_x_offset = 0
    accel_y_offset = 0
    accel_z_offset = 0
    readings = 100  # Number of readings to average

    for _ in range(readings):
        accel_x, accel_y, accel_z = read_accel_data()
        accel_x_offset += accel_x
        accel_y_offset += accel_y
        accel_z_offset += accel_z
        time.sleep(0.1)

    # Average the readings
    accel_x_offset /= readings
    accel_y_offset /= readings
    accel_z_offset /= readings

    # Adjust offsets based on expected gravity (Z-axis should be 1g)
    accel_x_offset -= 0
    accel_y_offset -= 0
    accel_z_offset -= 16384  # 16384 is the typical value for 1g when the sensor is not tilted.

    print(f"Accelerometer Calibration Offsets: X={accel_x_offset}, Y={accel_y_offset}, Z={accel_z_offset}")
    return accel_x_offset, accel_y_offset, accel_z_offset

# Function to calibrate gyroscope
def calibrate_gyro():
    gyro_x_offset = 0
    gyro_y_offset = 0
    gyro_z_offset = 0
    readings = 100  # Number of readings to average

    for _ in range(readings):
        gyro_x, gyro_y, gyro_z = read_gyro_data()
        gyro_x_offset += gyro_x
        gyro_y_offset += gyro_y
        gyro_z_offset += gyro_z
        time.sleep(0.1)

    # Average the readings
    gyro_x_offset /= readings
    gyro_y_offset /= readings
    gyro_z_offset /= readings

    #print(f"Gyroscope Calibration Offsets: X={gyro_x_offset}, Y={gyro_y_offset}, Z={gyro_z_offset}")
    return gyro_x_offset, gyro_y_offset, gyro_z_offset


accel_x_offset, accel_y_offset, accel_z_offset = calibrate_accel()
gyro_x_offset, gyro_y_offset, gyro_z_offset = calibrate_gyro()

def get_mpu_values():
    
    accel_x, accel_y, accel_z = read_accel_data()
    gyro_x, gyro_y, gyro_z = read_gyro_data()

    accel_x -= accel_x_offset
    accel_y -= accel_y_offset
    accel_z -= accel_z_offset
    gyro_x -= gyro_x_offset
    gyro_y -= gyro_y_offset
    gyro_z -= gyro_z_offset

    
    accel_vector = (accel_x, accel_y, accel_z)  
    gyro_vector = (gyro_x, gyro_y, gyro_z)      

    return accel_vector, gyro_vector

