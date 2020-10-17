#Processing

# Tamaño de Graficos

n = 100 # Ancho de la Matriz
m = 100	# Alto de la Matriz
cellSize =7 # Ancho y Alto de la celda

# Conjunto de estados

Np = { # No hay nada en la celda 									= Negro
      "name": "Np",
      "color": color(0)
}
Ps = { # Personas sanas												= Verde
      "name": "Ps",
      "color": color(0, 255, 127)
}
Cs = { # Persona con Covid-19 sintomática							= Naranja
      "name": "Cs",
      "color": color(255, 127, 31),
      "ciclos": 0
}
Cns = { # Persona con Covid-19 asintomática							= Amarillo
       "name": "Cns",
       "color": color(255, 255, 0),
       "ciclos": 0
}
Ct = { # Persona con Covid-19 en cuarentena o en cuidados médicos	= Rojo
      "name": "Ct",
      "color": color(255, 0, 0),
      "ciclos": 0
}
Pac = { # Persona curada con anticuerpos							= Azul
       "name": "Pac",
       "color": color(0, 191, 255)
}
# M = Persona muerta. 												= Negro


# Condiciones Iniciales

Ps_Start = 5000
Cs_Start = 5
Cns_Start = 5

# Probabilidades

P_mover = 0.25
P_Sintomas = 0.7
P_Sobrevivir = 0.8

# Ciclos de cambio

Ciclos_To_Ct = 7
Ciclos_To_Pac = 30
Ciclos_From_Ct = 20

# Conteos

Muertos = 0
Ciclos = 0
Activos = Cs_Start+Cns_Start
Np_cont = 0
Ps_cont = 0
Cs_cont = 0
Cns_cont = 0
Ct_cont = 0
Pac_cont = 0

# Tiempos

T_ms = 100
T_anterior = 0

# Interaccion

proceso = True
moving = False
pause = False
imprimir_Controles = False
fin = False


# Configuracion Inicial

def setup():
    global celdas 		# Matriz
    global celdasTemp	# Matriz Temporal
    size(cellSize*n, cellSize*m)
    celdas = [[Np] * n for _ in range(m)] # Declaracion de la Matriz
    celdasTemp = [[Np] * n for _ in range(m)] # Declaracion de la Matriz Temporal
    noSmooth()
    Cs_loc = [[int(random(n)), int(random(m))] for _ in range(Cs_Start)]
    Cns_loc = [[int(random(n)), int(random(m))] for _ in range(Cns_Start)]
    Cs_cont = Cs_Start
    Cns_cont = Cns_Start
    for  x in range(n):
        for y in range(m):
            s = random(n*m-Cs_Start-Cns_Start)
            if s < Ps_Start:
                state = Ps
            else:
                state = Np
            if Cs_cont:
                for coord in range(Cs_Start):
                    if (Cs_loc[coord][0]==x) and (Cs_loc[coord][1]==y):
                        state = {
                                 "name": "Cs",
                                 "color": color(255, 127, 31),
                                 "ciclos": 0
                                 }
                        Cs_cont -= 1
                        break
            if Cns_cont:
                for coord in range(Cns_Start):
                    if (Cns_loc[coord][0]==x) and (Cns_loc[coord][1]==y):
                        state = {
                                 "name": "Cns",
                                 "color": color(255, 255, 0),
                                 "ciclos": 0
                                 }
                        Cns_cont -= 1
                        break
            celdas[x][y] = state
    background(0) # Llena toda la pantalla de negro en caso de que las celdas no cubran toda la ventana
    info_window = Info()
# Pintar el mapa

