import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import obtener_clima, traducir_codigo_clima

st.set_page_config(page_title="Consulta de Meteorología en Tiempo Real-Fabricio Beltrand")

st.title("🌤️ Consulta de Meteorología en Tiempo Real")
st.write("Aplicación interactiva que consume la API pública de **Open-Meteo**.")

CIUDADES = {
    "Siguatepeque, Honduras": {"lat": 14.5933, "lon": -87.8333},
    "Tegucigalpa, Honduras": {"lat": 14.0818, "lon": -87.2068},
    "San Pedro Sula, Honduras": {"lat": 15.5042, "lon": -88.0250},
    "La Ceiba, Honduras": {"lat": 15.7597, "lon": -86.7915},
    "Comayagua, Honduras": {"lat": 14.4614, "lon": -87.6375},
    "choluteca, Honduras": {"lat": 13.3000, "lon": -87.1833},
    "Puerto Cortés, Honduras": {"lat": 15.9000, "lon": -87.9500},
}

ciudad_seleccionada = st.selectbox("Selecciona una ciudad para consultar el clima:", list(CIUDADES.keys()))
coordenadas = CIUDADES[ciudad_seleccionada]

if coordenadas:
    with st.spinner("Cargando datos meteorológicos..."):
        datos_clima = obtener_clima(coordenadas["lat"], coordenadas["lon"])
    
    if datos_clima and "current_weather" in datos_clima:
        clima_actual = datos_clima["current_weather"]
        
        temperatura = clima_actual["temperature"]
        velocidad_viento = clima_actual["windspeed"]
        codigo_clima = clima_actual["weathercode"]
        estado_clima = traducir_codigo_clima(codigo_clima)
        hora_lectura = clima_actual["time"]
        
        st.subheader(f"Clima actual en {ciudad_seleccionada}")
        st.markdown(f"**Condición actual:** {estado_clima}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Temperatura", value=f"{temperatura} °C")
        with col2:
            st.metric(label="Velocidad del Viento", value=f"{velocidad_viento} km/h")
            
        st.markdown("### Resumen técnico de coordenadas")
        df_coordenadas = pd.DataFrame({
            "Parámetro": ["Latitud", "Longitud", "Zona Horaria", "Última Actualización API"],
            "Valor": [coordenadas["lat"], coordenadas["lon"], datos_clima.get("timezone", "N/A"), hora_lectura]
        })
        st.table(df_coordenadas)
        
        st.subheader("Pronóstico por hora: Temperatura y Velocidad del Viento")
        
        if "hourly" in datos_clima:
            df_horario = pd.DataFrame(datos_clima["hourly"])
            df_horario["time"] = pd.to_datetime(df_horario["time"])
            df_horario = df_horario.head(24)
            
            df_horario = df_horario.rename(columns={
                "temperature_2m": "Temperatura (°C)",
                "wind_speed_10m": "Velocidad del Viento (km/h)"
            })
            
            fig = px.line(
                df_horario, 
                x="time", 
                y=["Velocidad del Viento (km/h)", "Temperatura (°C)"], 
                labels={"value": "Escala / Medida", "time": "Hora del Día", "variable": "Parámetro"},
                color_discrete_map={
                    "Velocidad del Viento (km/h)": "#FF0000",
                    "Temperatura (°C)": "#00FF00"
                }
            )
            
            fig.update_layout(hovermode="x unified", legend_title_text="Métricas")
            st.plotly_chart(fig, use_container_width=True)
            
            #--------------------------------------------------------------
            st.markdown("Análisis de Probabilidad de Lluvia")
            st.markdown("Probablemente va a llover en las siguientes horas si la velocidad del viento es alta y la temperatura baja.")
            min_temp = df_horario["Temperatura (°C)"].min()
            max_viento = df_horario["Velocidad del Viento (km/h)"].max()
            
            if min_temp < 20 and max_viento > 20:
                st.error(f"🚨 **Alerta de Lluvia Alta:** Se espera lluvia en las próximas horas debido a vientos fuertes ({max_viento} km/h) y temperaturas bajas ({min_temp} °C). 🌧️")
            elif min_temp < 23 or max_viento > 15:
                st.warning(f"⚠️ **Advertencia de Lluvia Moderada:** Condiciones parcialmente inestables detectadas en el transcurso de las próximas 24 horas.")
            else:
                st.info("✅ **Baja probabilidad:** Condiciones estables. No se esperan lluvias significativas para las próximas horas.")
                
        else:
            st.warning("No se encontraron datos horarios en la respuesta de la API.")
        
    else:
        st.error("No se pudieron recuperar los datos de la API. Inténtalo de nuevo.")