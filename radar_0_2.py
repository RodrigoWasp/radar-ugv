# -*- coding: utf-8 -*-
#librerias
import sys
import pygame
import numpy as np
import serial
from pygame.locals import *

textoin = ""
    #dispone la pantalla en 700x700
    def main():
    (w,h) = (700,700)
    x = [0]*50
    y = [0]*50
    deg = 0
    L1 = 0
    #instancia la pantalla de pygame
    pygame.init()
    pygame.display.set_mode((w, h), 0, 32)
    screen = pygame.display.get_surface()
    ser = serial.Serial("/dev/ttyUSB0",115200)
    #texto para imprimir datos relevantes
    while (True):
        #limpia la pantalla
        screen.fill((0, 20, 0, 0))
        textoin = ser.readline()         #lee los datos desde la serial
        textoin=textoin[:len(textoin)-3] #salta el   error de la toma de datos
        arreglom = fragmentar(textoin)   #fragmenta el arreglo y lo deja listo
        #empieza a trabajar con los datos fragmentados

        for data in arreglom:
            print data
            (L, deg) = data.split("-")
            (L, deg) = (int(float(L)), int(deg))
            #guarda el dato anterior y lo reutiliza
            if(L == (1.0 or 1)):
                L = L1
            else:
                L1 = L
            L = map(L,0,511,0,350) #se escalan las medidas que para no salgan de la pantalla
            #simula la forma del radar
            for i in range(1, 2):
                dx = w/2 * np.cos(np.radians(deg-i)) + w/2
                dy = h/2 * np.sin(np.radians(deg-i)) + h/2
                #dibuja la linea roja para
                pygame.draw.aaline(screen, (200,0,0), (w/2, h/2), (dx, dy),0)

            #dibuja el fondo
            pygame.draw.circle(screen, (0, 200, 0), (w/2, h/2), w/2, 1)
            pygame.draw.circle(screen, (0, 200, 0), (w/2, h/2), w/4, 1)
            pygame.draw.line(screen, (0, 200, 0), (0, h/2), (w, h/2))
            pygame.draw.line(screen, (0, 200, 0), (w/2, 0), (w/2, h))

            #calcula los valores de las cordenadas en eje x e y
            x0 = int(L*np.cos(np.radians(deg))) + w/2
            y0 = int(L*np.sin(np.radians(deg))) + h/2
            #no entiendo por qué chucha popea
            x.pop(49)
            y.pop(49)
            #inserta los datos en el arreglo  y los utiliza para dibujar el ultimo punto
            x.insert(0,x0)
            y.insert(0,y0)
            #Escribe las lineas del sensor
            for i in range(1, len(x)):
                pygame.draw.line(screen, (0, 255, 0),(w/2,h/2), (x[i], y[i]), 3)
            pygame.time.wait(10)
            pygame.display.update()

            #sale del radar
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


#--------------------------------funciones-------------------------------------

def map(x,in_min,in_max,out_min,out_max): #valor a escalar, minimo de entrada, maximo de salida, minimo de entrada, maximo salida
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def fragmentar(texto):
    arreglo = []
    arreglo = texto.split("#")
    return arreglo

#-- main --
main()