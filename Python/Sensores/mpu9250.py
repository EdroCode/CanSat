import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68, 
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)


mpu.configure()

def get_mpui_values():
   
    accel_data = mpu.readAccelerometerMaster()
    gyro_data = mpu.readGyroscopeMaster()
    mag_data = mpu.readMagnetometerMaster()

    return accel_data, gyro_data, mag_data