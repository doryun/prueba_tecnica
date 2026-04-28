import requests
import pandas as pd
from datetime import datetime, timedelta

#Obtener datos meteorológicos de la ultima semana
def obtener_datos_meteorologicos_valencia(latitud=39.47,longitud=-0.38,city="Valencia"):
    # Obteniendo dias de la ultima semana
    fecha_final =datetime.utcnow().date() - timedelta(days=1)
    fecha_inicio =fecha_final - timedelta(days=49)
    #Elijo esta api porque no requiere auth
    api ="https://archive-api.open-meteo.com/v1/archive"

    #Parametros necesarios para hacer la llamada
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio.isoformat(),
        "end_date": fecha_final.isoformat(),
        #Este paramentro de abajo dice que datos obtenemos de ese dia, en este caso temp max y min y precipitaciones
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Madrid"
    }
    #hacemos el get con requests
    respuesta = requests.get(api,params=params,timeout=30)
    respuesta.raise_for_status()
    #la respuesta viene en formato json
    datos = respuesta.json()
    # Crear dataframe
    df = pd.DataFrame(datos["daily"])
    # Transformaciones para que sea mas legible
    df = df.rename(columns={"time": "date"})
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["latitude"] = datos["latitude"]
    df["longitude"] = datos["longitude"]
    df["city"] = city
    df["load_date"] = datetime.utcnow().date()
    return df