def draw():
    global T_anterior, imprimir, Ciclos, Activos, fin, Np_cont, Ps_cont, Cs_cont, Cns_cont, Ct_cont, Pac_cont, proceso, moving
    # Dibuja la matriz
    for x in range(n):
        for y in range(m):
            fill(celdas[x][y].get("color"))
            rect(x*cellSize,y*cellSize,cellSize,cellSize)
    # Maneja los tiempos de iteracion
    imprimir_Controles = False
    if millis()-T_anterior > T_ms:
        if not pause:
            if proceso:
                Activos = replicacion() # ---------- Algoritmo de replicacion-------------
            else:
                Ciclos += 1
                moving = True
                desplazamiento()
            proceso = not proceso
            T_anterior=millis()
            imprimir_Controles = True
    # Pausarlo para ver informacion actual o final
    if Activos==0:
        fin = True
    if pause or fin:
        for x in range(n):
            for y in range(m):
                celdasTemp[x][y]=celdas[x][y]
        #Conteos
        """Np_cont = 0
        Ps_cont = 0
        Cs_cont = 0
        Cns_cont = 0
        Ct_cont = 0
        Pac_cont = 0"""
        #Imprime Informacion Preliminar
        if fin:
            """for x in range(n):
                for y in range(m):
                    if celdas[x][y].get("name") == "Np":
                        Np_cont += 1
                    elif celdas[x][y].get("name") == "Ps":
                        Ps_cont += 1
                    elif celdas[x][y].get("name") == "Cs":
                        Cs_cont += 1
                    elif celdas[x][y].get("name") == "Cns":
                        Cns_cont += 1
                    elif celdas[x][y].get("name") == "Ct":
                        Ct_cont += 1
                    elif celdas[x][y].get("name") == "Pac":
                        Pac_cont += 1
                    else:
                        print("La casilla no corresponde con ningun estado")
            print("-----Situacion actual-----")
            print("Muertos:",Muertos)
            print("Activos:",Activos)
            print("Espacios vacios:",Np_cont)
            print("Personas Sanas:",Ps_cont)
            print("Personas con covid sintomaticas:",Cs_cont)
            print("Personas con covid asintomaticas:",Cns_cont)
            print("Personas en cuarentena:",Ct_cont)
            print("Personas curadas:",Pac_cont)
            print("Ciclos:",Ciclos)
            imprimir = False"""
            noLoop()
        #print(Ciclos)
# Proceso para la replicacion de los automatas según las reglas

def replicacion():
    global Muertos
    # Salvar Matriz
    activos = 0
    for x in range(n):
        for y in range(m):
            celdasTemp[x][y]=celdas[x][y]
            if (celdas[x][y].get("name")=="Cs") or (celdas[x][y].get("name")=="Cns") or (celdas[x][y].get("name")=="Ct"):
                activos += 1
    if activos == 0:
        return activos
    # Lectura del entorno de cada celda para determinar el futuro del automata
    for x in range(n):
        for y in range(m):
            infectados = 0
            if celdasTemp[x][y].get("name")=="Ps":
                for xx in range(x-1, x+2):
                    for yy in range(y-1, y+2):
                        if not (xx==x and yy==y):
                            if (celdasTemp[xx%n][yy%m].get("name") != "Np") and (celdasTemp[xx%n][yy%m].get("name") != "Ps"):
                                infectados += 1
                infectar = random(10)
                if infectar < infectados:
                    afeccion = random(1)
                    if afeccion < P_Sintomas:
                        celdas[x][y] = {
                                        "name": "Cs",
                                        "color": color(255, 127, 31),
                                        "ciclos": 0
                                        }
                    else:
                        celdas[x][y] = {
                                        "name": "Cns",
                                        "color": color(255, 255, 0),
                                        "ciclos": 0
                                        }
            elif celdasTemp[x][y].get("name")=="Cs":
                if celdas[x][y].get("ciclos")>=Ciclos_To_Ct:
                    celdas[x][y] = {
                                    "name": "Ct",
                                    "color": color(255, 0, 0),
                                    "ciclos": 1
                                    }
                else:
                    celdas[x][y]["ciclos"] += 1
            elif celdasTemp[x][y].get("name")=="Cns":
                if celdas[x][y].get("ciclos")>=Ciclos_To_Pac:
                    celdas[x][y] = Pac
                else:
                    celdas[x][y]["ciclos"] += 1
            elif celdasTemp[x][y].get("name")=="Ct":
                if celdas[x][y].get("ciclos")>=Ciclos_From_Ct:
                    ultimatum = random(1)
                    if ultimatum < P_Sobrevivir:
                        celdas[x][y] = Pac
                    else:
                        celdas[x][y] = Np
                        Muertos +=1
                else:
                    celdas[x][y]["ciclos"] += 1
    return activos

