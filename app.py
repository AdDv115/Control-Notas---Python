from flask import Flask, render_template, request, redirect, session, send_file
from database import obtenerusuarios
from dashprincipal import creartablero
from database import insertarEst, conectar, existe_estudiante, obtener_claves_estudiantes
import pandas as pd
import os
import tempfile
import time
import uuid

app = Flask(__name__)


#Clave Session
app.secret_key = "115"

creartablero(app)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response


@app.route("/", methods = ["GET","POST"])
def login():
    
    #Verificar si el formulario fue enviado
    if request.method == "POST":
        
        #Capturar los datos del formulario
        username = request.form["usern"]
        password = request.form["pass"]
        
        usuario = obtenerusuarios(username)
        
        #Verificar si existe el usuario
        if usuario:
            
            if usuario["password"] == password:
                
                #Crea la sesion del usuario
                session["username"] = usuario["username"]
                session["rolusu"] = usuario["rolusu"]
                                
                return redirect("/dashp/")
            
            else:
                return "Contraseña Incorrecta"
            
        else:
            return "Usuario no existe" 
    
    return render_template("login.html")

@app.route("/dashp/")
def dashp():
    if "username" not in session:
        
        return redirect("/")

    return render_template(
        "dashpi.html",
        usuario=session["username"],
        resumen_cargue=session.pop("resumen_cargue", None),
        archivo_rechazados=bool(session.get("rechazados_path")),
        marca_tiempo=int(time.time())
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/regest", methods=["GET","POST"])
def regEst():
    if "username" not in session:
        return redirect("/")
    
    if request.method == "POST":
        
        Nombre = normalizar_texto(request.form["nom"])
        Edad = request.form["edad"]
        Carrera = normalizar_texto(request.form["carrera"])
        Nota1 = float(request.form["n1"])
        Nota2 = float(request.form["n2"])
        Nota3 = float(request.form["n3"])

        if existe_estudiante(Nombre, Carrera):
            return render_template("registro.html", mensaje="El estudiante ya está registrado.", tipo_mensaje="error")
        
        Promedio = round((Nota1 + Nota2 + Nota3)/3, 2)
    
        Desempeño = calculardesempeño(Promedio)
        
        insertarEst(Nombre, Edad, Carrera, Nota1, Nota2, Nota3, Promedio, Desempeño)
        
        return redirect("/dashp/")
    
    return render_template("registro.html")

# Funciones auxiliares
def quitar(texto):
    acentos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"
    }
    for acento, sin_acento in acentos.items():
        texto = texto.replace(acento, sin_acento)
    return texto


def normalizar_texto(texto):
    texto = str(texto).strip()
    texto = quitar(texto)
    return texto.title()


def convertir_numero(valor):
    if pd.isna(valor):
        return None

    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def formatear_rechazado(valor):
    if pd.isna(valor):
        return ""
    return valor

def calculardesempeño(promedio):
    if promedio >= 4.5: return "Excelente"
    elif promedio >= 4: return "Bueno"
    elif promedio >= 3: return "Regular"
    return "Bajo"


@app.route("/cg", methods=["GET", "POST"])
def cargar():
    if "username" not in session:
        return redirect("/")
        
    if request.method == "POST":
        archivo = request.files["archivo"]

        df = pd.read_excel(archivo)
        columnas_requeridas = ["Nombre", "Edad", "Carrera", "Nota1", "Nota2", "Nota3"]
        faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]

        if faltantes:
            mensaje = "El archivo no contiene las columnas requeridas: " + ", ".join(faltantes)
            return render_template("carga_masiva.html", mensaje=mensaje, tipo_mensaje="error")

        rechazados = []
        estudiantes_validos = []
        duplicados = 0
        claves_existentes = obtener_claves_estudiantes()
        claves_archivo = set()

        for _, fila in df.iterrows():
            nombre_limpio = normalizar_texto(fila["Nombre"]) if not pd.isna(fila["Nombre"]) else ""
            carrera_limpia = normalizar_texto(fila["Carrera"]) if not pd.isna(fila["Carrera"]) else ""
            edad = convertir_numero(fila["Edad"])
            nota1 = convertir_numero(fila["Nota1"])
            nota2 = convertir_numero(fila["Nota2"])
            nota3 = convertir_numero(fila["Nota3"])

            motivos = []

            if not nombre_limpio or not carrera_limpia or None in [edad, nota1, nota2, nota3]:
                motivos.append("Datos faltantes")

            if edad is not None and edad < 0:
                motivos.append("Edad negativa")

            notas = [nota for nota in [nota1, nota2, nota3] if nota is not None]
            if notas and any(nota < 0 or nota > 5 for nota in notas):
                motivos.append("Notas invalidas")

            clave_estudiante = (nombre_limpio, carrera_limpia)
            if nombre_limpio and carrera_limpia and (clave_estudiante in claves_existentes or clave_estudiante in claves_archivo):
                motivos.append("Estudiante duplicado")
                duplicados += 1

            if motivos:
                rechazados.append({
                    "Nombre": nombre_limpio or formatear_rechazado(fila["Nombre"]),
                    "Edad": formatear_rechazado(fila["Edad"]),
                    "Carrera": carrera_limpia or formatear_rechazado(fila["Carrera"]),
                    "Nota1": formatear_rechazado(fila["Nota1"]),
                    "Nota2": formatear_rechazado(fila["Nota2"]),
                    "Nota3": formatear_rechazado(fila["Nota3"]),
                    "Motivo": ", ".join(dict.fromkeys(motivos))
                })
                continue

            promedio = round((nota1 + nota2 + nota3) / 3, 2)
            desempeño = calculardesempeño(promedio)

            estudiantes_validos.append((
                nombre_limpio,
                int(edad) if float(edad).is_integer() else edad,
                carrera_limpia,
                nota1,
                nota2,
                nota3,
                promedio,
                desempeño
            ))
            claves_archivo.add(clave_estudiante)

        #Insertar en la base de datos
        conn = conectar()
        cursor = conn.cursor()
        
        query = """INSERT INTO Estudiantes(Nombre,Edad,Carrera,nota1,nota2,nota3,Promedio,Desempeño) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        for estudiante in estudiantes_validos:
            cursor.execute(query, estudiante)
            
        conn.commit()
        conn.close()

        if session.get("rechazados_path") and os.path.exists(session["rechazados_path"]):
            os.remove(session["rechazados_path"])
            session.pop("rechazados_path", None)

        if rechazados:
            nombre_archivo = f"rechazados_{uuid.uuid4().hex[:8]}.xlsx"
            ruta_archivo = os.path.join(tempfile.gettempdir(), nombre_archivo)
            pd.DataFrame(rechazados).to_excel(ruta_archivo, index=False)
            session["rechazados_path"] = ruta_archivo
        else:
            session.pop("rechazados_path", None)

        session["resumen_cargue"] = {
            "insertados": len(estudiantes_validos),
            "rechazados": len(rechazados),
            "duplicados": duplicados
        }

        return redirect("/dashp/")
    
    return render_template("carga_masiva.html")


@app.route("/descargar-rechazados")
def descargar_rechazados():
    if "username" not in session:
        return redirect("/")

    ruta_archivo = session.get("rechazados_path")
    if not ruta_archivo or not os.path.exists(ruta_archivo):
        return redirect("/dashp/")

    return send_file(ruta_archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
