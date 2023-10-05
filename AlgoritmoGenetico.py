import random
import time

#------------------------------------------------------------------------------------------------#
#  CORRER EL CODIGO VRP_map PARA GENERAR ARCHIVO HTML PARA VISUALIZAR LAS RUTAS                  #
#------------------------------------------------------------------------------------------------#

start = time.time()

#Vector con valores de "Demanda" de cierto producto, en Toneladas, ordenadas por ciudad.
demanda = (0, 2, 5, 5, 4, 3, 2, 4, 5, 3, 3, 4, 5, 3, 3, 5)

cities = (
    "Bogota", "Tunja", "Sogamoso", "Yopal", "Villavicencio",
    "Medellin", "Villeta", "Manizales", "Pereira", "Ibague",
    "Neiva", "Cali", "Bucaramanga", "Villanueva", "Soacha", "Ituango"
)

#Diccionario para calcular distancias entre ciudades
distancias = {
    "Bogota": (0, 129, 192, 265, 90, 426, 95, 292, 249, 216, 303, 343, 309, 13, 22, 23),
    "Tunja": (129, 0, 63, 174, 104, 370, 112, 176, 224, 87, 174, 274, 295, 143, 115, 114),
    "Sogamoso": (192, 63, 0, 111, 161, 369, 168, 171, 250, 149, 190, 267, 276, 206, 169, 157),
    "Yopal": (265, 174, 111, 0, 250, 472, 251, 332, 411, 261, 316, 337, 381, 256, 259, 255),
    "Villavicencio": (90, 104, 161, 250, 0, 537, 110, 372, 269, 90, 233, 117, 446, 205, 63, 97),
    "Medellin": (426, 370, 369, 472, 537, 0, 429, 193, 317, 438, 536, 420, 140, 422, 442, 415),
    "Villeta": (95, 112, 168, 251, 110, 429, 0, 261, 164, 118, 213, 70, 353, 139, 73, 28),
    "Manizales": (292, 176, 171, 332, 372, 193, 261, 0, 126, 295, 368, 215, 256, 276, 326, 299),
    "Pereira": (249, 224, 250, 411, 269, 317, 164, 126, 0, 188, 281, 157, 392, 216, 92, 98),
    "Ibague": (216, 87, 149, 261, 90, 438, 118, 295, 188, 0, 116, 262, 330, 159, 127, 117),
    "Neiva": (303, 174, 190, 316, 233, 536, 213, 368, 281, 116, 0, 383, 396, 248, 216, 232),
    "Cali": (343, 274, 267, 337, 117, 420, 70, 215, 157, 262, 383, 0, 477, 144, 127, 88),
    "Bucaramanga": (309, 295, 276, 381, 446, 140, 353, 256, 392, 330, 396, 477, 0, 359, 442, 413),
    "Villanueva": (13, 143, 206, 256, 205, 422, 139, 276, 216, 159, 248, 144, 359, 0, 134, 126),
    "Soacha": (22, 115, 169, 259, 63, 442, 73, 326, 92, 127, 216, 127, 442, 134, 0, 42),
    "Ituango": (23, 114, 157, 255, 97, 415, 28, 299, 98, 117, 232, 88, 413, 126, 42, 0)
}

def calcular_distancias(ruta):
    #Suma de todas las distancias en el recorrido
    distancia = 0
    
    #Almacena la posicion de la ciudad destino
    destino = cities.index(ruta[0])
    #Suma la distancia desde mi posicion hasta el destino
    distancia += distancias["Bogota"][destino]
    
    for i in range(len(ruta)):
        #Calcula la distancia desde la ultima ciudad hasta bogota
        if i == (len(ruta)-1):
            distancia += distancias[ruta[i]][0]
        #Suma las distancias de una ciudad a otra
        else:                                          
            destino = cities.index(ruta[i+1])         
            distancia += distancias[ruta[i]][destino]
            
    return distancia

#Me indica que tan buena es mi solucion
def fitness(genoma):
    ganancia = 0
    #calcula la ganancia de cada ruta dentro del genoma
    for ruta in genoma:
        #Inicializo variable para contar toneladas totales que entrega cada camion
        entregas = 0
        #Se añade una medida que tiene en cuenta la distancia para ajustar el fitness
        distancia = 1000/calcular_distancias(ruta)
        
        #Itera por todas las ciudades de la ruta y suma todas las entregas
        for i in range(len(ruta)):
            posicion = cities.index(ruta[i])
            entregas += demanda[posicion]
        #Restricciones del problema
        if 15 > entregas <= 20:
            ganancia += entregas * 5 * distancia
        elif entregas > 20:
            ganancia += entregas * 5 * distancia - (entregas - 20) * 2
        else:
            ganancia += entregas * 5/2 * distancia
    return ganancia

#Funcion utilizada para crear la poblacion inicial
def iniciar_genoma():
    #Crea una liesta copiando la tupla cities
    citiesCopy = list(cities[1:16])
    random.shuffle(citiesCopy)
    ruta1 = list(citiesCopy[0:5])
    ruta2 = list(citiesCopy[5:10])
    ruta3 = list(citiesCopy[10:15])
    solucion = (ruta1,ruta2,ruta3)
    return solucion

#Funcion de mutacion utilizada para crear nueva generacion
def mutacion(padre):
    hijo = list(padre)
    for _ in range(random.randint(1,4)):
        ruta_a = random.randint(0,2)
        ciudad_a = random.randint(0,4)
        ruta_b = random.randint(0,2)
        ciudad_b = random.randint(0,4)
        hijo[ruta_a][ciudad_a] , hijo[ruta_b][ciudad_b] = hijo[ruta_b][ciudad_b] , hijo[ruta_a][ciudad_a]
    hijo = tuple(hijo)
    return hijo


solutions = []
for s in range(1000):
    #Aqui generas toda la poblacion
    solutions.append(iniciar_genoma())

for i in range(100):
    rankedSolutions = []
    
    for s in solutions:
        rankedSolutions.append( (fitness(s),s) )
        rankedSolutions.sort()
        rankedSolutions.reverse()
        
    print(f"=== Gen {i} best solutions === ")
    print(rankedSolutions[0][0])
    print(rankedSolutions[999][0])
    
    #Rompe el for cuando encuentra una solucion con un fitness mayor de cierto valor
    if rankedSolutions [0][0] > 300:
        print("Se llego a un valor de: ", rankedSolutions [0][0], " de funcionalidad")
        break
    
    #selecciona las mejores soluciones
    bestSolutions = rankedSolutions[:100]
    
    #Extrae solo las rutas de bestSolutions
    padres = []
    for s in bestSolutions:
        padres.append(s[1])
    
    #Muta muchas veces las mejores soluciones de manera aleatoria, cambiando solo aquellas que son mutadas en las siguiente generacion
    #Las peores soluciones permanecen igual
    for _ in range(1000):
        mutacion(random.choice(padres))

#Se guarda la ultima ruta, o la primera ruta encontrada que supere un fitness de 300
Rutas = rankedSolutions[0][1]
print(Rutas)

end = time.time() 

#Imprime el tiempo tomado para encontrar una solucion: 
print("El algoritmo demoro: ",end-start, " segundos")

#------------------------------------------------------------------------------------------------#
#  CORRER EL CODIGO VRP_map PARA GENERAR ARCHIVO HTML PARA VISUALIZAR LAS RUTAS                  #
#------------------------------------------------------------------------------------------------#