from google.cloud import bigquery
from google.oauth2 import service_account
from descargar_datos import obtener_datos_meteorologicos_valencia

DATASET_NAME = "SANDBOX_weather_valencia"
TABLE_NAME = "weather_daily"


#Metodo para subir a Bigquery
def subir_df_a_bigquery(df):
    #Leemos las credenciales
    credenciales = service_account.Credentials.from_service_account_file("gcp-key.json")

    client = bigquery.Client(credentials=credenciales, project=credenciales.project_id)
    # Se crea el dataset si no existe
    dataset_name = "SANDBOX_weather_valencia"
    dataset_id = f"{credenciales.project_id}.{DATASET_NAME}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location ="EU"
    client.create_dataset(dataset, exists_ok=True)
    table_id =f"{dataset_id}.{TABLE_NAME}"

    #Escribimos en el dataset
    job_config =bigquery.LoadJobConfig(write_disposition="WRITE_APPEND",autodetect=True)
    job =client.load_table_from_dataframe(df,table_id,job_config=job_config)
    #Esperamos a que termine el job
    job.result()

def main():
    df = obtener_datos_meteorologicos_valencia()
    subir_df_a_bigquery(df)
    print("Subidos los datos")

if __name__ == "__main__":
    main()