import mysql.connector
import pandas as pd

def conectar():
    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "web"
    )
    
    return conexion


def obtenerusuarios(username):
    
    #Conectar con la base de datos
        coon = conectar()
        cursor = coon.cursor(dictionary=True)   
        
        #buscar el usuario en la base de datos
        cursor.execute("SELECT * FROM Usuarios WHERE username=%s", (username,))
        usuario = cursor.fetchone()
        coon.close()
        
        return usuario

#Obtener estudiantes
def obtenerestudiantes():
    
    coon = conectar()
    query = "SELECT * FROM Estudiantes"
    df = pd.read_sql(query,coon)
    coon.close()
    
    return df

#Registrar estudiantes
def insertarEst(Nombre, Edad, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeño):
    coon = conectar()
    cursor = coon.cursor()
    
    query = """INSERT INTO Estudiantes(Nombre, Edad, Carrera, nota1, nota2, nota3, Promedio, Desempeño) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(query,(Nombre, Edad, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeño))
    coon.commit()
    coon.close()


def existe_estudiante(nombre, carrera):
    coon = conectar()
    cursor = coon.cursor()

    query = """SELECT 1 FROM Estudiantes WHERE Nombre = %s AND Carrera = %s LIMIT 1"""
    cursor.execute(query, (nombre, carrera))
    existe = cursor.fetchone() is not None
    coon.close()

    return existe


def obtener_claves_estudiantes():
    coon = conectar()
    cursor = coon.cursor()

    cursor.execute("SELECT Nombre, Carrera FROM Estudiantes")
    claves = {(nombre, carrera) for nombre, carrera in cursor.fetchall()}
    coon.close()

    return claves
    
if __name__ == "__main__":
    
    coon = conectar()
    print("Conexion exitosa")
    coon.close()
