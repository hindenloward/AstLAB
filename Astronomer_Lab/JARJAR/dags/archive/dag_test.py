from airflow.decorators import dag, task
from airflow.utils.email import send_email
from datetime import datetime

@dag(
    dag_id="smtp_test_email",
    start_date=datetime(2026, 2, 25),
    schedule=None,          # manual trigger only
    catchup=False,
    tags=["smtp", "test"],
)
def smtp_test_email():

    @task
    def send_test_email():
        send_email(
            to=["linden.howard@astrotrials.com"],
            subject="SMTP2GO Airflow Test",
            html_content="""
            <h3>SMTP Test Successful</h3>
            <p>This email confirms that Airflow can send email via SMTP2GO.</p>
            """
        )

    #send_test_email()

#smtp_test_email()