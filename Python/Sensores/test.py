import smbus2

bus = smbus2.SMBus(1)
mpu_address = 0x68  

try:
    # L� 6 bytes do aceler�metro (registos 0x3B a 0x40)
    accel = bus.read_i2c_block_data(mpu_address, 0x3B, 6)
    
    # L� 6 bytes do girosc�pio (registos 0x43 a 0x48)
    gyro = bus.read_i2c_block_data(mpu_address, 0x43, 6)

    print(f"Aceler�metro: {accel}")
    print(f"Girosc�pio: {gyro}")

except Exception as e:
    print(f"Erro ao ler sensores: {e}")
