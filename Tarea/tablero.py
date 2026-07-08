from PIL import Image, ImageDraw, ImageFont
import math
from hexagono import Hexagono


class Tablero:
    def __init__(self, filas= int, columnas= int)->None:
        
        #ajustes del tablero:
        self.filas:int = filas
        self.columnas:int = columnas
        self.radio:int = 55 #tamaño del hexagono
        self.hexagonos: list[Hexagono] = [] #los hexagonos
        #-----------------
        #lo necesario para generar la imagen 
        self.margen:int = 160 #permite centrar la imagen
        self.ancho = int(math.sqrt(3) * self.radio * (self.filas + 0.5) + 2 * 10)
        self.alto = int(1.5 * self.radio * (self.columnas - 1) + 2 * self.radio + 2 * 30)
        self.img = Image.new("RGB", (self.ancho, self.alto), "white")
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("arial.ttf", 20) 
        #-----------------------------


    def agregar_hexagono(self, fila, col, valor="", material = "", numero = "")->None:

        dy = col * 1.5 * self.radio + self.margen 
        # con la formula del ancho de un hexagono puedo sacar el punto y del hexagono (ya que la punta mira hacia arriba)
        # y la formula es 2*radio, pero con 2 me genera una separacion entre hexagonos, con 1.5 quedan
        # juntos, luego le sumo el margen para que queden centrados a la imagen
  
        dx = fila * math.sqrt(3) * self.radio + self.margen
        # lo mismo que antes, con la formula de la altura del hexagono puedo sacar el punto x,
        # la formula de la altura es raiz de 3 * radio 
        
        if col % 2:
            dx += (math.sqrt(3)/2 * self.radio)
        #se empezaron a apilar, asi que para evitar que se juntaran demasiado, los impares los baje a la mitad y quearon finos finos

        hexagono = Hexagono(dx, dy, self.radio, valor, material, numero) #x, y, tamamaño, Id del json

        #y con eso se sacan los puntos de cada vertice y los mando a la lista
        self.hexagonos.append(hexagono) #son puros puntos

    def dibujar(self)->None:
        self.img = Image.new("RGB", (self.ancho, self.alto), "white")
        self.draw = ImageDraw.Draw(self.img)
        from puerto import Puerto
        from terreno import Terreno
        for a in self.hexagonos: 
            puntos = a.vertices()
            self.draw.line(puntos + [puntos[0]], fill="black", width=2) 
            #este comando sinceramente lo del final no lo entiendo bien pq lo saque del tictactoe, pero lo de los puntos
            #es literalmente unir el siguiente con el anterior

            texto = a.valor #Id del json
            material = a.material
            numero = a.numero
            if material == "desert" or material == "desierto":
                for t in Terreno.list:
                    if t.id == texto:
                        if t.theif == True:
                            self.draw.text((a.cx -33, a.cy -8 ), "ladron", fill="black", font=self.font)
                        else:
                            self.draw.text((a.cx -33, a.cy -8 ), material, fill="black", font=self.font)
            elif texto in [p.id for p in Puerto.list]:
                self.draw.text((a.cx -15, a.cy +11 ), texto, fill="black", font=self.font)
                self.draw.text((a.cx -25, a.cy -11 ), material, fill="black", font=self.font)
            elif texto in [t.id for t in Terreno.list]:
                for t in Terreno.list:
                    if t.id == texto:
                        if t.theif == True:
                            self.draw.text((a.cx -33, a.cy -27 ), "ladron", fill="black", font=self.font)
                        else:
                            self.draw.text((a.cx -8, a.cy -27 ), numero, fill="black", font=self.font)
                self.draw.text((a.cx -15, a.cy +11 ), texto, fill="black", font=self.font)
                self.draw.text((a.cx -25, a.cy -11 ), material, fill="black", font=self.font)
            #el cx y cy son llamados desde la clase de hexagono pq son los puntos centrales de cada hexagono
            # y ese -9 y -8 son para centrar bien el texto

    def mostrar(self)->None:
        self.dibujar()
        self.img.show()



