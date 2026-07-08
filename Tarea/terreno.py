import json
import random
from pieces import pieces
from puerto import Puerto
class Terreno:
    list = []
    numbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    materials = []

    def __init__(self)-> None:
        self.id = int
        self.material = str
        self.edges = {}
        self.corners = {}
        self.num = 0
        self.theif = bool

    def load(filename: str):
        with open(filename, 'r', encoding = 'utf-8' ) as f:
            data = json.load(f)
            for v in data["tiles"]:
                new = Terreno()
                new.id = (v["id"])
                new.material =(v["material"])
                new.edges = (v["edges"])
                if new.material == "desierto" or new.material == "desert":
                    new.theif = True
                else:
                    if new.material not in Terreno.materials:
                        Terreno.materials.append(new.material)
                    ficha = random.choice(Terreno.numbers)
                    new.num = ficha
                    new.theif = False
                    Terreno.numbers.remove(ficha)
                Terreno.list.append(new)

    def check_corner(self, corner: str) -> bool:
        return self.corners.get(corner) is None
    
    def update_terrain(self, corner: str, piece):
        self.corners[corner] = piece

    def produce(num) -> None:
        terrenos = Terreno.list
        for t in terrenos:
            if num == t.num and not t.theif:
                for piece in t.corners.values():
                    jug = piece.get_jug(piece.player)
                    resource = t.material
                    if piece.type == "city":
                        jug.agregar_cartas(resource, 2)
                    if piece.type == "village":
                        jug.agregar_cartas(resource, 1)

    def trade(self, terreno_id, player_name, material_in, material_out):
        terrenos = Terreno.list
        puertos = Puerto.list
        corners = ["top", "top-right", "bottom-right", "bottom", "bottom-left", "top-left"]
        directions = ["top-right", "right", "bottom-right", "bottom-left", "left", "top-left"]
        for terreno in terrenos:
            if terreno.id == terreno_id:
                for i in range(len(directions)):
                    direction = directions[i]

                    if direction in terreno.edges:
                        edge_id = terreno.edges[direction]

                        # Buscar puerto en ese edge
                        port = next((p for p in puertos if p.id == edge_id), None)

                        if port:
                            # Revisar esquinas asociadas
                            c1 = corners[i]
                            c2 = corners[(i + 1) % 6]

                            for corner in [c1, c2]:
                                if corner in terreno.corners:
                                    piece = terreno.corners[corner]
                                    jug = pieces.get_jug(piece.player)

                                    if jug.name == player_name:
                                        if port.material == "generic":
                                            if jug.cartas[material_in] >= 3:
                                                jug.quitar_cartas(material_in, 3)
                                                jug.agregar_cartas(material_out, 1)

                                        else:
                                            if jug.cartas[port.material] >= 2:
                                                jug.quitar_cartas(port.material, 2)
                                                jug.agregar_cartas(material_out, 1)
    
    def get_list(self):
        return Terreno.list

    def get_theif(self)->bool:
        return self.theif
    
    def get_id(self)->int:
        return self.id