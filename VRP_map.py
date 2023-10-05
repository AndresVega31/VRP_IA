# biblioteca para crear mapas iterativos
import folium 
from folium import plugins
from AlgoritmoGenetico import Rutas

#------------------------------------------------------------------------------------------------#
#  ABRIR EL ARCHIVO HTML GENERADO LUEGO DE CORRER ESTE CODIGO                                    #
#------------------------------------------------------------------------------------------------#

#Estas coordenadas representan la ubicación geográfica de cada ciudad en términos de su latitud
# (norte o sur) y longitud (este u oeste) en grados decimales.

# Lista de ciudades y sus coordenadas
ciudades = {
    "Bogota": [4.609710, -74.081749],
    "Tunja": [5.535400, -73.367592],
    "Sogamoso": [5.714777, -72.932911],
    "Yopal": [5.337752, -72.394731],
    "Villavicencio": [4.142438, -73.626204],
    "Medellin": [6.244203, -75.581214],
    "Villeta": [5.010957, -74.377634],
    "Manizales": [5.067825, -75.517953],
    "Pereira": [4.808717, -75.690601],
    "Ibague": [4.437301, -75.234447],
    "Neiva": [2.936020, -75.290469],
    "Cali": [3.451647, -76.532051],
    "Bucaramanga": [7.119349, -73.122742],
    "Villanueva": [4.097080, -73.244429],
    "Soacha": [4.579590, -74.207425],
    "Ituango": [7.166107, -75.990775]
}

# Crear un mapa centrado en Bogotá
mapa = folium.Map(location=[4.609710, -74.081749], zoom_start=6)

# Agregar marcador para Bogotá con un color diferente
folium.Marker(
    location=ciudades["Bogota"],
    tooltip="Bogota",
    icon=folium.Icon(color="red")  # Color rojo para el marcador de Bogotá
).add_to(mapa)

# Agregar marcadores para las demás ciudades
for ciudad, coords in ciudades.items():
    if ciudad != "Bogota":
        folium.Marker(coords, tooltip=ciudad).add_to(mapa)


Sol = list(Rutas)

# Organiza las rutas para empezar y terminar en bogota
for i in range(3):
    Sol[i] = ["Bogota"] + Sol[i] + ["Bogota"]
    
#funcion para trazar diferentes rutas
def trazar_ruta(ciudades_ordenadas, color):
    coordenadas_ruta = [ciudades[ciudad] for ciudad in ciudades_ordenadas]
    folium.PolyLine(coordenadas_ruta, color=color).add_to(mapa)
    
    # Agregar flechas a la ruta
    if len(coordenadas_ruta) > 1:
        plugins.AntPath(
            locations=coordenadas_ruta,
            dash_array=[10, 20],
            delay=800,
            color=color
        ).add_to(mapa)
        
#Traza cada ruta con un color diferente
trazar_ruta(Sol[0],"blue")
trazar_ruta(Sol[1],"red")
trazar_ruta(Sol[2],"purple")

# Mostrar el mapa
mapa.save("ruta_mapa.html")  # Guardar como archivo HTML
mapa

#------------------------------------------------------------------------------------------------#
#  ABRIR EL ARCHIVO HTML GENERADO LUEGO DE CORRER ESTE CODIGO                                    #
#------------------------------------------------------------------------------------------------#