from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 2, 25),
    schedule="@hourly", tags=['LAB']
)

def dag_uno():
    @task
    def first_wt():
        var = 1
        print(var)
    @task
    def second_wt():
        var = 4
        print(var)
    @task
    def third_wt():
        var = 6
        print(var)
    @task
    def fourth_wt():
        var = 4
        print(var)

    first_wt()>>second_wt()>>third_wt()>>fourth_wt()

dag_uno()



