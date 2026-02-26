# from airflow.decorators import dag, task
# from datetime import datetime
# import requests
# import json
# @dag(start_date=datetime(2026, 2, 21),
#     schedule="@daily", tags=['DAG-1']
# )

# def dag_tres():
#     @task
#     def return_json():
#         r = requests.get('https://api.publicapis.org/entries', timeout=10)
#         return response.json()
#     @task
#     def validat_json():
#      var = 3
#     print(var)        
#     @task
#     def third_wt():
#         var = 3
#         print(var)
#     @task
#     def fourth_wt():
#         var = 4
#         print(var)

#     first_wt()>>second_wt()>>third_wt()>>fourth_wt()

# dag_tres()



