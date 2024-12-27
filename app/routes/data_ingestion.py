# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 14:42:14 2024
data_ingestion
@author: rober ugalde
"""

from flask import Blueprint, jsonify
import requests
import pandas as pd
import psycopg2
import yfinance as yf
from datetime import datetime

# Define the data ingestion blueprint
data_ingestion_bp = Blueprint('data_ingestion', __name__)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost", 
        port="5432"
    )

# Route to fetch and save all economic data
@data_ingestion_bp.route('/fetch', methods=['GET'])
def fetch_and_save_data():
    try:
        exchange_rate_data()
        mexico_gdp_data()
        mexico_inflation_data()
        mexico_unemployment_data()
        usa_gdp_data()
        usa_inflation_data()
        usa_unemployment_data()
        trade_balance_data()
        remittances_data()
        oil_prices_data()
        interest_rates_mexico_data()
        interest_rates_usa_data()
        sp500_data()
        ipc_mexico_data()  # Added IPC data fetch
        
        return jsonify({"message": "All data fetched and saved successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def exchange_rate_data():
    conn = get_db_connection()
    cursor = conn.cursor()

  # Step 1: Retrieve 10-year historical data for MXN/USD
    ticker = "MXN=X"
    data = yf.Ticker(ticker)
    historical_data = data.history(period="10y").reset_index()
    historical_data = historical_data[["Date", "Close"]].rename(columns={"Close": "MXN_USD"})

  # Insert the data into the database
    for index, row in historical_data.iterrows():
        date = row["Date"].strftime("%Y-%m-%d")
        exchange_rate = row["Exchange Rate  MXN_USD"]

      # Insert data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, MXN_USD) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET MXN_USD = EXCLUDED.MXN_USD;
        """, (date, exchange_rate))

  # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()

#2 mexico_gdp  connecting to SQL

import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime



# Step 1: Define the FRED series code for Mexico's GDP
def mexico_gdp_data():
    gdp_code = 'NGDPRSAXDCMXQ'  # Mexico's GDP in USD
    start_date = '2014-01-01'
    end_date = '2024-01-01'

    gdp_data = web.DataReader(gdp_code, 'fred', start_date, end_date)

# Step 7: Save the data into the existing economic_data table in PostgreSQL
# Setup the database connection
  
    conn = get_db_connection()
    cursor = conn.cursor()

  # Insert the GDP data into the economic_data table (Mexico_GDP
    for date, gdp in gdp_data.iterrows():
        date_str = date.strftime('%Y-%m-%d')
        gdp_value = gdp['NGDPRSAXDCMXQ']
        
        cursor.execute("""
            INSERT INTO economic_data (date, Mexico_GDP) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET Mexico_GDP = EXCLUDED.Mexico_GDP;
        """, (date_str, gdp_value))

    conn.commit()
    cursor.close()
    conn.close()

def mexico_inflation_data():
    inflation_code = 'FPCPITOTLZGMEX'  # Mexico's Inflation Rate
    start_date = '2014-01-01'
    end_date = '2024-01-01'

    inflation_data = web.DataReader(inflation_code, 'fred', start_date, end_date)

    conn = get_db_connection()
    cursor = conn.cursor()

    for date, inflation in inflation_data.iterrows():
        date_str = date.strftime('%Y-%m-%d')
        inflation_value = inflation['FPCPITOTLZGMEX']
        
        cursor.execute("""
            INSERT INTO economic_data (date, Mexico_Inflation) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET Mexico_Inflation = EXCLUDED.Mexico_Inflation;
        """, (date_str, inflation_value))

    conn.commit()
    cursor.close()
    conn.close()

def mexico_unemployment_data():
    unemployment_code = 'LRUN64TTMXA156N'  # Mexico's Unemployment Rate
    url = f"https://api.stlouisfed.org/fred/series/observations"
    
    params = {
        "series_id": "LRUN64TTMXA156N",
        "api_key": "a5e807df13889a6f9009c9bdea0d650f",  # Replace with your actual API key
        "file_type": "json"
    }

    response = requests.get(url, params=params)






