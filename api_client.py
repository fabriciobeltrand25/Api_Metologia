import requests 

def obtener_clima(latitud, longitud):
   
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true&hourly=temperature_2m,wind_speed_10m&timezone=auto"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def traducir_codigo_clima(codigo):
    codigos = {
        0: "Cielo despejado ☀️",
        1: "Principalmente despejado 🌤️",
        2: "Parcialmente nublado ⛅",
        3: "Nublado ☁️",
        45: "Niebla 🌫️",
        48: "Niebla con escarcha 🌫️",
        51: "Llovizna ligera 🌧️",
        53: "Llovizna moderada 🌧️",
        55: "Llovizna densa 🌧️",
        61: "Lluvia débil 🌧️",
        63: "Lluvia moderada 🌧️",
        65: "Lluvia fuerte 🌧️",
        80: "Lluvia ligera intermitente 🌦️",
        81: "Lluvia moderada intermitente 🌦️",
        82: "Lluvia fuerte intermitente ⛈️",
        95: "Tormenta eléctrica ⛈️",
    }
    return codigos.get(codigo, "Condiciones variables 🌍")