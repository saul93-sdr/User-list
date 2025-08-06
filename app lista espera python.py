import streamlit as st
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "usuarios.json"

# Inicializa el archivo si no existe
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Cargar datos de usuarios
def cargar_datos():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Guardar datos de usuarios
def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Quitar sesiones pasadas
def limpiar_sesiones_pasadas(data):
    ahora = datetime.now()
    for usuario in data:
        sesiones = data[usuario]["sesiones"]
        futuras = [s for s in sesiones if datetime.fromisoformat(s) > ahora]
        data[usuario]["sesiones"] = futuras
    return data

# Reservar sesión
def reservar_sesion(data, nombre, nueva_fecha):
    if nombre not in data:
        data[nombre] = {"sesiones": []}
    data = limpiar_sesiones_pasadas(data)
    if len(data[nombre]["sesiones"]) < 2:
        data[nombre]["sesiones"].append(nueva_fecha.isoformat())
        guardar_datos(data)
        st.success(f"Sesión reservada para {nueva_fecha.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.error("¡Has alcanzado el máximo de 2 sesiones activas!")
    return data

# Interfaz de Streamlit
st.title("📋 Lista de espera de sesiones")

# Cargar y limpiar datos
data = cargar_datos()
data = limpiar_sesiones_pasadas(data)
guardar_datos(data)

# Formulario para registrarse o iniciar sesión
nombre = st.text_input("Tu nombre:")

if nombre:
    st.subheader(f"Hola, {nombre} 👋")

    # Mostrar sesiones activas del usuario
    sesiones_propias = data.get(nombre, {}).get("sesiones", [])
    if sesiones_propias:
        st.write("Tus sesiones activas:")
        for s in sesiones_propias:
            st.write(f"🕒 {datetime.fromisoformat(s).strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("No tienes sesiones activas.")

    # Reservar nueva sesión
    if len(sesiones_propias) < 2:
        fecha = st.date_input("Selecciona la fecha")
        hora = st.time_input("Selecciona la hora")
        nueva_fecha = datetime.combine(fecha, hora)
        if st.button("Reservar sesión"):
            data = reservar_sesion(data, nombre, nueva_fecha)
    else:
        st.warning("Solo puedes tener 2 sesiones activas a la vez.")

    st.markdown("---")

# Mostrar todos los usuarios y sus sesiones
st.subheader("📑 Lista completa de usuarios")
for usuario, info in data.items():
    st.write(f"**{usuario}**:")
    for s in info["sesiones"]:
        st.write(f"🔹 {datetime.fromisoformat(s).strftime('%Y-%m-%d %H:%M')}")