def desplazamiento():
    global moving
    for x in range(n):
        for y in range(m):
            if celdas[x][y].get("name") != "Np":
                move = random(1)
                moves = [0,0,0,0] # [Norte, Este, Sur, Oeste]
                for xx in range(x-1, x+2):
                    for yy in range(y-1, y+2):
                        if (xx!=x and yy==y) or (xx==x and yy!=y):
                            if yy>y and celdas[xx%n][yy%n].get("name")=="Np":
                                moves[0] = P_mover
                            elif xx>x and celdas[xx%n][yy%n].get("name")=="Np":
                                moves[1] = P_mover
                            elif yy<y and celdas[xx%n][yy%n].get("name")=="Np":
                                moves[2] = P_mover
                            elif xx<x and celdas[xx%n][yy%n].get("name")=="Np":
                                moves[3] = P_mover
                if move<moves[0]:
                    celdas[x][(y+1)%m] = celdas[x][y]
                    celdas[x][y] = Np
                elif move<(moves[0]+moves[1]) and move>moves[0]:
                    celdas[(x+1)%n][y] = celdas[x][y]
                    celdas[x][y] = Np
                elif move<(moves[0]+moves[1]+moves[2]) and move>(moves[0]+moves[1]):
                    celdas[x][y-1] = celdas[x][y]
                    celdas[x][y] = Np
                elif move<(moves[0]+moves[1]+moves[2]+moves[3]) and move>(moves[0]+moves[1]+moves[2]):
                    celdas[x-1][y] = celdas[x][y]
                    celdas[x][y] = Np
    moving = False
def keyPressed():
    global pause, Ciclos, fin, Muertos
    if key == 'r' or key == 'R':
        Ciclos = 0
        Muertos = 0
        # Restart: reinitialization of cells
        Cs_loc = [[int(random(n)), int(random(m))] for _ in range(Cs_Start)]
        Cns_loc = [[int(random(n)), int(random(m))] for _ in range(Cns_Start)]
        Cs_cont = Cs_Start
        Cns_cont = Cns_Start
        for  x in range(n):
            for y in range(m):
                s = random(n*m-Cs_Start-Cns_Start)
                if s < Ps_Start:
                    state = Ps
                else:
                    state = Np
                if Cs_cont:
                    for coord in range(Cs_Start):
                        if (Cs_loc[coord][0]==x) and (Cs_loc[coord][1]==y):
                            state = {
                                    "name": "Cs",
                                    "color": color(255, 127, 31),
                                    "ciclos": 0
                                    }
                            Cs_cont -= 1
                            break
                if Cns_cont:
                    for coord in range(Cns_Start):
                        if (Cns_loc[coord][0]==x) and (Cns_loc[coord][1]==y):
                            state = {
                                    "name": "Cns",
                                    "color": color(255, 255, 0),
                                    "ciclos": 0
                                    }
                            Cns_cont -= 1
                            break
                celdas[x][y] = state
        if fin:
            fin = False
            loop()
    if key == ' ':  # On/off of pause
        pause = not pause
    if (key == 'c' or key == 'C'):  # Clear all
        for x in range(n):
            for y in range(m):
                celdas[x][y] = Np  # Save all to zero

