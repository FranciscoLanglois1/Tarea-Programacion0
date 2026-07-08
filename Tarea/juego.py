from figuras import Figuras

class Juego:
    def __init__(self, tablero):
        self.tablero = tablero
        self.figuras = Figuras(self.tablero.draw)
        self.carreteras = []
        self.figuras_hexagonos = {}  # clave: id_hex, valor: lista de tuplas (tipo, posicion)

    def agregar_carretera(self, id1, id2):
        try:
            hex1 = next(h for h in self.tablero.hexagonos if h.valor == id1)
            hex2 = next(h for h in self.tablero.hexagonos if h.valor == id2)
        except StopIteration:
            print("Uno de los hexágonos no existe.")
            return
        self.carreteras.append((id1, id2))

    def agregar_figura(self, id_hex, tipo, posicion):
        if posicion ==1:
            posicion = 6
        else:
            posicion= (posicion+5)%6
        if tipo not in {"pueblo", "ciudad", "ladron"}:
            print("Tipo de figura inválido.")
            return

        if not any(h.valor == id_hex for h in self.tablero.hexagonos):
            print("El hexágono no existe.")
            return

        if posicion < 1 or posicion > 6:
            print("Posición inválida. Debe ser entre 1 y 6.")
            return

        if id_hex not in self.figuras_hexagonos:
            self.figuras_hexagonos[id_hex] = []

        # Verificar si ya hay una figura en esa posición
        for fig, pos in self.figuras_hexagonos[id_hex]:
            if pos == posicion:
                print(f"Ya hay una figura en la posición {posicion} de este hexágono.")
                return

        if tipo == "ladron":
            for key in list(self.figuras_hexagonos):
                self.figuras_hexagonos[key] = [f for f in self.figuras_hexagonos[key] if f[0] != "ladron"]
            self.figuras_hexagonos[id_hex].append(("ladron", posicion))
            return

        # máximo 3 figuras distintas a ladron
        figuras_sin_ladron = [f for f in self.figuras_hexagonos[id_hex] if f[0] != "ladron"]
        if len(figuras_sin_ladron) >= 3:
            print("Máximo de 3 figuras (sin contar el ladrón) por hexágono alcanzado.")
            return

        self.figuras_hexagonos[id_hex].append((tipo, posicion))

    def mostrar(self):
        self.tablero.dibujar()
        self.figuras = Figuras(self.tablero.draw)

        for id1, id2 in self.carreteras:
            try:
                hex1 = next(h for h in self.tablero.hexagonos if h.valor == id1)
                hex2 = next(h for h in self.tablero.hexagonos if h.valor == id2)
                self.figuras.agregar_carretera(hex1, hex2)
            except StopIteration:
                continue

        for id_hex, figuras in self.figuras_hexagonos.items():
            try:
                hexagono = next(h for h in self.tablero.hexagonos if h.valor == id_hex)
                vertices = hexagono.vertices()
                for tipo, pos in figuras:
                    if 1 <= pos <= 6:
                        vx, vy = vertices[pos - 1]
                        if tipo == "pueblo":
                            self.figuras.triangulo(vx, vy, 10)
                        elif tipo == "ciudad":
                            self.figuras.cuadrado(vx, vy, 10)
                        elif tipo == "ladron":
                            self.figuras.circulo(vx, vy, 10)
            except StopIteration:
                continue

        self.tablero.img.show()

    def guardar_imagen(self, nombre="tablero_guardado.png"):
        self.tablero.dibujar()
        self.figuras = Figuras(self.tablero.draw)

        for id1, id2 in self.carreteras:
            try:
                hex1 = next(h for h in self.tablero.hexagonos if h.valor == id1)
                hex2 = next(h for h in self.tablero.hexagonos if h.valor == id2)
                self.figuras.agregar_carretera(hex1, hex2)
            except StopIteration:
                continue

        for id_hex, figuras in self.figuras_hexagonos.items():
            try:
                hexagono = next(h for h in self.tablero.hexagonos if h.valor == id_hex)
                vertices = hexagono.vertices()
                for tipo, pos in figuras:
                    if 1 <= pos <= 6:
                        vx, vy = vertices[pos - 1]
                        if tipo == "pueblo":
                            self.figuras.triangulo(vx, vy, 10)
                        elif tipo == "ciudad":
                            self.figuras.cuadrado(vx, vy, 10)
                        elif tipo == "ladron":
                            self.figuras.circulo(vx, vy, 10)
            except StopIteration:
                continue

        self.tablero.img.save(nombre)