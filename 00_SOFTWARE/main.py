
import os
from pyvista import examples
import numpy as np

import pyvista as pv
import json
import time

DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS = json.load(open(f"{DIR}\\settings\\settings.json"))

p = pv.Plotter()
legno = None
pezzo = None
punta = None
quality = SETTINGS['General']['Quality']
points = []

def initializePlotter():
    global p
    if SETTINGS['Plotter']['show_axes']:
        p.show_axes()
    if SETTINGS['Plotter']['show_grid']:
        p.show_grid()


def initializeLegno():
    global legno
    
    dimensions = SETTINGS['Legno']["Dimensions"]
    legno = pv.Box(level=2,bounds=([
            0,dimensions['x'],
            0,dimensions['y'],
            0,dimensions['z']
        ])).triangulate()
    return

def initializePezzo(src):
    global pezzo
    dimensioni = []

    try:
        pezzo = pv.get_reader(src)
        pezzo = pezzo.read()
    except:
        return
    print(f"Bounds: {pezzo.bounds}")
    
    for i in range(0,len(pezzo.bounds),2):
        if pezzo.bounds[i] < 0 and (pezzo.bounds[i+1] > 0 or pezzo.bounds[i+1] < 0):
            dimensioni.append(round(abs(pezzo.bounds[i])+abs(pezzo.bounds[i+1]),2))
        elif pezzo.bounds[i] > 0 and pezzo.bounds[i] > 0:
            dimensioni.append(round(abs(pezzo.bounds[i]-pezzo.bounds[i+1]),2))
    
    print(f"Dimensioni: {dimensioni}")
            

def initializePunta():
    pass

def main():
    initializePlotter()
    initializeLegno()
    initializePezzo(f"{DIR}\\Pezzo.stl")

    Alegno = p.add_mesh(legno,show_edges=True)
    Apezzo = p.add_mesh(pezzo,show_edges=True)

    p.show()
    
if __name__ == "__main__":
    main()