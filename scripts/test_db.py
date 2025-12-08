#!/usr/bin/env python <-- Aquí se especifica el intérprete de Python - shebang

#Documentacion del script - docstring
"""
test_db.py - Test PostgreSQL connection for Django project #Probamos conexión a PostgreSQL

Usage: #Como usar

    From project root: python scripts/test_db.py #desde la raíz del proyecto
    From scripts folder: python test_db.py #desde la carpeta scripts
"""
import os #Manejo de rutas y variables de entorno
import sys #Manipulación del sistema
import psycopg2 #Conexión a PostgreSQL
from datetime import datetime #Registro de Fecha/Hora

#Función principal de prueba de conexión a la DB
def test_postgresql_connection():
    """Test connection to PostgreSQL database using settings from Django project."""
    
    print("Probando conexión a PostgreSQL...") #Inicio
    print(f"Base de datos: {DB_CONFIG['dbname']}") #Apuntamos a la base de datos
    print(f"Usuario: {DB_CONFIG['user']}") #Usuario
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}") #Servidor (host y puerto - por estandar van juntos)

    #Manejo de errores
    try:
        #intentamos conectar
        conn = psycopg2.connect(**DB_CONFIG)

        #Si la conexión es exitosa
        cursor = conn.cursor() #Creamos cursor para ejecutar los comandos SQL
        cursor.execute("SELECT version(), current_database(), current_user;")  #Consultamos versión, base de datos y usuario

        version, db_name, db_user = cursor.fetchone() #Asigna cada columna a una variable y con fetchone se obtiene una linea de resultados.
        print("Conexión exitosa a PostgreSQL!")
        print(f"Versión de PostgreSQL: {version.split()[0]}") #Mostramos versión
        print(f"Base de datos: {db_name}") #Mostramos base de datos
        print(f"Usuario: {db_user}") #Mostramos usuario
        print(f"Hora de conexión al servidor: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") #Mostramos hora de conexión      
        #Se recomienda el uso de formato completo de fecha y hora para logs y depuración

        #Prueba de consulta simple: Ejecutar SELECT 1
        cursor.execute("SELECT 1 AS test_value")
        test_result = cursor.fetchone()[0]
        print(f"Prueba de consulta exitosa, valor retornado: {test_result}")

        #cerramos cursor y conexión
        cursor.close()
        conn.close()
        return True

        #Manejo de errores de conexión
    except psycopg2.OperationalError as e:
        print("Error de conexión a PostgreSQL:")
        print("\nEste error puede deberse a:")
        print("\nPostgreSQL no se está ejecutando correctamente.")
        print("\nLa configuración de conexión es incorrecta.")
        print("\nEl puerto o host son incorrectos.")
        print("\nLas credenciales de usuario son incorrectas.")
        print(f"\nDetalles del error: {e}")
        return False
    
    except Exception as e:
        print(f"Ocurrió un error inesperado {e}")
        return False
        

if __name__ == "__main__":
    # Configuración de conexión a PostgreSQL desde settings.py
    DB_CONFIG = {
        'dbname': 'castor_db',      # Nombre de mi BD
        'user': 'castor_user',      # Usuario de PostgreSQL
        'password': 'castor123',    # Contraseña
        'host': 'localhost',        # Host
        'port': '5432'              # Puerto de PostgreSQL
    }
    
    print("=" * 50) #Cadena de separación para estandarización visual
    print("TEST DE CONEXIÓN A POSTGRESQL")
    print("=" * 50) #Cadena de separación para estandarización visual
    
    result = test_postgresql_connection() #Llamamos a nuestra función de prueba DB
    
    if result:
        print("\n¡Prueba exitosa!")
        sys.exit(0)  #0 = éxito
    else:
        print("\n ¡Prueba fallida!")
        sys.exit(1)  #1 = error


