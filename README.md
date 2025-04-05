# Sensores

## MPU9250 - Movimento e Orientação

O sensor MPU (como o MPU6050 ou MPU9250) é um módulo de medição inercial que combina:

- **Acelerómetro** – Mede aceleração nos eixos X, Y e Z, útil para detetar movimento e inclinação.
- **Giroscópio** – Mede a velocidade de rotação, permitindo detetar rotações e movimentos angulares.
- **Magnetómetro** – Mede o campo magnético, ajudando a determinar a orientação em relação ao norte magnético (bussola digital).

### Conexões

- **VCC -> 3.3V**
- **GND -> GND**
- **SCL -> GPIO3 (I2C SCL)**
- **SDA -> GPIO2 (I2C1 SDA)**
  
