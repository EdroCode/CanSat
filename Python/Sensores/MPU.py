import FaBo9Axis_MPU9250

class MPU9250Sensor:
    def __init__(self):
        try:
            self.sensor = FaBo9Axis_MPU9250.MPU9250()
            self.failed = False
        except Exception as e:
            print("[ERRO] Não foi possível inicializar o MPU9250:", e)
            self.sensor = None
            self.failed = True

    def read(self):
        if self.failed or self.sensor is None:
            return None
        try:
            accel = self.sensor.readAccel()
            gyro = self.sensor.readGyro()
            mag = self.sensor.readMagnet()

            return (
                gyro.get("x"), gyro.get("y"), gyro.get("z"),
                accel.get("x"), accel.get("y"), accel.get("z"),
                mag.get("x"), mag.get("y"), mag.get("z")
            )
        except Exception as e:
            print("[ERRO] Falha ao ler dados do MPU9250:", e)
            return None
