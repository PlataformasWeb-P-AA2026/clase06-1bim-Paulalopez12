import csv
import os
from base_datos import conn

# Se usa el objeto Connection y se accede al método cursor
cursor = conn.cursor()

# Asegurar que exista la tabla antes de operar
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Autor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        cedula TEXT,
        edad INTEGER
    )
    """
)
conn.commit()

# ------------------------------------------------------------------
# Obtener la ruta absoluta del archivo info.csv
# ------------------------------------------------------------------
# __file__ = ruta del archivo actual (guardardb.py)
# dirname(__file__) = carpeta donde está guardardb.py
# join(...) = construir la ruta correcta al archivo CSV

ruta_actual = os.path.dirname(__file__)

# El CSV está en ejemplo0/data/info.csv (misma carpeta que este script)
ruta_csv = os.path.join(ruta_actual, "info.csv")

# Abrir el archivo CSV
archivo = open(ruta_csv, "r", encoding="utf-8")

# Crear lector CSV
lector = csv.reader(archivo)

# Saltar la primera fila (encabezados)
next(lector, None)

# Recorrer cada fila del archivo CSV
for linea in lector:
    # Se asume el siguiente orden en el CSV:
    # nombre, apellido, cedula, edad

    nombre = linea[0]
    apellido = linea[1]
    cedula = linea[2]
    edad = int(linea[3])

    # Crear la sentencia SQL
    cadena_sql = """INSERT INTO Autor (nombre, apellido, cedula, edad) \
VALUES ('%s', '%s', '%s', %d);""" % (
        nombre,
        apellido,
        cedula,
        edad
    )

    # Ejecutar el SQL
    cursor.execute(cadena_sql)

# Confirmar los cambios
conn.commit()

# ------------------------------------------------------------------
# Consultar los datos almacenados
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("LEYENDO DATOS DE LA BASE DE DATOS")
print("=" * 60 + "\n")

cadena_consulta_sql = "SELECT * from Autor"
cursor.execute(cadena_consulta_sql)

informacion = cursor.fetchall()

print(f"Total de registros: {len(informacion)}\n")
print(f"{'ID':<5} {'NOMBRE':<20} {'APELLIDO':<20} {'CEDULA':<15} {'EDAD':<5}")
print("-" * 65)

for d in informacion:
    print(f"{d[0]:<5} {d[1]:<20} {d[2]:<20} {d[3]:<15} {d[4]:<5}")

print("-" * 65)

# Cerrar archivo y cursor
archivo.close()
cursor.close()

print("\n¡Proceso completado exitosamente!")