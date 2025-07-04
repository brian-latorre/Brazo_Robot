# Escaneo de código QR automatizado por brazo robot

>Este proyecto fue iniciado en el curso de Arquitectura de Computadoras de la Universidad Nacional de Ingeniería gracias al aporte del profezor César Martín Cruz Salazar con un brazo robot. 

<div align="center">
  <img src="https://raw.githubusercontent.com/brian-latorre/Brazo_robot/main/Multimedia/Servomotores_Readme.jpeg" width="350">
</div>

## Descripción 

El proyecto es un sistema automatizado que combina el uso de un brazo robótico controlado por Arduino, un script de Python y una cámara de celular, diseñado para **rotar un cubo hasta detectar una cara con un código QR en él y leer su información.**

La iniciativa surgió del objetivo de automatizar la lectura de datos de numerosos paquetes que ingresan diariamente a una tienda.

Este repositorio contiene todo lo que necesitas para replicar nuestro proyecto con el brazo robótico: 
- Programas
- Videos 
- Imágenes
- Renders
- Documentación

También puedes usarlo como guía para desarrollar tu propio proyecto, especialmente si estás comenzando desde cero, tal como lo hicimos nosotros.
Recomendamos la lectura de nuestra [documentación](https://github.com/brian-latorre/Brazo_Robot/blob/main/Documentos/Documentaci%C3%B3n_Brazo_Robot.pdf) para aprender sobre el brazo robótico. 

## Objetivo del proyecto

- Automatizar la detección y lectura de códigos QR presentes en un cubo.
- Usar un brazo robótico para girar el cubo hasta encontrar la cara adecuada.
- Facilitar la reutilización del sistema por parte de estudiantes o desarrolladores nuevos.

Este es un video de cómo un cubo realiza las rotaciones utilizando nuestro sistema, evidenciando que con estas rotaciones se pueden ver todas las caras de un cubo. 

https://github.com/user-attachments/assets/c4cf7143-7717-4c40-a67a-482367c9a5b3

## Software

- [Arduino IDE](https://www.arduino.cc/en/software/)
- Visual Studio Code
- [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&pli=1)

## Hardware

- Celular
- Brazo Robótico de 6 servomotores
- Arduino UNO Mini

## Requerimientos Físicos
Debido a las limitaciones del brazo, requerimos una nueva base para realizar las rotaciones y ayudar al brazo a que agarre el cubo en todo momento. La base del brazo necesitó aproximadamente 1.5cm de altura extra, las bases extras fueron hechas con corte láser mientras que sus patas fueron impresas en 3D. 

## ¿Cómo empezar?

1. Descarga la carpeta [Programas](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas).
2. Abre el archivo [Arduino_Movimientos.ino](https://github.com/brian-latorre/Brazo_Robot/blob/main/Programas/ArduinoIDE/Arduino_Movimientos/Arduino_Movimientos.ino) con la aplicación Arduino IDE.
3. Presiona los botones _Verify_ y _Upload_ en Arduino IDE. (recomendamos que el brazo esté apagado para evitar movimientos bruscos)
4. Cierra el programa de Arduino IDE.
5. Abre la aplicación IP Webcam en tu celular y posicionala para obtener una vista isométrica del cubo.
6. Abre el programa [Detectar_QR.py](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas/Python/Detectar_QR.py) y reemplaza la IP del programa por la IP que muestra la aplicación. (el programa y la aplicación deben estar conectados a la misma red)
7. Coloca el cubo en la posición de inicio.
8. Corre el programa [Detectar_QR.py](https://github.com/brian-latorre/Brazo_Robot/tree/main/Programas/Python/Detectar_QR.py).
9. Presiona **Empezar** en la interfaz. 

## Resultado Final

![Video]()

## Limitaciones

- Dependencia de buena iluminación para que la cámara lea correctamente los QR.
- Requiere ajustar bien la posición del brazo.
- Necesita una base física extra para sujetar y girar correctamente el cubo.




