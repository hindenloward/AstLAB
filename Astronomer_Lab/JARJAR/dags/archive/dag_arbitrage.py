from airflow.sdk import dag, task
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import requests

@dag(start_date=datetime(2026, 2, 21),
    schedule="@daily", tags=['LAB']
)

def dag_connect():
    @task
    def pull_arbitrage_data():
        url = "https://sportsbook-api2.p.rapidapi.com/v0/advantages/"

        querystring = {"type":"ARBITRAGE"}

        headers = {
	        "x-rapidapi-key": "f86481e110msh66a7f1afac3aecep1eeb04jsn1d3493b8ba72",
	        "x-rapidapi-host": "sportsbook-api2.p.rapidapi.com"
}

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Parse the JSON response
       

    @task
    def create_file(data):
        s3 = S3Hook(aws_conn_id='aws_default')
        s3.load_string(
            string_data=str(data),
            key='Arbitrage_data.txt',
            bucket_name='amzn-demo-lab-astro-trials',
            replace=True
        )
    

   # data = pull_arbitrage_data()
    #create_file(data)

#dag_connect()