# Ventana de Informacion ------------------------------------------------------------------------------------------------------------------------------------------
class Info(PApplet):
    def __init__(self):
        switches = ('--sketch-path=' + sketchPath(), '')
        PApplet.runSketch(switches, self)  
        
    def settings(self):
        self.size(400, 550)
        
    def draw(self):
        #Conteos
        Np_cont = 0
        Ps_cont = 0
        Cs_cont = 0
        Cns_cont = 0
        Ct_cont = 0
        Pac_cont = 0
        #Revisa la Informacion Preliminar
        self.background(0)
        for x in range(n):
            for y in range(m):
                if celdas[x][y].get("name") == "Np":
                    Np_cont += 1
                elif celdas[x][y].get("name") == "Ps":
                    Ps_cont += 1
                elif celdas[x][y].get("name") == "Cs":
                    Cs_cont += 1
                elif celdas[x][y].get("name") == "Cns":
                    Cns_cont += 1
                elif celdas[x][y].get("name") == "Ct":
                    Ct_cont += 1
                elif celdas[x][y].get("name") == "Pac":
                    Pac_cont += 1
                #else:
                #    print("La casilla no corresponde con ningun estado")
        #Imprime la Informacion recogida
        self.fill(255)
        self.textAlign(CENTER)
        self.textSize(28)
        self.text(u"Situación actual:", 200, 50)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Muertos: ", 10, 100)
        self.textAlign(RIGHT)
        self.text(Muertos, 390, 100)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Activos: ", 10, 125)
        self.textAlign(RIGHT)
        self.text(Activos, 390, 125)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Espacios vacios: ", 10, 150)
        self.textAlign(RIGHT)
        self.text(Np_cont, 390, 150)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Personas Sanas: ", 10, 175)
        self.textAlign(RIGHT)
        self.text(Ps_cont, 390, 175)
        self.noStroke()
        self.fill(Ps.get("color"))
        self.rect(300, 162, 16, 16)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text(u"Personas con covid sintomáticas: ", 10, 200)
        self.textAlign(RIGHT)
        self.text(Cs_cont, 390, 200)
        self.noStroke()
        self.fill(Cs.get("color"))
        self.rect(300, 187, 16, 16)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text(u"Personas con covid asintomáticas: ", 10, 225)
        self.textAlign(RIGHT)
        self.text(Cns_cont, 390, 225)
        self.noStroke()
        self.fill(Cns.get("color"))
        self.rect(300, 212, 16, 16)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Personas en cuarentena: ", 10, 250)
        self.textAlign(RIGHT)
        self.text(Ct_cont, 390, 250)
        self.noStroke()
        self.fill(Ct.get("color"))
        self.rect(300, 237, 16, 16)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Personas curadas: ", 10, 275)
        self.textAlign(RIGHT)
        self.text(Pac_cont, 390, 275)
        self.noStroke()
        self.fill(Pac.get("color"))
        self.rect(300, 262, 16, 16)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Ciclos: ", 10, 300)
        self.textAlign(RIGHT)
        self.text(Ciclos, 390, 300)
        self.stroke(255)
        self.line(10, 325, 390, 325)
        self.textSize(28)
        self.textAlign(CENTER)
        self.text("Controles:", 200, 375)
        self.textAlign(LEFT)
        self.textSize(16)
        if pause:
            self.fill(color(0, 191, 255))
        self.text("Pausa: ", 10, 425)
        self.textAlign(RIGHT)
        self.text("Barra Espaciadora", 390, 425)
        self.fill(255)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Limpiar: ", 10, 450)
        self.textAlign(RIGHT)
        self.text("C", 390, 450)
        self.textAlign(LEFT)
        self.textSize(16)
        self.text("Resetear: ", 10, 475)
        self.textAlign(RIGHT)
        self.text("R", 390, 475)
        self.line(10, 500, 390, 500)
        self.textAlign(CENTER)
        self.textSize(10)
        self.text("Sebastian Sanchez y Johan Ruiz", 200, 525)

    def keyPressed(self, event):
        global pause, Ciclos, fin, Muertos
        if self.key == 'r' or self.key == 'R':
            Ciclos = 0
            Muertos = 0
            # Restart: reinitialization of cells
            Cs_loc = [[int(random(n)), int(random(m))] for _ in range(Cs_Start)]
            Cns_loc = [[int(random(n)), int(random(m))] for _ in range(Cns_Start)]
            Cs_cont = Cs_Start
            Cns_cont = Cns_Start
            for  x in range(n):
                for y in range(m):
                    s = random(n*m-Cs_Start-Cns_Start)
                    if s < Ps_Start:
                        state = Ps
                    else:
                        state = Np
                    if Cs_cont:
                        for coord in range(Cs_Start):
                            if (Cs_loc[coord][0]==x) and (Cs_loc[coord][1]==y):
                                state = {
                                         "name": "Cs",
                                         "color": color(255, 127, 31),
                                         "ciclos": 0
                                         }
                                Cs_cont -= 1
                                break
                    if Cns_cont:
                        for coord in range(Cns_Start):
                            if (Cns_loc[coord][0]==x) and (Cns_loc[coord][1]==y):
                                state = {
                                        "name": "Cns",
                                        "color": color(255, 255, 0),
                                        "ciclos": 0
                                        }
                                Cns_cont -= 1
                                break
                    celdas[x][y] = state
            if fin:
                fin = False
                loop()
        if self.key == ' ':  # On/off of pause
            pause = not pause
        if (self.key == 'c' or self.key == 'C'):  # Clear all
            for x in range(n):
                for y in range(m):
                    celdas[x][y] = Np  # Save all to zero
            loop()
