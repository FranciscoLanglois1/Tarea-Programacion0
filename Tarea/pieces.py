class pieces:

    def __init__(self):
        self.player: str #id del jugador dueño de la pieza
        self.type: str #road / village / city para el tipo de pieza
        self.id: str # id
        self.roads: dict = {} #caminos que conectan la pieza con otras piezas basado en direccion (formato :{[direccion]: id_pieza en esa direccion})
    directions = ["top-left","top-right","left","right","bottom-left","bottom-right"]
    #nota, hacer el imput para poner una ciudad como una pregunta binaria, ej:
    # presione 1 0 2 para
    # 1) ciudad
    # 2) pueblo
    def get_jug(self, player): 
        from jugador import Jugador
        for i in Jugador.list:
            if i.name == player:
                jug = i
        return jug

    def place_road(self, source: str, direction: int, player):

        jug = self.get_jug(player)

        if jug.cartas['clay']<1 or jug.cartas['wood']<1:
            print("recursos insuficientes")
        else:
            if len(jug.roads)<15:
                n = len(jug.carreteras)
                jug.quitar_carta('clay', 1)
                jug.quitar_carta('wood', 1)
    
    def update_build(self, structure: str, direction: str):

        self.roads[direction] = structure

    def place_village(self, tile:str, point: int, player: str) -> None:
        from terreno import Terreno
        jug = self.get_jug(player)
        corners = ["top", "top-right","bottom-right", "bottom", "bottom-left", "top-left" ]
        directions = ["top-left", "top-right", "right", "bottom-right", "bottom-left", "left"]
        corner = corners[point-1]
        if jug.cartas['clay']<1 or jug.cartas['wood']<1 or jug.cartas['wool']<1 or jug.cartas['cereal']<1:
            print("recursos insuficientes")
        else:
            if len(jug.piezas["pueblos"]) < 5:
                jug.quitar_carta('wood', 1)
                jug.quitar_carta('clay', 1)
                jug.quitar_carta('wool', 1)
                jug.quitar_carta('cereal', 1)
                for i in range(1,6):
                    if all(p.id != f"v0{i}" for p in jug.piezas["pueblos"]):
                        self.id = f"v0{i}" 
                        break
                terrenos = Terreno.list
                for i in range(1,4):
                    if i == 1:
                        terreno = next((t for t in terrenos if t.id == tile), None)
                        if terreno.check_corner(corner): 
                            self.type = "village"
                            self.player = jug.name
                            jug.piezas["pueblos"].append(self)
                            jug.puntos += 1  # Aumentar los puntos del jugador
                            # Actualizar el terreno para reflejar el pueblo
                            terreno.update_terrain(corner, self)
                            terreno1 = terreno

                    else:
                        dir = (point+i-3)%6
                        cor = (point-3+2*i)%6
                        if directions[dir] in terreno1.edges:
                            terreno = next((t for t in terrenos if t.id == terreno1.edges[directions[dir]]), None)
                            corner = corners[cor]
                            if terreno is None:
                                break
                            if terreno.check_corner(corner):
                                terreno.update_terrain(corner, self)

    def upgrade_village(self, village, player) -> None:

        jug = self.get_jug(player)

        if jug.cartas['cereal']<2 or jug.cartas['mineral']<3:
            print("recursos insuficientes")
        else:
            if len(jug.piezas["ciudades"]) < 4:
                n = len(jug.ciudades)
                pueblo = None
                for p in jug.piezas['pueblos']:
                    if p.id == village:
                        pueblo = p
                        break
            
                jug.quitar_carta('cereal', 2)
                jug.quitar_carta('mineral', 3)

                self.id = f"c0{n+1}" 
                self.type = "city"

                jug.piezas['pueblos'].drop(pueblo)
                jug.piezas["ciudades"].append(self) 
                jug.puntos += 1    