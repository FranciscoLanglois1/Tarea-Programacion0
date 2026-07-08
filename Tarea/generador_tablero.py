from tablero import Tablero
from load import Load
import random

class GeneradorTablero:
    def __init__(self) -> None:
        self.tablero = Tablero(7, 7)
        self.L: Load = Load() #para poder usar algunas funciones de load 

        self.Centro: list = [ ] 

        self.sectores = []
        self.puertos = []
        self.desierto = None

        #en las coordenadas estoy a prueba y error, por alguna razon quedaron al reves, pero funcionan
        #osea, en la demostracion de abajo estan en orden numerico, por eso se ve tan desastroso 
        
        self.coordenadas_sectores = [
                            (1,0), (2,0), (3,0),
                        (0,1), (1,1), (2,1), (3,1),
                    (0,2), (1,2)        , (3,2), (4,2),            
                        (0,3), (1,3), (2,3), (3,3),
                           (1,4), (2,4), (3,4)                        
        ]
        
        #FUNCIONARON LESGOOOOOOOOOOOOOOOOOOOOOOO
        self.coordenadas_puertos = random.choice([
            [(1,-1),(3,-1), (0,0), (4,1), (-1,2), (4,3), (0,4),(3,5), (1,5)],  
            [(0,-1),(2,-1), (-1,1), (4,0), (-1,3), (5,2), (0,5),(4,4),(2,5)]
        ])
        
    def Carga(self, json_path: str) -> None:
        L=self.L #para simplificar el "comando"
        L.load(json_path) #carga del json
        self.sectores = L.sectores #para crear una copia de las listas q se crean en load y aplicarlas en el mapa
        self.puertos = L.puertos
        self.desierto = L.desierto
        if L.mapa == 1:
            self.coordenadas_puertos =  [ #primer mapa
                (0,-1), #p01 top left

                (2,-1), #p02 top rigth

                (-1,1), #p08 bottom right

                (4,0),  #p09 bottom left

                (5,2),  #p03 left

                (-1,3), #p04 top right

                (4,4),  #p05 right

                (0,5),  #p06 left

                (2,5)]  #p07 bottom right
        
        elif L.mapa == 2:
            self.coordenadas_puertos = [ #segundo mapa
                (1,-1), 

                (3,-1), 

                (0,0), 

                (4,1), 

                (-1,2),

                (4,3), 

                (0,4),

                (3,5), 

                (1,5)]

        else:
            print("hay un error al portar el mapa")
            exit()

    def random(self, json_path: str) -> None:

        L=self.L #para simplificar el "comando"
        L.load(json_path) #carga del json
        self.sectores = L.sectores #para crear una copia de las listas q se crean en load y aplicarlas en el mapa
        self.puertos = L.puertos
        self.desierto = L.desierto

        random.shuffle(self.sectores) #para hacer q sea aleatorio
        random.shuffle(self.puertos)


    def ubicar_hexagonos(self) -> None:
        from terreno import Terreno
        from puerto import Puerto
        self.tablero.agregar_hexagono(2, 2, self.desierto, "desierto")

        for (columna, fila), sector in zip(self.coordenadas_sectores, self.sectores):  #sect
            for i in Terreno.list:
                if sector == i.id:
                    self.tablero.agregar_hexagono(columna, fila, sector, i.material, str(i.num))
            

        for (col, fila), puerto in zip(self.coordenadas_puertos, self.puertos):  #puertos
            for i in Puerto.list:
                if puerto == i.id:  
                    self.tablero.agregar_hexagono(col, fila, puerto, i.material)

    def mostrar(self) -> None:
        self.tablero.mostrar()
        

#l= Load()
#l.load("mapa1.json")  
#print(l.mapa)         #para comprobar q se esta cargando el mapa correcto
