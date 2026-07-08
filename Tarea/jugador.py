import random
class Jugador:
    list = []
    mazo_desarrollo = {"Caballero":14, "Punto_de_victoria":5, "Monopolio":2, "Invento":2 , "Carreteras":2}

    def __init__(self, name: str)->None:
        self.name: str=name
        self.cartas= {} #maso de materias primas del jugador
        self.puntos=0 #puntos acumulados del jugador
        self.caballeros=0 #cantidad de cartas de caballeros del jugador
        self.carreteras_continuas=0 #cantidad de carreteras consecutivas del jugador
        #self.carreteras=0 #carreteras ganadas en cartas de desarrollo del jugador que debe colocar donde el convenga
        self.cartas_desarrollo={"Caballero":0, "Punto_de_victoria":0, "Monopolio":0, "Invento":0 , "Carreteras":0} #maso de caertas de desarrollo del jugador
        self.piezas={'caminos':[], 'pueblos':[], 'ciudades': []}
        Jugador.list.append(self)

    def get_name(self)->str:
        return self.name
    
    def get_puntos(self)->int:
        return self.puntos
    
    def get_cartas(self):
        return self.cartas
    
    def get_caballeros(self)->int:
        return self.caballeros

    def get_carreteras(self)->int:
        return self.carreteras_continuas
    
    def crear_cartas(material):
        for jug in Jugador.list:
            jug.cartas[material] = 0

    def agregar_cartas(self, material: str, cantidad: int)->None:
        self.cartas[material] += cantidad

    def quitar_carta(self, material: str, cantidad: int)->None:
        self.cartas[material] -= cantidad

    def agregar_carta_desarrollo(self)->None:
        self.quitar_carta('cereal',1)
        self.quitar_carta('mineral',1)
        self.quitar_carta('wool',1)
        cartas = []
        for i in Jugador.mazo_desarrollo:
            for card in range(Jugador.mazo_desarrollo[i]):
                cartas.append(i)
        carta=random.choice(cartas)
        self.cartas_desarrollo[carta] +=1

    def tirar_dados(self)->int:
        from terreno import Terreno
        dado1=random.randint(1,6)
        dado2=random.randint(1,6)
        numero = dado1 + dado2
        if numero==7:
            posicion=input('id del terreno para colocar el ladron:')
            self.mover_ladron(posicion)

        else:
            Terreno.produce(numero)

    def ladron(self, posicion)-> None:
        self.mover_ladron(posicion)
        self.quitar_cartas()
        return self.position
    
    def caballero(self) -> None:
        posicion = input("id de terreno para el ladron:")
        self.ladron(posicion)
        self.caballeros += 1
        self.cartas_desarrollo["caballero"] -= 1
        return(posicion)
    
    def mover_ladron(self,terreno):
        from terreno import Terreno
        terrenos = Terreno.list
        for t in terrenos:
            if t.theif:
                t.theif = False
        for T in terrenos:
            if T.id == terreno:
                T.theif = True
                a= T.id
        self.robar_cartas(terreno)
        return a
      
    def quitar_cartas(self)->None:
        for J in Jugador.list: 
            cantidad = sum(J.cartas.values())
            if cantidad >=8:
                if cantidad %2 == 0:
                    for i in range(0,1+cantidad/2):
                        carta=input('elegir material:')
                        if J.cartas[carta]>0:
                            J.quitar_carta(carta, 1)
                        else:
                            while J.cartas[carta] == 0:
                                print("material insuficiente")
                                carta=input('elegir material:')
                elif cantidad %2!=0:
                    for i in range(0,1+cantidad//2):
                        carta=input('elegir material:')
                        if J.cartas[carta]>0:
                            J.quitar_carta(carta, 1)
                        else:
                            while J.cartas[carta] == 0:
                                print("material insuficiente")
                                carta=input('elegir material:')
    
    def robar_cartas(self, posicion)->None:
        from terreno import Terreno
        opciones = []
        for terreno in Terreno.list:
            if terreno.id == posicion:
                for corner in terreno.corners.values():
                    if corner.player not in opciones:
                        opciones.append(corner.player)
        
        jug = input(f"De los siguientes, elija un jugador: {', '.join(opciones)} ")
        for p in Jugador.list:
            if p.name == jug:
                cartas = []
                for i in p.cartas:
                    for card in range(p.cartas[i]):
                        cartas.append(i)
                    
                carta=random.choice(cartas)
                p.quitar_carta(carta,1)
                print(f"conseguiste una carta de {carta}")
                self.agregar_cartas(carta,1)

    def jugar_carta_desarrollo(self)->None:
        opciones=[]
        for clave, cantidad in self.cartas_desarrollo.items():
            opciones.extend([clave] * cantidad)
        c=input(f"De las siguientes cartas, elija una para jugar: {', '.join(opciones)} ")
        acciones = {
        "Caballero": self.caballero(),
        "Punto_de_victoria": self.punto_de_victoria(),
        "Monopolio": self.monopolio(),
        "Invento": self.invento(),
        "Carreteras": self.carreteras()
        }
        accion=acciones.get(c)
        if accion:
            accion()

    def mayor_ejercito(self)->None:
        for j in Jugador.list:
            if j.caballeros <= self.caballeros and self.caballeros >= 3:
                if self.m_ejercito==False:
                    self.m_ejercito=True
                    self.puntos+=2
                else:
                    self.m_ejercito=True
            elif j.caballeros > self.caballeros and self.m_ejercito==True:
                self.puntos-=2
                self.m_ejercito=False
 
    def carreteras(self)->None:
        self.agregar_cartas('wood',2)
        self.agregar_cartas('clay',2)
        print("materiales recibidos")
        self.cartas_desarrollo["Carreterras"]-=1

    def invento(self)->None:
        material1=str(input('material a elegir "wool", "wood", "clay", "mineral" y "cereal": '))
        material2=str(input('material a elegir "wool", "wood", "clay", "mineral" y "cereal": '))
        self.agregar_cartas(material1,1)
        self.agregar_cartas(material2,1)
        self.cartas_desarrollo["Invento"]-=1
       
    def monopolio(self)->None:
        material=str(input('material a elegir "wool", "wood", "clay", "mineral" y "cereal": '))
        cantidad=0
        for j in Jugador.list:
            if j is not self and j.cartas[material]>=1:
                i=j.cartas[material]
                cantidad+=i
                j.quitar_carta(material, i)
        self.agregar_cartas(material, cantidad)
        self.cartas_desarrollo["Monopolio"]-=1

    def punto_de_victoria(self)->None:
        self.puntos+=1
        self.cartas_desarrollo["Punto_de_victoria"]-=1