
import os
from pyvista import examples
import numpy as np

import pyvista as pv
import json
import time

DIR = os.path.dirname(os.path.realpath(__file__))
SETTINGS = json.load(open(f"{DIR}\\settings\\settings.json"))

p = pv.Plotter()
legno = pv.Box()
pezzo = pv.PolyData()
punta = pv.Cylinder()
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
    global p
    bounds = [
        SETTINGS['Legno']['Starting point']['x'], 
        SETTINGS['Legno']['Starting point']['x']+SETTINGS['Legno']['Dimensions']['x'],
        SETTINGS['Legno']['Starting point']['y'], 
        SETTINGS['Legno']['Starting point']['y']+SETTINGS['Legno']['Dimensions']['y'],
        SETTINGS['Legno']['Starting point']['z'], 
        SETTINGS['Legno']['Starting point']['z']+SETTINGS['Legno']['Dimensions']['z'],
        ]
    legno = pv.Box(bounds=bounds).triangulate()
    
    dimensioni = [round(abs(bounds[0])+abs(bounds[1]),2),round(abs(bounds[2])+abs(bounds[3]),2),round(abs(bounds[4])+abs(bounds[5]),2)]
    AtestoLegno = p.add_text(f'Dimensioni Legno: \n x {dimensioni[0]}\ny {dimensioni[1]}\nz {dimensioni[2]}', 
                    position='upper_right', 
                    color='black',
                    font_size=10,
                )
    
    Alegno = p.add_mesh(legno,name=SETTINGS['Legno']['Name'], style=SETTINGS['Legno']['Style'], line_width=3, color="brown")
    return [Alegno,AtestoLegno]

def initializePezzo(src):
    global p
    global legno
    global pezzo

    try:
        pezzo = pv.read(src).triangulate()
        pezzo.rotate_z(-90)
        pezzo.translate([-pezzo.bounds[0],-pezzo.bounds[2],-pezzo.bounds[4]])
        dimensioni = [round(abs(pezzo.bounds[0])+abs(pezzo.bounds[1]),2),round(abs(pezzo.bounds[2])+abs(pezzo.bounds[3]),2),round(abs(pezzo.bounds[4])+abs(pezzo.bounds[5]),2)]
        pezzo.scale(
            [
                .06, #SONO DI PROVA
                .06,
                .04])

        dimensioni = [round(abs(pezzo.bounds[0])+abs(pezzo.bounds[1]),2),round(abs(pezzo.bounds[2])+abs(pezzo.bounds[3]),2),round(abs(pezzo.bounds[4])+abs(pezzo.bounds[5]),2)]
        pezzo['collision'] = np.zeros(pezzo.n_cells, dtype=bool)
        Apezzo = p.add_mesh(pezzo, style='')
        p.add_text(f'Dimensioni Pezzo: \n x {dimensioni[0]}\ny {dimensioni[1]}\nz {dimensioni[2]}', 
                        position='upper_left', 
                        color='black',
                        font_size=10)
        return Apezzo
    except:
        return 0

def initializePunta():
    global p
    global punta
    global legno
    global points

    punta = pv.Cylinder(radius=SETTINGS['Punta']['Radius'], direction=(0,0,1), center=(0,0,SETTINGS['Legno']['Dimensions']['z']+SETTINGS["Punta"]["Height"]),height=SETTINGS["Punta"]["Height"]).triangulate()
    Apunta = p.add_mesh(punta, color="grey", style='Wireframe')
    return [Apunta,0]

def main():
    global p
    global legno
    global pezzo
    global punta
    global quality
    global points

    initializePlotter()
    Alegno, AtestoLegno = initializeLegno()
    Apezzo = initializePezzo(src=f"{DIR}\\Pezzo.stl")
    Apunta, AtestoPunta = initializePunta()
    Alegno = p.add_mesh(legno, style = 'Wireframe', color="Brown")

    #p.add_mesh(pv.MultipleLines(points=points),color='Yellow')
    #print(len(points))

    #_ = p.add_checkbox_button_widget(CalcoloPunti,value=True)
    CalcoloPunti()
    p.show()

def CalcoloPunti():
    global legno
    global pezzo
    global points
    global p

    for z in range(int(legno.bounds[4]*10),int(legno.bounds[5]*10),int(quality*10)):
            for x in range(int(legno.bounds[0]*10),int(legno.bounds[1]*10),int(quality*10)):
                for y in range(int(legno.bounds[2]*10),int(legno.bounds[3]*10),int(quality*10)):
                    if([x/10,y/10,z/10] not in pezzo.points):
                        points.append([x/10,y/10,z/10])
    p.add_mesh(pv.MultipleLines(points=points),color='Yellow')
if __name__ == "__main__":
    main()