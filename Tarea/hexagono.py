import math

#clase q hice dedicada a la creacion de los vertices del hexagono
class Hexagono:
    def __init__(self, cx: float, cy: float, radio: float, valor: str = "", material: str = "", numero: str = ""):
        self.cx = cx #coord x 
        self.cy = cy #coord y 
        self.radio = radio #tamaño del hexagono
        self.valor = valor #Id del json
        self.material = material
        self.numero = numero

    # sirve para calcular los 6 puntos que forman el borde del hexágono. no saben cuanto me demore buscando esto xDDDDDD
    # su forma de funcionamiento es que va girando 60 grados en cada punto hasta hacer los 6
    def vertices(self):
        puntos = []
        for i in range(6):
            angulo = math.radians(60 * i - 30)
            x = self.cx + self.radio * math.cos(angulo)
            y = self.cy + self.radio * math.sin(angulo)
            puntos.append((x, y))
        return puntos

    
