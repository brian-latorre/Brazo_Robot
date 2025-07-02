# Escaneo de código QR automatizado por brazo robot

>Este proyecto fue iniciado en el curso de Arquitectura de Computadoras de la Universidad Nacional de Ingeniería gracias al aporte del profezor César Martín Cruz Salazar con un brazo robot. 

## Descripción 

El proyecto es un sistema automatizado que combina el uso de un brazo robótico controlado por Arduino, un script Python y una cámara de celular, diseñado para **rotar un cubo hasta detectar una cara con un código QR en él y leer su información.**

La iniciativa surgió del objetivo de automatizar la lectura de datos de numerosos paquetes que ingresan diariamente a una tienda.

Este repositorio contiene todo lo que necesitas para replicar nuestro proyecto con el brazo robótico: 
- Programas
- Videos 
- Imágenes
- Renders
- Documentación

También puedes usarlo como guía para desarrollar tu propio proyecto, especialmente si estás comenzando desde cero, tal como hicimos nosotros.

## Objetivo del proyecto

- Automatizar la detección y lectura de códigos QR presentes en un cubo.
- Usar un brazo robótico para girar el cubo hasta encontrar la cara adecuada.
- Facilitar la reutilización del sistema por parte de estudiantes o desarrolladores nuevos.

## Software

- [Arduino IDE](https://www.arduino.cc/en/software/)
- Visual Studio Code
- [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&pli=1)

## Hardware

- Celular
- Brazo Robótico de 6 servomotores
- Arduino UNO Mini

## ¿Cómo empezar?

Recomendamos seguir la [documentación] que creamos para poder usar el brazo robótico. 

## Descargas

1. Descarga la carpeta [Programas](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas).
2. Abre el archivo [Arduino_Movimientos.ino](https://github.com/brian-latorre/Brazo_Robot/blob/main/Programas/ArduinoIDE/Arduino_Movimientos/Arduino_Movimientos.ino) con la aplicación Arduino IDE.
3. Presiona los botones _Verify_ y _Upload_ en Arduino IDE. (recomendamos que el brazo esté apagado para evitar movimientos bruscos)
4. Cierra el programa de Arduino IDE. (recomendamos revisar [documentación] para evitar errores)
5. Abre la aplicación IP Webcam en tu celular y posicionala para obtener una vista isométrica del cubo.
6. Abre el programa [Detectar_QR.py](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas/Python/Detectar_QR.py) y reemplaza la IP del programa por la IP que muestra la aplicación. (el programa y la aplicación deben estar conectados a la misma red)
7. Coloca el cubo en la posición de inicio.
8. Corre el programa [Detectar_QR.py](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas/Python/Detectar_QR.py).
9. Presiona **Empezar** en la interfaz. 

## Resultado Final

![Video]()

### Limitaciones

- Dependencia de buena iluminación para la cámara.
- Revisar que el brazo no esté torcido entre los servos _Codo-Muñeca-In_.
- Necesidad de bases para hacer los giros del cubo y poder agarrar los cubos de manera correcta. 

<img src="https://github.com/brian-latorre/Brazo_robot/blob/main/Multimedia/Servomotores.jpeg" width="400">

