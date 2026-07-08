import math

class Figuras:
    def __init__(self, draw):
        self.draw = draw

    def triangulo(self, x, y, tam): #pueblo
        h = tam * math.sqrt(3) / 2
        puntos = [
            (x, y - h / 2),
            (x - tam / 2, y + h / 2),
            (x + tam / 2, y + h / 2)
        ]
        self.draw.polygon(puntos, fill="red")

    def cuadrado(self, x, y, tam): #para ciudad 
        self.draw.rectangle([
            (x - tam/2, y - tam/2),
            (x + tam/2, y + tam/2)
        ], fill="blue")

    def circulo(self, x, y, radio): #para el ladron
        self.draw.ellipse([
            (x - radio, y - radio),
            (x + radio, y + radio)
        ], fill="black")

    def agregar_carretera(self, hex1, hex2, color="green", grosor=3): #las carreteras
        p1 = (hex1.cx, hex1.cy)
        p2 = (hex2.cx, hex2.cy)
        self.draw.line([p1, p2], fill=color, width=grosor)
            