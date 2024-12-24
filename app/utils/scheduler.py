from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
import requests

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data, 'interval', hours=24)
    scheduler.start()

def fetch_data():
    try:
        response = requests.get("http://127.0.0.1:5000/api/data/fetch")
        if response.status_code == 200:
            current_app.logger.info("Data ingestion successful")
        else:
            current_app.logger.error(f"Data ingestion failed: {response.content}")
    except Exception as e:
        current_app.logger.error(f"Scheduler error: {e}")
