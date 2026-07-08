import json

class Load:
    def __init__(self) -> None :
        self.sectores: list= []
        self.puertos: list= []
        self.desierto: list= [] 

        self.puertos_br=[]
        self.puertos_bl=[]
        self.puertos_tl=[]
        self.puertos_tr=[]
        self.puertos_l=[]
        self.puertos_r=[]

        self.mapa: int = int

        
    def load(self, filename: str) -> None:
        with open(filename, 'r') as f:
            data = json.load(f)
            for t in data["tiles"]:
                if t["material"] == "desert":  #le cambie a materiales para q coincidan con los otros mapas
                    self.desierto=(t["id"])  #pero de momento lo mantengo mostrando el id para reconocer la casilla
                    
                else:    
                    Sector=(t["id"])  #lo mismo para aca, este se debe cambiar por material para que printee material
                                                                 
                    self.sectores.append(Sector)
            #----------------------------------------------- ahora vienen los puertos

                puertobr = t["edges"].get("bottom-right") #para obtener solo los valores de abajo a la derecha
                puertobl = t["edges"].get("bottom-left") #para obtener solo los valores de abajo a la izquierda
                puertotl = t["edges"].get("top-left") #para obtener solo los valores de arriba a la izquierda
                puertotr = t["edges"].get("top-right") #para obtener solo los valores de arriba a la derecha
                puertol = t["edges"].get("left") #para obtener solo los valores de la izquierda
                puertor = t["edges"].get("right") #para obtener solo los valores de la derecha
                
                if str(puertobr).startswith("p"):  #el startswith es literal como dice, busca el valor que inicie con la letra p
                    self.puertos_br.append(puertobr)

                if str(puertobl).startswith("p"):
                    self.puertos_bl.append(puertobl)

                if str(puertotl).startswith("p"):
                    self.puertos_tl.append(puertotl)

                if str(puertotr).startswith("p"):
                    self.puertos_tr.append(puertotr)

                if str(puertol).startswith("p"):
                    self.puertos_l.append(puertol)

                if str(puertor).startswith("p"):
                    self.puertos_r.append(puertor)

            if len(self.puertos_tl) == 0: #para detectar que es del segundo mapa
                self.mapa= 2
                #print("es el segundo mapa") 
                self.puertos.extend([ 
                    self.puertos_tr[0], 

                    self.puertos_tr[1], 

                    self.puertos_tr[2],

                    self.puertos_br[0], 

                    self.puertos_bl[0], 

                    self.puertos_l[0],  

                    self.puertos_l[1], 

                    self.puertos_r[0], 

                    self.puertos_r[1]
                ]) 
                              
                
                    
            if len(self.puertos_tl) == 1:  #para detectar q es del primer mapa
                self.mapa= 1

                #print("es el primer mapa")
                self.puertos.extend([
                    self.puertos_tl[0], #p01

                    self.puertos_tr[0], #p02

                    self.puertos_l[0], #p03

                    self.puertos_tr[1], #p04

                    self.puertos_r[0], #p05

                    self.puertos_l[1], #p06

                    self.puertos_br[0], #p07

                    self.puertos_bl[0], #p09

                    self.puertos_br[1] #p08     
                ])

                



            

