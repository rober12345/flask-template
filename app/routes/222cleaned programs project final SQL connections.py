# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:51:55 2024

@author: rober ugalde
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 06:39:41 2024

@author: rober ugalde
"""



1 exchange_rate_data  saving data in economic_data-db=#
  
import psycopg2

# Setup the database connection
conn = psycopg2.connect(
    dbname="economic_data-db", 
    user="postgres", 
    password="ManzanaOrganico1", 
    host="localhost",  # or your database server address
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()


import sys
sys.path.append("C:\\Users\\rober ugalde\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages")


import yfinance as yf
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime

# Setup the database connection
import psycopg2

# Setup the database connection
conn = psycopg2.connect(
    dbname="economic_data-db", 
    user="postgres", 
    password="ManzanaOrganico1", 
    host="localhost",  # or your database server address
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()

# Step 1: Retrieve 10-year historical data for MXN/USD
ticker = "MXN=X"
data = yf.Ticker(ticker)
historical_data = data.history(period="10y")

# Step 2: Prepare the data
historical_data.reset_index(inplace=True)
historical_data = historical_data[["Date", "Close"]]
historical_data.rename(columns={"Close": "Exchange Rate (MXN/USD)"}, inplace=True)

# Insert the data into the database
for index, row in historical_data.iterrows():
    date = row["Date"].strftime("%Y-%m-%d")
    exchange_rate = row["Exchange Rate (MXN/USD)"]
    
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

# Display the plot as usual
plt.figure(figsize=(12, 6))
plt.plot(historical_data["Date"], historical_data["Exchange Rate (MXN/USD)"], label="MXN/USD", color="blue", linewidth=2)
plt.title("MXN/USD Exchange Rate - 10 Year Trend", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Exchange Rate (MXN/USD)", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()











xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

XXXXXXXXX


2 mexico_gdp  connecting to SQL

import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime

# Step 1: Define the FRED series code for Mexico's GDP
gdp_code = 'NGDPRSAXDCMXQ'  # Mexico's GDP in USD

# Step 2: Fetch the data from FRED (assuming you have an internet connection)
# Let's fetch the last 10 years of data (or adjust the dates as needed)
start_date = '2014-01-01'
end_date = '2024-01-01'

# Fetch GDP data from FRED
gdp_data = web.DataReader(gdp_code, 'fred', start_date, end_date)

# Step 3: Inspect the data (first few rows)
print(gdp_data.head())

# Step 4: Subtract the GDP data (e.g., subtracting the GDP of 2020 from all data points)
# Example: Subtract the GDP of 2020 from all years (or any other custom operation)
gdp_2020 = gdp_data.loc['2020']
gdp_data_subtracted = gdp_data - gdp_2020

# Step 5: Plot the original and subtracted GDP data
plt.figure(figsize=(12, 6))

# Plot original GDP data
plt.plot(gdp_data.index, gdp_data, label='Mexico GDP', color='blue')

# Plot the subtracted GDP data
plt.plot(gdp_data.index, gdp_data_subtracted, label='GDP - 2020', color='orange')

# Step 6: Customize the plot
plt.title("Mexico GDP (Original and Subtracted from 2020)")
plt.xlabel("Date")
plt.ylabel("GDP (USD Billion)")
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Step 7: Save the data into the existing economic_data table in PostgreSQL
# Setup the database connection
conn = psycopg2.connect(
    dbname="economic_data-db", 
    user="postgres", 
    password="ManzanaOrganico1", 
    host="localhost",  # or your database server address
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()

# Insert the GDP data into the economic_data table (Mexico_GDP column)
for date, gdp in gdp_data.iterrows():
    # Convert the date to string format and get the GDP value
    date_str = date.strftime('%Y-%m-%d')
    gdp_value = gdp['NGDPRSAXDCMXQ']
    
    # Insert or update the GDP data into the economic_data table
    cursor.execute("""
        INSERT INTO economic_data (date, Mexico_GDP) 
        VALUES (%s, %s)
        ON CONFLICT (date) DO UPDATE 
        SET Mexico_GDP = EXCLUDED.Mexico_GDP;
    """, (date_str, gdp_value))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()




xxxxxxxxxxxxxxxxxxxxxxxx



xxxxxxxxxxxxxxxxxxxxx



3 mexico_inflation

import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime

# Step 1: Define the FRED series code for Mexico's Inflation Rate
inflation_code = 'FPCPITOTLZGMEX'  # Mexico's Inflation Rate

# Step 2: Fetch the data from FRED (assuming you have an internet connection)
# Adjust the date range as needed
start_date = '2014-01-01'
end_date = '2024-01-01'

# Fetch inflation data from FRED
inflation_data = web.DataReader(inflation_code, 'fred', start_date, end_date)

# Step 3: Inspect the data (first few rows)
print(inflation_data.head())

# Step 4: Perform a custom operation (e.g., subtract the inflation rate of 2020)
# Ensure there is data for the target year
inflation_2020 = inflation_data.loc['2020'].mean()  # Use the average value of 2020 if multiple entries exist
inflation_data_subtracted = inflation_data - inflation_2020

# Step 5: Plot the original and adjusted inflation data
plt.figure(figsize=(12, 6))

# Plot original inflation data
plt.plot(inflation_data.index, inflation_data, label='Mexico Inflation Rate', color='blue')

# Plot the adjusted inflation data
plt.plot(inflation_data.index, inflation_data_subtracted, label='Inflation - 2020', color='orange')

# Step 6: Customize the plot
plt.title("Mexico Inflation Rate (Original and Adjusted for 2020)")
plt.xlabel("Date")
plt.ylabel("Inflation Rate (%)")
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Step 7: Save the data into the existing economic_data table in PostgreSQL
# Setup the database connection
conn = psycopg2.connect(
    dbname="economic_data-db", 
    user="postgres", 
    password="ManzanaOrganico1", 
    host="localhost",  # or your database server address
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()

# Insert the inflation data into the economic_data table (Mexico_Inflation column)
for date, inflation in inflation_data.iterrows():
    year = date.year
    inflation_value = inflation['FPCPITOTLZGMEX']
    
    print(f"Updating year: {year}, Inflation={inflation_value}")
    
    cursor.execute("""
        UPDATE economic_data
        SET mexico_inflation = %s
        WHERE date >= %s AND date < %s;
    """, (inflation_value, f'{year}-01-01', f'{year + 1}-01-01'))
    
conn.commit()






XXXXXXXXX

4 mexico_unemployment sql PostgreSQL

import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Replace with your FRED API key
series_id = "LRUN64TTMXA156N"  # Mexico Unemployment Rate Series ID
url = f"https://api.stlouisfed.org/fred/series/observations"

# Step 2: Fetch data from FRED API
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Successfully fetched data from FRED API")
    
    # Step 3: Extract observations
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 4: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "Unemployment Rate": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # 'coerce' converts invalid date formats to NaT
    
    # Remove rows with NaT in 'Date' or None in 'Unemployment Rate'
    df = df.dropna(subset=['Date', 'Unemployment Rate'])
    
    # Step 5: Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df["Date"], df["Unemployment Rate"], marker="o", linestyle="-", color="b")
    plt.title("Mexico Unemployment Rate (Ages 15-64)")
    plt.xlabel("Year")
    plt.ylabel("Unemployment Rate (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 6: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the unemployment data into the economic_data table (Mexico_Unemployment column)
    for _, row in df.iterrows():
        # Access the date and unemployment value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Use the Date column from the row
        unemployment_value = row['Unemployment Rate']
        
        # Insert or update the unemployment data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, Mexico_Unemployment) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET Mexico_Unemployment = EXCLUDED.Mexico_Unemployment;
        """, (date_str, unemployment_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")




xxxxxxx

5 usa_gdp

import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Your FRED API key
series_id = "GDP"  # USA GDP Series ID
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Fetch data from FRED API
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched USA GDP data from FRED API!")
    
    # Step 3: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 4: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "USA GDP": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Handle invalid date formats
    
    # Remove rows with NaT or None values
    df = df.dropna(subset=['Date', 'USA GDP'])
    
    # Step 5: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["USA GDP"], marker="o", linestyle="-", color="g")
    plt.title("USA GDP Over Time")
    plt.xlabel("Year")
    plt.ylabel("Gross Domestic Product (Billions USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 6: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the USA GDP data into the economic_data table (USA_GDP column)
    for _, row in df.iterrows():
        # Access the date and GDP value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        usa_gdp_value = row['USA GDP']
        
        # Insert or update the USA GDP data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, USA_GDP) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET USA_GDP = EXCLUDED.USA_GDP;
        """, (date_str, usa_gdp_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")





xxxxxxxxx


6 usa_inflation

import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Your FRED API key
series_id = "T10YIE"  # 10-Year Inflation Expectation Series ID
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Fetch data from FRED API
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched USA 10-Year Inflation data from FRED API!")
    
    # Step 3: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 4: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "USA Inflation": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Handle invalid date formats
    
    # Remove rows with NaT or None values
    df = df.dropna(subset=['Date', 'USA Inflation'])
    
    # Step 5: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["USA Inflation"], marker="o", linestyle="-", color="b")
    plt.title("USA 10-Year Breakeven Inflation Rate")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 6: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the USA Inflation data into the economic_data table (USA_Inflation column)
    for _, row in df.iterrows():
        # Access the date and inflation value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        usa_inflation_value = row['USA Inflation']
        
        # Insert or update the USA Inflation data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, USA_Inflation) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET USA_Inflation = EXCLUDED.USA_Inflation;
        """, (date_str, usa_inflation_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")





xxxxxxxx

 7 usa_unemployment with PostgreSQL
 
import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Your FRED API key
series_id = "UNRATE"  # USA Unemployment Rate Series ID
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Fetch data from FRED API
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched USA Unemployment Rate data from FRED API!")
    
    # Step 3: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 4: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "USA Unemployment": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Handle invalid date formats
    
    # Remove rows with NaT or None values
    df = df.dropna(subset=['Date', 'USA Unemployment'])
    
    # Step 5: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["USA Unemployment"], marker="o", linestyle="-", color="r")
    plt.title("USA Unemployment Rate")
    plt.xlabel("Year")
    plt.ylabel("Unemployment Rate (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 6: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
   
    # Insert the USA Unemployment data into the economic_data table (USA_Unemployment column)
    for _, row in df.iterrows():
        # Access the date and unemployment value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        usa_unemployment_value = row['USA Unemployment']
        
        # Insert or update the USA Unemployment data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, USA_Unemployment) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET USA_Unemployment = EXCLUDED.USA_Unemployment;
        """, (date_str, usa_unemployment_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")

 
 
 






XXXXXXX

8 sp500_data  with PostgreSQL :
    
import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Your FRED API key
series_id = "SP500"  # S&P 500 Series ID
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Define parameters to fetch data for the last 10 years
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "observation_start": "2014-01-01",  # 10 years ago
    "observation_end": "2024-01-01"     # Current year
}

# Step 3: Fetch data from FRED API
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched S&P 500 data from FRED API!")
    
    # Step 4: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 5: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "S&P 500 Index": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convert to datetime
    
    # Remove rows with NaT or None values
    df = df.dropna(subset=['Date', 'S&P 500 Index'])
    
    # Step 6: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["S&P 500 Index"], marker="o", linestyle="-", color="g")
    plt.title("S&P 500 Index (Last 10 Years)")
    plt.xlabel("Year")
    plt.ylabel("S&P 500 Index Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 7: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the S&P 500 data into the economic_data table (SP500 column)
    for _, row in df.iterrows():
        # Access the date and S&P 500 index value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        sp500_value = row['S&P 500 Index']
        
        # Insert or update the S&P 500 data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, SP500) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET SP500 = EXCLUDED.SP500;
        """, (date_str, sp500_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")
    
  



xxxxxx  works perfectly  



9 ipc_mexico_data   PostgreSQL

import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Your FRED API key
series_id = "SP500"  # S&P 500 Series ID
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Define parameters to fetch data for the last 10 years
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "observation_start": "2014-01-01",  # 10 years ago
    "observation_end": "2024-01-01"     # Current year
}

# Step 3: Fetch data from FRED API
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched S&P 500 data from FRED API!")
    
    # Step 4: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 5: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "S&P 500 Index": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convert to datetime
    
    # Remove rows with NaT or None values
    df = df.dropna(subset=['Date', 'S&P 500 Index'])
    
    # Step 6: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["S&P 500 Index"], marker="o", linestyle="-", color="g")
    plt.title("S&P 500 Index (Last 10 Years)")
    plt.xlabel("Year")
    plt.ylabel("S&P 500 Index Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Step 7: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the S&P 500 data into the economic_data table (SP500 column)
    for _, row in df.iterrows():
        # Access the date and S&P 500 index value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        sp500_value = row['S&P 500 Index']
        
        # Insert or update the S&P 500 data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, SP500) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET SP500 = EXCLUDED.SP500;
        """, (date_str, sp500_value))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")






xxxxxxx

10 oil_prices  PostgreSQL :
    

import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Step 1: Define FRED API details for WTI Crude Oil Prices
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Replace with your FRED API key
series_id = "IR14260"  # WTI Crude Oil Price (FRED series ID)
url = "https://api.stlouisfed.org/fred/series/observations"

# Step 2: Define parameters to fetch data for the last 10 years
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "observation_start": "2014-01-01",  # Start date (10 years ago)
    "observation_end": "2024-01-01"     # End date (current year)
}

# Step 3: Fetch data from FRED API
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Successfully fetched S&P 500 data from FRED API!")
    
    # Step 4: Extract observations
    data = response.json()
    observations = data["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"]) if obs["value"] != "." else None for obs in observations]
    
    # Step 5: Create a DataFrame
    df = pd.DataFrame({"Date": dates, "Oil Prices (WTI)": values})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convert to datetime
    
    # Check the columns to ensure proper naming
    print(df.columns)
    
    # Ensure there are no missing values or invalid entries
    df = df.dropna(subset=['Date', 'Oil Prices (WTI)'])
    
    # Step 6: Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Oil Prices (WTI)"], marker="o", linestyle="-", color="r")
    plt.title("WTI Crude Oil Prices (Last 10 Years)")
    plt.xlabel("Year")
    plt.ylabel("Oil Price (USD per barrel)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Step 7: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert or update the oil price data into the economic_data table
    for _, row in df.iterrows():
        # Access the date and oil price value from the row
        date_str = row['Date'].strftime('%Y-%m-%d')  # Format the date
        oil_price = row['Oil Prices (WTI)']
        
        # Insert or update the oil price data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, Oil_Prices) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET Oil_Prices = EXCLUDED.Oil_Prices;
        """, (date_str, oil_price))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Error fetching data: {response.status_code}")






xxxxxx

11 interest_rates_mex,


import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Define the API endpoint and your API key
url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "a5e807df13889a6f9009c9bdea0d650f"
series_id = "INTGSTMXM193N"  # Interest Rates for 10-Year Government Bonds in Mexico

# Define the parameters for the API request
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "frequency": "m",  # Monthly data
    "observation_start": "2000-01-01",  # Start date
    "observation_end": "2024-12-31"  # End date
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    observations = data["observations"]
    
    # Convert the data to a DataFrame for easy analysis
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])  # Convert the date column to datetime format
    df["value"] = pd.to_numeric(df["value"], errors='coerce')  # Convert value to numeric
    
    # Step 2: Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["value"], label="Interest Rates - 10-Year Government Bonds (Mexico)", color="red")
    plt.title("Interest Rates for 10-Year Government Bonds (Mexico)")
    plt.xlabel("Year")
    plt.ylabel("Interest Rate (%)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Step 3: Save the data into the existing economic_data table in PostgreSQL
    # Setup the database connection
    conn = psycopg2.connect(
        dbname="economic_data-db", 
        user="postgres", 
        password="ManzanaOrganico1", 
        host="localhost",  # or your database server address
        port="5432"        # default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert or update the interest rate data into the economic_data table
    for _, row in df.iterrows():
        # Access the date and interest rate value from the row
        date_str = row['date'].strftime('%Y-%m-%d')  # Format the date
        interest_rate = row['value']
        
        # Insert or update the interest rate data into the economic_data table
        cursor.execute("""
            INSERT INTO economic_data (date, Interest_Rates_Mex) 
            VALUES (%s, %s)
            ON CONFLICT (date) DO UPDATE 
            SET Interest_Rates_Mex = EXCLUDED.Interest_Rates_Mex;
        """, (date_str, interest_rate))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

else:
    print(f"Failed to fetch data: {response.status_code}")









xxxxxx
12  interest rates  with PostgreSQL:
    
import requests
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Define the API endpoint and API key
url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Replace with your API key
series_id = "DFF"  # Federal Funds Effective Rate series ID

# Define parameters for the API request
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "frequency": "m",
    "observation_start": "2014-01-01",
    "observation_end": "2024-12-31"
}

# Database connection settings
db_settings = {
    "dbname": "economic_data-db",
    "user": "postgres",
    "password": "ManzanaOrganico1",  # Replace with your password
    "host": "localhost",
    "port": "5432"
}

try:
    # Step 1: Fetch data from FRED API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Successfully fetched Federal Funds Effective Rate data from FRED API!")
        data = response.json()

        # Step 2: Process data into DataFrame
        observations = data["observations"]
        df = pd.DataFrame(observations)
        df["date"] = pd.to_datetime(df["date"])  # Convert to datetime
        df["value"] = pd.to_numeric(df["value"], errors='coerce')  # Convert to numeric
        df = df.dropna(subset=["value"])  # Drop rows with NaN values

        # Step 3: Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df["date"], df["value"], label="Federal Funds Effective Rate", color="blue")
        plt.title("Federal Funds Effective Rate (2014-2024)")
        plt.xlabel("Year")
        plt.ylabel("Rate (%)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

        # Step 4: Connect to PostgreSQL database
        connection = psycopg2.connect(**db_settings)
        cursor = connection.cursor()
        print("Connected to the database.")

        # Step 5: Insert or update the data into usa_interest_rates
        for _, row in df.iterrows():
            date_str = row["date"].strftime('%Y-%m-%d')
            interest_rate = row["value"]

            cursor.execute("""
                INSERT INTO economic_data (date, USA_Interest_Rates)
                VALUES (%s, %s)
                ON CONFLICT (date) DO UPDATE 
                SET USA_Interest_Rates = EXCLUDED.USA_Interest_Rates;
            """, (date_str, interest_rate))

        # Commit and close
        connection.commit()
        cursor.close()
        connection.close()
        print("Federal Funds Effective Rate data successfully saved to the database!")

    else:
        print(f"Failed to fetch data: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")









xxxxxx





13 trade_balance PostgreSQL


import requests
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Define the FRED API endpoint and API key
url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "a5e807df13889a6f9009c9bdea0d650f"  # Replace with your FRED API key
series_id = "BOPGTB"  # Trade Balance Series ID

# API Request parameters
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "frequency": "m",  # Monthly data
    "observation_start": "2014-01-01",  # Start date
    "observation_end": "2024-12-31"     # End date
}

# Database connection settings
db_settings = {
    "host": "localhost",
    "dbname": "economic_data-db",  # Database name
    "user": "postgres",            # Your database user
    "password": "ManzanaOrganico1",  # Replace with your actual database password
    "port": 5432                   # PostgreSQL default port
}

try:
    # Step 1: Fetch data from FRED API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Successfully fetched Trade Balance data from FRED API!")
        data = response.json()

        # Step 2: Process the data into a DataFrame
        observations = data["observations"]
        df = pd.DataFrame(observations)
        df["date"] = pd.to_datetime(df["date"])  # Convert to datetime
        df["value"] = pd.to_numeric(df["value"], errors='coerce')  # Convert value to numeric
        df = df.dropna(subset=["value"])  # Drop rows with NaN values

        # Step 3: Connect to PostgreSQL Database
        connection = psycopg2.connect(**db_settings)
        cursor = connection.cursor()
        print("Connected to the database.")

        # Step 4: Insert data into the economic_data table
        for _, row in df.iterrows():
            date = row["date"].date()
            value = row["value"]

            # Use UPSERT (INSERT ... ON CONFLICT) to avoid duplication
            cursor.execute("""
                INSERT INTO economic_data (date, trade_balance)
                VALUES (%s, %s)
                ON CONFLICT (date)
                DO UPDATE SET trade_balance = EXCLUDED.trade_balance;
            """, (date, value))

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        print("Trade Balance data successfully saved to the database!")

        # Step 5: Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df["date"], df["value"], label="Trade Balance", color="green")
        plt.title("US Trade Balance (2014-2024)")
        plt.xlabel("Year")
        plt.ylabel("Trade Balance (Millions of USD)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    else:
        print(f"Failed to fetch data: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")




xxxxxxxx




xxxxxxxx
xxxxx

14 remittances PostgreSQL :


import requests
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Define the API endpoint and your API key
url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "a5e807df13889a6f9009c9bdea0d650f"
series_id = "DDOI11MXA156NWDB"  # Remittances Series ID

# Define the parameters for the API request
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "frequency": "a",  # Annual data
    "observation_start": "2000-01-01",  # Start date
    "observation_end": "2024-12-31"  # End date
}

# Database connection settings
db_settings = {
    "host": "localhost",
    "dbname": "economic_data-db",  # Database name
    "user": "postgres",            # Your database user
    "password": "ManzanaOrganico1",  # Replace with your actual database password
    "port": 5432                   # PostgreSQL default port
}

try:
    # Step 1: Fetch data from FRED API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Successfully fetched Remittances data from FRED API!")
        data = response.json()

        # Step 2: Process the data into a DataFrame
        observations = data["observations"]
        df = pd.DataFrame(observations)
        df["date"] = pd.to_datetime(df["date"])  # Convert to datetime
        df["value"] = pd.to_numeric(df["value"], errors='coerce')  # Convert value to numeric
        df = df.dropna(subset=["value"])  # Drop rows with NaN values

        # Step 3: Connect to PostgreSQL Database
        connection = psycopg2.connect(**db_settings)
        cursor = connection.cursor()
        print("Connected to the database.")

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS remittances (
        date DATE PRIMARY KEY,
        remittances DOUBLE PRECISION
    );
    """)

    # Commit the changes and close the connection
    connection.commit()





        # Step 4: Insert data into the remittances table
        for _, row in df.iterrows():
            date = row["date"].date()
            value = row["value"]

            # Use UPSERT (INSERT ... ON CONFLICT) to avoid duplication
            cursor.execute("""
                INSERT INTO remittances (date, remittances)
                VALUES (%s, %s)
                ON CONFLICT (date)
                DO UPDATE SET remittances = EXCLUDED.remittances;
            """, (date, value))

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        print("Remittances data successfully saved to the database!")

        # Step 5: Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df["date"], df["value"], label="Remittances to Mexico", color="blue", marker="o")
        plt.title("Annual Remittances to Mexico (2000-2024)")
        plt.xlabel("Year")
        plt.ylabel("USD (Millions)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    else:
        print(f"Failed to fetch data: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")













"""
remittances original code :

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the API endpoint and your API key
url = "https://api.stlouisfed.org/fred/series/observations"
api_key = "a5e807df13889a6f9009c9bdea0d650f"
series_id = "DDOI11MXA156NWDB"  # Remittances Series ID

# Define the parameters for the API request
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json",
    "frequency": "a",  # Annual data
    "observation_start": "2000-01-01",  # Start date
    "observation_end": "2024-12-31"  # End date
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    observations = data["observations"]
    
    # Convert the data to a DataFrame for easy analysis
    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])  # Convert the date column to datetime format
    df["value"] = pd.to_numeric(df["value"], errors='coerce')  # Convert value to numeric
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["value"], label="Remittances to Mexico", color="blue", marker="o")
    plt.title("Annual Remittances to Mexico (2000-2024)")
    plt.xlabel("Year")
    plt.ylabel("USD (Millions)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()
else:
    print(f"Failed to fetch data: {response.status_code}")

"""



FETCHING THE DATA INTO ONE PAGER:
    
    
    


import psycopg2
import pandas as pd

# Database connection settings
db_settings = {
    "host": "localhost",
    "dbname": "economic_data-db",  # Updated database name
    "user": "postgres",            # Your database user
    "password": "ManzanaOrganico1",  # Replace with your actual database password
    "port": 5432                   # PostgreSQL default port
}

# Connect to the database
connection = psycopg2.connect(**db_settings)
query = "SELECT * FROM economic_data"

# Fetch data into DataFrame
df = pd.read_sql(query, connection)

# Close the database connection
connection.close()

# Display the first few rows of the dataframe
print(df.head())
    


XXXXX
Exploratory Data Analysis.

XXXX


import sys
sys.path.append("C:\\Users\\rober ugalde\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages")


import yfinance as yf
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime

# Setup the database connection
import psycopg2

# Step 1: Retrieve 10-year historical data for MXN/USD
ticker = "MXN=X"
data = yf.Ticker(ticker)
historical_data = data.history(period="10y")

# Step 2: Prepare the data
historical_data.reset_index(inplace=True)
historical_data = historical_data[["Date", "Close"]]
historical_data.rename(columns={"Close": "Exchange Rate (MXN/USD)"}, inplace=True)



import matplotlib.pyplot as plt

# Set the figure size for better visibility
plt.figure(figsize=(12, 8))



# Plot each economic indicator alongside mxn_usd
plt.subplot(3, 2, 1)
plt.plot(df['date'], df['Exchange Rate (MXN/USD)'], label='MXN to USD Exchange Rate', color='blue')
plt.title('MXN to USD Exchange Rate')
plt.xlabel('Date')
plt.ylabel('MXN to USD')

# Plot other economic indicators
plt.subplot(3, 2, 2)
plt.plot(df['date'], df['mexico_gdp'], label='Mexico GDP', color='green')
plt.title('Mexico GDP')
plt.xlabel('Date')
plt.ylabel('GDP (in Millions)')

plt.subplot(3, 2, 3)
plt.plot(df['date'], df['mexico_inflation'], label='Mexico Inflation', color='red')
plt.title('Mexico Inflation')
plt.xlabel('Date')
plt.ylabel('Inflation (%)')

plt.subplot(3, 2, 4)
plt.plot(df['date'], df['usa_gdp'], label='USA GDP', color='purple')
plt.title('USA GDP')
plt.xlabel('Date')
plt.ylabel('GDP (in Millions)')


plt.subplot(3, 2, 6)
plt.plot(df['date'], df['trade_balance'], label='Trade Balance', color='brown')
plt.title('US Trade Balance')
plt.xlabel('Date')
plt.ylabel('Trade Balance (Millions of USD)')

# Adjust layout
plt.tight_layout()
plt.show()
