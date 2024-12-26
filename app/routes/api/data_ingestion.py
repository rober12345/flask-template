# -*- coding: utf-8 -*-
"""
data_ingestion.py
Data ingestion for 14 economic variables into PostgreSQL.
@author: rober ugalde
"""

# Flask imports
from flask import Blueprint, jsonify, current_app
import psycopg2
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# Blueprint Definition
data_ingestion_bp = Blueprint('data_ingestion', __name__, url_prefix='/data')

# Database Connection
def get_db_connection():
    return psycopg2.connect(
        dbname="economic_data-db",
        user="postgres",
        password="ManzanaOrganico1",
        host="localhost",
        port="5432"
    )

# Execute Query Utility
def execute_query(query, params):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        current_app.logger.error(f"Database error: {e}")
        raise e

# Fetch Data from FRED API
def fetch_fred_data(series_id, column_name, start_date='2014-01-01', end_date='2024-12-31', frequency='m'):
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": "a5e807df13889a6f9009c9bdea0d650f",
            "file_type": "json",
            "frequency": frequency,
            "observation_start": start_date,
            "observation_end": end_date
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            observations = response.json()["observations"]
            df = pd.DataFrame(observations)
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors='coerce')
            df.dropna(subset=["value"], inplace=True)

            for _, row in df.iterrows():
                date = row["date"].strftime("%Y-%m-%d")
                value = row["value"]
                execute_query(
                    f"""INSERT INTO economic_data (date, {column_name})
                        VALUES (%s, %s)
                        ON CONFLICT (date) DO UPDATE 
                        SET {column_name} = EXCLUDED.{column_name};""",
                    (date, value)
                )
            return True
        else:
            current_app.logger.error(f"Failed to fetch data for {column_name}: {response.status_code}")
            return False
    except Exception as e:
        current_app.logger.error(f"Error fetching {column_name}: {e}")
        raise e

# ✅ Route for Each Variable

# 1. Exchange Rate Data (MXN/USD)
@data_ingestion_bp.route('/fetch_exchange_rate', methods=['GET'])
def fetch_exchange_rate():
    try:
        ticker = "MXN=X"
        data = yf.Ticker(ticker)
        historical_data = data.history(period="10y")
        historical_data.reset_index(inplace=True)
        historical_data = historical_data[["Date", "Close"]]
        historical_data.rename(columns={"Close": "MXN_USD"}, inplace=True)

        for _, row in historical_data.iterrows():
            date = row["Date"].strftime("%Y-%m-%d")
            value = row["MXN_USD"]
            execute_query(
                """INSERT INTO economic_data (date, MXN_USD)
                   VALUES (%s, %s)
                   ON CONFLICT (date) DO UPDATE 
                   SET MXN_USD = EXCLUDED.MXN_USD;""",
                (date, value)
            )
        return jsonify({"status": "success", "message": "Exchange rate data ingested."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. Remittances
@data_ingestion_bp.route('/fetch_remittances', methods=['GET'])
def fetch_remittances():
    return fetch_fred_data("DDOI11MXA156NWDB", "remittances")

# 3. Mexico GDP
@data_ingestion_bp.route('/fetch_mexico_gdp', methods=['GET'])
def fetch_mexico_gdp():
    return fetch_fred_data("NGDPRSAXDCMXQ", "Mexico_GDP")

# 4. Mexico Inflation
@data_ingestion_bp.route('/fetch_mexico_inflation', methods=['GET'])
def fetch_mexico_inflation():
    return fetch_fred_data("FPCPITOTLZGMEX", "Mexico_Inflation")

# 5. Mexico Unemployment
@data_ingestion_bp.route('/fetch_mexico_unemployment', methods=['GET'])
def fetch_mexico_unemployment():
    return fetch_fred_data("LRUN64TTMXA156N", "Mexico_Unemployment")

# 6. USA GDP
@data_ingestion_bp.route('/fetch_usa_gdp', methods=['GET'])
def fetch_usa_gdp():
    return fetch_fred_data("GDP", "USA_GDP")

# 7. USA Inflation
@data_ingestion_bp.route('/fetch_usa_inflation', methods=['GET'])
def fetch_usa_inflation():
    return fetch_fred_data("T10YIE", "USA_Inflation")

# 8. USA Unemployment
@data_ingestion_bp.route('/fetch_usa_unemployment', methods=['GET'])
def fetch_usa_unemployment():
    return fetch_fred_data("UNRATE", "USA_Unemployment")

# 9. S&P 500
@data_ingestion_bp.route('/fetch_sp500', methods=['GET'])
def fetch_sp500():
    return fetch_fred_data("SP500", "SP500")

# 10. Oil Prices
@data_ingestion_bp.route('/fetch_oil_prices', methods=['GET'])
def fetch_oil_prices():
    return fetch_fred_data("IR14260", "Oil_Prices")

# 11. Interest Rates Mexico
@data_ingestion_bp.route('/fetch_interest_rates_mex', methods=['GET'])
def fetch_interest_rates_mex():
    return fetch_fred_data("INTGSTMXM193N", "Interest_Rates_Mex")

# 12. USA Interest Rates
@data_ingestion_bp.route('/fetch_usa_interest_rates', methods=['GET'])
def fetch_usa_interest_rates():
    return fetch_fred_data("DFF", "USA_Interest_Rates")

# 13. Trade Balance
@data_ingestion_bp.route('/fetch_trade_balance', methods=['GET'])
def fetch_trade_balance():
    return fetch_fred_data("BOPGTB", "trade_balance")

# 14. IPC Mexico
@data_ingestion_bp.route('/fetch_ipc_mexico', methods=['GET'])
def fetch_ipc_mexico():
    return fetch_fred_data("SP500", "IPC_Mexico")


## ✅ **3. Next Steps**

1. Start Flask:
   ```cmd
   flask run
