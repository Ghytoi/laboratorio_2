from controller import Robot

robot = Robot()

TIME_STEP = 30

# Motores
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0)
right_motor.setVelocity(0)

# Sensores distancia
ps0 = robot.getDevice('ps0')  # frontal izquierda
ps7 = robot.getDevice('ps7')  # frontal derecha
ps5 = robot.getDevice('ps5')  # lateral izquierda
ps1 = robot.getDevice('ps1')  # lateral derecha

sensors = [ps0, ps1, ps5, ps7]

for s in sensors:
    s.enable(TIME_STEP)

# Encoders
left_encoder = robot.getDevice('left wheel sensor')
right_encoder = robot.getDevice('right wheel sensor')

left_encoder.enable(TIME_STEP)
right_encoder.enable(TIME_STEP)

# Variables Kalman
d_est = 80
P = 1
Q = 0.01
R = 5

while robot.step(TIME_STEP) != -1:

    # Lecturas
    front_left = ps0.getValue()
    front_right = ps7.getValue()

    left_side = ps5.getValue()
    right_side = ps1.getValue()

    # Medición sensores
    z = (front_left + front_right) / 2

    # Predicción
    P = P + Q
    d_pred = d_est

    # Corrección
    K = P / (P + R)

    d_est = d_pred + K * (z - d_pred)

    P = (1 - K) * P

    threshold = 70

    # Navegación reactiva
    if d_est < threshold:

        # avanzar
        left_motor.setVelocity(5)
        right_motor.setVelocity(5)

    else:

        # decidir giro
        if left_side > right_side:

            # girar derecha
            left_motor.setVelocity(3)
            right_motor.setVelocity(-3)

        else:

            # girar izquierda
            left_motor.setVelocity(-3)
            right_motor.setVelocity(3)

    print("Estimación:", d_est)