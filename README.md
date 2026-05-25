Laboratorio 2: Navegación Reactiva con Filtrado y Fusión de Sensores en Webots

Integrantes
-	Ingerber Sobarzo
  
Objetivo
Implementar un sistema de navegación reactiva en Webots utilizando sensores de distancia y encoders de rueda, aplicando técnicas de filtrado y un filtro de Kalman para estimar de forma más robusta la distancia frontal a obstáculos y mejorar la toma de decisiones del robot.
Robot y Sensores Utilizados
Para el desarrollo del laboratorio se utilizó el robot e-puck de Webots, el cual corresponde a un robot móvil diferencial con dos ruedas motrices independientes.

Sensores utilizados:
- ps0: sensor frontal izquierdo
- ps7: sensor frontal derecho
- ps5: sensor lateral izquierdo
- ps1: sensor lateral derecho

Encoders utilizados:
- left wheel sensor
- right wheel sensor
Frecuencia de Muestreo
El controlador fue ejecutado utilizando un TIME_STEP de 30 ms.

Por lo tanto:
Ts = 0.03 s
fs = 1 / Ts = 33.3 Hz

Esto significa que el robot actualiza sus sensores y decisiones aproximadamente 33 veces por segundo.
Descripción General del Controlador
El controlador implementado considera:
- Inicialización de motores
- Lectura de sensores de distancia
- Lectura de encoders
- Fusión sensorial mediante filtro de Kalman
- Estimación de distancia frontal
- Navegación reactiva
- Evitación de obstáculos
Inicialización de Motores
Los motores fueron configurados en modo velocidad:

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

Esto permite controlar directamente la velocidad angular de las ruedas.
Lectura de Sensores
En cada iteración del controlador se obtienen las lecturas de los sensores:

front_left = ps0.getValue()
front_right = ps7.getValue()

left_side = ps5.getValue()
right_side = ps1.getValue()

Posteriormente se calcula una medición frontal promedio:

z = (front_left + front_right) / 2

Esta medición corresponde a la variable utilizada por el filtro de Kalman.
Análisis de Señales
Las señales entregadas por los sensores presentan ruido y pequeñas variaciones incluso cuando el robot permanece frente al mismo obstáculo.

Estas variaciones se producen debido a:
- ruido electrónico,
- reflexiones infrarrojas,
- pequeñas variaciones en la orientación del robot,
- limitaciones propias de los sensores.

Por esta razón, utilizar directamente las lecturas crudas puede producir movimientos inestables y giros innecesarios.
Estimación del Avance mediante Encoders
Los encoders entregan desplazamientos angulares en radianes.

El desplazamiento lineal puede estimarse mediante:

s = rθ

donde:
- s es el desplazamiento lineal
- r es el radio de la rueda
- θ es el desplazamiento angular

En la implementación actual los encoders fueron habilitados correctamente y utilizados como parte de la estructura general del sistema de navegación.
Filtro Simple Aplicado
Como filtro simple se utilizó el promedio entre ambos sensores frontales:

z = (front_left + front_right) / 2

Este promedio reduce parcialmente el ruido presente en cada sensor individual y mejora la estabilidad de la medición frontal.
Implementación del Filtro de Kalman
Se implementó un filtro de Kalman escalar para estimar la distancia frontal al obstáculo más cercano.

Variables utilizadas:
- d_est = 80
- P = 1
- Q = 0.01
- R = 5

Donde:
- d_est corresponde a la distancia estimada
- P corresponde a la covarianza del error
- Q representa el ruido del modelo
- R representa el ruido de medición
Etapa de Predicción
La etapa de predicción fue implementada mediante:

P = P + Q
d_pred = d_est

En esta etapa el filtro estima el nuevo estado utilizando la estimación anterior y el modelo de movimiento.
Ganancia de Kalman
La ganancia de Kalman se calcula mediante:

K = P / (P + R)

La ganancia determina cuánto confía el filtro en la predicción y cuánto en la medición.

Si la medición es muy ruidosa, el filtro confía más en la predicción.
Si la predicción es muy incierta, el filtro confía más en la medición.
Etapa de Corrección
La etapa de corrección fue implementada mediante:

d_est = d_pred + K * (z - d_pred)

Esta ecuación combina la predicción obtenida por el modelo y la medición real entregada por los sensores frontales.
Navegación Reactiva
La lógica reactiva utiliza la distancia estimada mediante el filtro de Kalman.

Se definió un umbral de seguridad:
threshold = 70

Si la distancia estimada es menor al umbral, el robot avanza:

left_motor.setVelocity(5)
right_motor.setVelocity(5)

En caso contrario, el robot gira para evitar el obstáculo.

La dirección del giro se decide utilizando los sensores laterales:
- si el obstáculo está más próximo por la izquierda, el robot gira a la derecha,
- si el obstáculo está más próximo por la derecha, el robot gira a la izquierda.
Escenarios de Prueba
Se diseñaron dos escenarios de prueba:

1. Entorno simple:
- pocos obstáculos
- espacios amplios
- navegación sencilla

2. Entorno complejo:
- múltiples obstáculos
- zonas estrechas
- necesidad de maniobras frecuentes.
Resultados Obtenidos
Durante las pruebas se observaron los siguientes resultados:

- El robot logró evitar colisiones correctamente.
- El filtro de Kalman entregó una estimación más estable que las lecturas crudas.
- Se redujeron movimientos bruscos y oscilaciones.
- Los sensores laterales permitieron seleccionar correctamente la dirección de giro.
- El comportamiento reactivo mejoró utilizando señales filtradas.
Comparación entre Señales
Lecturas crudas:
- mayor ruido
- variaciones rápidas
- decisiones menos estables

Señales filtradas:
- menor variación
- movimiento más suave
- menos oscilaciones

Estimación con Kalman:
- mayor estabilidad
- mejor comportamiento reactivo
- decisiones más robustas frente al ruido

Conclusiones
En este laboratorio se implementó exitosamente un sistema de navegación reactiva utilizando sensores de distancia y fusión sensorial mediante filtro de Kalman.

El filtro permitió obtener una estimación más estable de la distancia frontal, reduciendo el efecto del ruido presente en las mediciones.

La navegación reactiva permitió al robot avanzar y evitar obstáculos utilizando información frontal y lateral.

Como mejora futura, podría incorporarse una predicción más precisa utilizando directamente el desplazamiento calculado mediante los encoders.

Instrucciones de Ejecución
1. Abrir el proyecto en Webots.
2. Cargar el mundo del laboratorio.
3. Ejecutar el controlador del robot.
4. Iniciar la simulación.
5. Observar el comportamiento del robot y las estimaciones mostradas por consola.
