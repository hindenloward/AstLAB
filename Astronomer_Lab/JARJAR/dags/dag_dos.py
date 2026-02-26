from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 2, 21),
    schedule=None, tags=['LAB']
)

def dag_dos():
    @task
    def first_wt():
        var = 1
        print(var)
    @task
    def second_wt():
        var = 2
        print(var)
    @task
    def third_wt():
        var = 3
        print(var)
    @task
    def fourth_wt():
        var = 4
        print(var)

    first_wt()
    second_wt()
    third_wt()
    fourth_wt()

dag_dos()



