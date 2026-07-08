from generador_tablero import GeneradorTablero
from jugador import Jugador
from pieces import pieces
from terreno import Terreno
from puerto import Puerto
from juego import Juego
import random

class Menu:
    def __init__(self) -> None:
        print("Menu")
        self.generador = GeneradorTablero()
        self.juego = None

    def Start(self):

        for m in Terreno.materials:
            Jugador.crear_cartas(m)
        
        jugadores = self.def_jugadores()
        orden = self.orden_de_juego(jugadores)

        for i in orden:
            pieza = pieces()
            tile = input(f"{i.name} escribe el id del terreno en el que quere poner la pieza: ")
            print("1- top") 
            print("2- top-right") 
            print("3- bottom-right") 
            print("4- bottom") 
            print("5- bottom-left") 
            print("6- top-left")
            corner = int(input(f"{i.name} en cual esquina la quieres ubicar el poblado (1,6): ")) 
            i.agregar_cartas('wood', 2)
            i.agregar_cartas('clay', 2)
            i.agregar_cartas('wool', 1)
            i.agregar_cartas('cereal', 1)
            pieza.place_village(tile, corner, i.name)
            self.agregar_construccion("pueblo",tile,corner)

            #road = pieces()
            #road.place_road("vo1",direccion,i.name)
        
        for i in range(len(orden)):
            player = orden[-1-i]
            pieza = pieces()
            tile = input(f"{player.name} escribe el id del terreno en el que queres poner la pieza: ")
            print("1- top") 
            print("2- top-right") 
            print("3- bottom-right") 
            print("4- bottom") 
            print("5- bottom-left") 
            print("6- top-left")
            corner = int(input(f"{player.name} en cual esquina la quieres ubicar el poblado (1,6): ")) 
            player.agregar_cartas('wood', 2)
            player.agregar_cartas('clay', 2)
            player.agregar_cartas('wool', 1)
            player.agregar_cartas('cereal', 1)
            pieza.place_village(tile, corner, player.name)
            self.agregar_construccion("pueblo",tile,corner)

        turn = 0
        while all(jugador.puntos < 10 for jugador in orden):
            player = orden[turn]
            player.tirar_dados()

            self.juego.mostrar()

            action = "pending"
            while action != "pasar":
                action = input("te gustaria construir,negociar,carta de desarrollo o pasar: ")
                if action == "construir":
                    for k in player.cartas.keys():
                        print(f"tienes {player.cartas[k]} cartas de {k}\n")
                    construction = input("quieres construir un camino, poblado, ciudad o carta de desarrollo: ")
                    if construction == "camino":
                        pieza.place_road("p","j",player.name)
                        self.agregar_construccion(self,"carretera","p",0)
                    if construction == "poblado":
                        pieza = pieces()
                        tile = input(f"{player.name} escribe el id del terreno en el que queres poner la pieza: ")
                        print("1- top") 
                        print("2- top-right") 
                        print("3- bottom-right") 
                        print("4- bottom") 
                        print("5- bottom-left") 
                        print("6- top-left")
                        corner = int(input(f"{player.name} en cual esquina la quieres ubicar el poblado (1,6): "))
                        pieza.place_village(tile, corner, player.name)
                        self.agregar_construccion("pueblo",tile,corner)
                    if construction == "ciudad":
                        aldea = input(f"{player.name} escribe el id del poblado que quieres mejorar: ")
                        for v in player.piezas["pueblos"]:
                            if v.name == aldea:
                                for t in Terreno.list:
                                    for c in t.corners:
                                        if t.corners[c].id == aldea:
                                            tile = t.id
                                            corner = c
                                v.upgrade_village(self, aldea, player)
                                self.agregar_construccion("ciudad",tile,corner)
                    if construction == "carta de desarrollo":
                        player.agregar_carta_desarrollo()
                
                if action == "negociar":
                    cambio = input("vas a cambiar con un puerto, jugador o caja: ")
                    if cambio == "jugador":
                        p1= player
                        temp = input("cual es el nombre de jugador del jugador con el que quieres intercambiar: ")
                        for a in orden:
                            if a.name == temp:
                                p2 = temp
                        if p2:
                            m1 = input(f"que recurso recibe{p1.name}: ")
                            c1 = int(input(f"cuanto recibe{p1.name}: "))
                            m2 = input(f"que recurso da{p1.name} a cambio: ")
                            c2 = int(input(f"cuanto da{p1.name}: "))
                            p1.agregar_cartas(m1,c1)
                            p1.quitar_carta(m2,c2)
                            p2.agregar_cartas(m2,c2)
                            p2.quitar_carta(m1,c1)
                    if cambio == "puerto":
                        port = input("desde que terreno quieres cambiar (id): ")
                        m_in = input("que material quieres recibir: ")
                        m_out = input("que material vas a cambiar: ")
                        for t in Terreno.list:
                            if t.id == port:
                                t.trade(port,player.name,m_in,m_out)
                    if cambio == "caja":
                        m_in = input("que material quieres recibir: ")
                        m_out = input("que material vas a cambiar: ")
                        player.agregar_cartas(m_in,1)
                        player.quitar_carta(m_out,4)
                if action == "carta de desarrollo":
                    print(f"tienes {player.cartas_desarrollo['Caballero']} cartas de caballero\n "
                        f"{player.cartas_desarrollo['Invento']} cartas de invento\n "
                        f"{player.cartas_desarrollo['Monopolio']} cartas de monopolio\n "
                        f"{player.cartas_desarrollo['Punto_de_victoria']} cartas de victoria\n "
                        f"{player.cartas_desarrollo['Carreteras']} cartas de carretera")
                else:
                    print("accion no valida")
                    action = input("te gustaria construir,negociar,carta de desarrollo o pasar: ")
                action = input("te gustaria construir,negociar,carta de desarrollo o pasar: ")
            turn = (turn+1)%len(orden)   

    def seleccionar_mapa(self):
        eleccion = str(input("Elija 'cargar' o 'random': "))

        if eleccion == "random":
            Terreno.load("randomap.json")
            Puerto.load("randomap.json")
            self.generador.random("randomap.json")
            self.generador.ubicar_hexagonos()
            self.juego = Juego(self.generador.tablero) #para q funcione el tema de carreteras ciudades
            self.juego.mostrar()

        elif eleccion == "cargar":
            mapa = str(input("¿Qué mapa desea cargar?: "))           
            Terreno.load(mapa)
            Puerto.load(mapa)
            self.generador.Carga(mapa)
            self.generador.ubicar_hexagonos()
            self.juego = Juego(self.generador.tablero)
            self.juego.mostrar()

        else:
            print("Opción inválida.")

    def def_jugadores(self):
        N_jugadores = int(input("cuantos jugadores son (elija de 2 a 4):"))

        jugadores = []

        #while N_jugadores == 1:
         #   print("jugadores insuficientes")
          #  N_jugadores = int(input("cuantos jugadores son (elija de 2 a 4):"))

        for i in range(N_jugadores):
            nombre = input(f"Nombre del jugador {i + 1}: ")
            jugadores.append(Jugador(nombre))  # Añadir el jugador a la lista

        return jugadores
    
    def orden_de_juego(self, lista):
        random.shuffle(lista)
        return lista
    
    def agregar_construccion(self,tipo,tile,corner):
        if not self.juego:
            print("Debe cargar un mapa antes.")
            return

        eleccion = tipo
        if eleccion == "carretera":
            print("entre que terrenos quieres tu carretera")
            t1 = input("id del primer terreno: ")
            t2 = input("id del segundo terreno: ")
            self.juego.agregar_carretera(t1, t2)

        elif eleccion in {"pueblo", "ciudad", "ladron"}:
            id_hex = tile
            posicion = corner
            self.juego.agregar_figura(id_hex, eleccion, posicion)

        else:
            print("Opción inválida.")
            return

        self.juego.mostrar()
        self.juego.guardar_imagen("tablero_final.png")