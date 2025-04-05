from Sensores.DHT22 import get_dht22
from Sensores.mpu9250 import get_mpu_values
from Interface import update_values, root
from time import sleep
import os

mode = 0   # terminal = 1 Interface = 0


# Verifical se o sensor retornou uma variavel real
def verify_value(val):
    return val if val is not None else "N/A"



def update():
    inside_temp, inside_hum = verify_value(get_dht22())
    accel_vector, gyro_vector = verify_value(get_mpu_values())
    update_values(inside_temp, inside_hum, accel_vector, gyro_vector, 0)
    
    root.after(1000, update) 


def setup():
    
    root.after(1000, update) 
    root.mainloop()

def terminal_mode():

    inside_temp, inside_hum = get_dht22()

    print("Temperatura:" + str(inside_temp))
    print("Humidade:" + str(inside_hum))
    sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(accel_values)
    #print(gyro_values)
    #print(mag_values)


if __name__ == "__main__":

    print("Programa Inicializado")
    print("Iniciando e calibrando os Sensores...")
    setup()
    sleep(3)
    while True:
        update()


