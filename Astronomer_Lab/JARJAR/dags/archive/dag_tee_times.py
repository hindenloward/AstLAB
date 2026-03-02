from airflow.sdk import dag, task
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from openai import OpenAI
from airflow.utils.email import send_email
import requests
from bs4 import BeautifulSoup

URL = "https://www.coloradonationalgolfclub.com/tee-times"  
page = requests.get(URL)

# Check if the request was successful
if page.status_code != 200:
    print("Failed to retrieve the web page")
    exit()
else:
    print("Web page retrieved successfully")
soup = BeautifulSoup(page.content, "html.parser")

for tee_times in soup.find_all("Tee_Times", id="teetimes-tile-time"):
    print(tee_times.text.strip())