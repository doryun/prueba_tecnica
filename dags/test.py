from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta, timezone
from airflow.models import BaseOperator

NUMERO_TAREAS = 6

#La diferencia entre un Hook y una conexion es que la conexion contiene los datos que utilizara el hook
#para realizar acciones en el sistema al que se conecta.

default_args = {
'owner': 'airflow',
'depends_on_past': False,
'start_date': datetime(1900, 1, 1),
'retries': 1,
'retry_delay': timedelta(seconds=5)
}

class TimeDiff(BaseOperator):
    template_fields = ("int_date",)

    def __init__(self, int_date, **kwargs):
        super().__init__(**kwargs)
        self.int_date = int_date

    def execute(self, context):
        actual = datetime.now(timezone.utc)

        if isinstance(self.int_date, str):
            int_date = datetime.fromisoformat(self.int_date)
        else:
            int_date = self.int_date

        if int_date.tzinfo is None:
            int_date = int_date.replace(tzinfo=timezone.utc)

        diff = actual - int_date
        self.log.info(f"Fecha actual: {actual}")
        self.log.info(f"Fecha introducida: {int_date}")
        self.log.info(f"Hay una diferencia de: {diff}")

with DAG(
    dag_id= "test",
    schedule = "0 3 * * *",
    default_args=default_args
) as dag:
    tasks = {}

    start = EmptyOperator (task_id="start")
    end = EmptyOperator(task_id="end")

    # Crear tareas, se hace con 1 para evitar el 0 par
    for i in range(1,NUMERO_TAREAS + 1):
        tasks[i] = EmptyOperator(task_id=f"task_{i}")

    # Separamos impares y pares
    impares = [tasks[i] for i in range(1, NUMERO_TAREAS + 1) if(i % 2 != 0)]
    pares = [tasks[i] for i in range(1, NUMERO_TAREAS + 1) if(i % 2 == 0)]

    calculo_tiempo = TimeDiff(task_id="calculo_tiempo",int_date="2026-04-28T00:00:00")

start>>end
for par in pares:
    for impar in impares:
        impar >> par
calculo_tiempo