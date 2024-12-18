import datetime, time
"""
print(datetime.date(2024, 11, 27))

print(time.localtime())

lista = time.localtime()

print("año: ", lista[0:-3])

print(datetime.datetime(lista[0], lista[1], lista[2], lista))

"""

instancia = "imagen.webp.jpg"
nombre = instancia.split(".")
cadena = "letras"
nuevo_nombre = nombre[0] + cadena
for aux in range(1, len(nombre[-2])):
    nuevo_nombre += "." + nombre[aux]
print(nuevo_nombre)