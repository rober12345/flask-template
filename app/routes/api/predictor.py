# Flask imports
from flask import Blueprint, jsonify, current_app, send_file
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2
import os

# Define Blueprint
predictor_bp = Blueprint('predictor', __name__, url_prefix='/predict')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="economic_data-db",
        user="postgres",
        password="ManzanaOrganico1",
        host="localhost",
        port="5432"
    )

# Route to plot prediction data
@predictor_bp.route('/plot', methods=['GET'])
def plot_predictions():
    try:
        # Step 1: Fetch historical data
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, MXN_USD FROM economic_data
            WHERE date >= '2023-11-01'
            ORDER BY date;
        """)
        historical_data = cursor.fetchall()
        
        # Fetch forecast data (replace this with actual future forecast query)
        cursor.execute("""
            SELECT date, predicted_exchange_rate FROM forecast_data
            WHERE date >= '2024-11-01' AND date <= '2025-03-31'
            ORDER BY date;
        """)
        forecast_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Step 2: Convert to DataFrame
        data = pd.DataFrame(historical_data, columns=['date', 'mxn_usd'])
        future_data = pd.DataFrame(forecast_data, columns=['date', 'predicted_exchange_rate'])
        
        data['date'] = pd.to_datetime(data['date'])
        future_data['date'] = pd.to_datetime(future_data['date'])
        
        # Step 3: Plot the data
        plt.figure(figsize=(20, 10))
        
        # Plot Historical Data
        plt.plot(data['date'], data['mxn_usd'], label='Historical Data', color='blue')
        
        # Plot Forecast Data
        plt.plot(
            future_data['date'],
            future_data['predicted_exchange_rate'],
            label='Forecast with Daily Fluctuations (Nov 2024 - Mar 2025)',
            color='red',
            linestyle='--'
        )
        
        # Add Markers for Key Dates
        plt.axvline(pd.Timestamp('2024-11-01'), color='green', linestyle='--', label='Forecast Start (Nov 2024)')
        plt.axvline(pd.Timestamp('2025-01-01'), color='purple', linestyle='--', label='Forecast Start (Jan 2025)')
        plt.axvline(pd.Timestamp('2025-03-01'), color='orange', linestyle='--', label='Forecast Start (Mar 2025)')
        
        # Add Monthly Dividers
        for month_start in pd.date_range(start='2024-11-01', end='2025-03-31', freq='MS'):
            plt.axvline(month_start, color='gray', linestyle=':', alpha=0.6)
            plt.text(
                month_start,
                plt.ylim()[1] * 0.95,
                month_start.strftime('%b %Y'),
                rotation=90,
                verticalalignment='center',
                fontsize=9,
                color='gray'
            )
        
        # Format the x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        
        # Labels and Legend
        plt.title('Daily MXN/USD Exchange Rate Forecast with Realistic Fluctuations (Nov 2024 - Mar 2025)')
        plt.xlabel('Date')
        plt.ylabel('MXN/USD')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Step 4: Save plot as a static image
        plot_path = os.path.join(current_app.root_path, 'static', 'plots', 'forecast_plot.png')
        plt.savefig(plot_path)
        plt.close()
        
        return jsonify({"status": "success", "plot_path": "/static/plots/forecast_plot.png"})
    
    except Exception as e:
        current_app.logger.error(f"Error generating plot: {e}")
        return jsonify({"error": str(e)}), 500







# Ensure 'date' columns are datetime objects
data['date'] = pd.to_datetime(data['date'])
future_data['date'] = pd.to_datetime(future_data['date'])

# Verify alignment
print(data[['date', 'mxn_usd']].tail())
print(future_data[['date', 'predicted_exchange_rate']].head())



import matplotlib.dates as mdates

plt.figure(figsize=(20, 10))

# Plot Historical Data
plt.plot(data['date'], data['mxn_usd'], label='Historical Data', color='blue')

# Plot Forecast Data with Fluctuations
plt.plot(
    future_data['date'],
    future_data['predicted_exchange_rate'],
    label='Forecast with Daily Fluctuations (Nov 2024 - Mar 2025)',
    color='red',
    linestyle='--'
)

# Add Markers for Key Dates
plt.axvline(pd.Timestamp('2024-11-01'), color='green', linestyle='--', label='Forecast Start (Nov 2024)')
plt.axvline(pd.Timestamp('2025-01-01'), color='purple', linestyle='--', label='Forecast Start (Jan 2025)')
plt.axvline(pd.Timestamp('2025-03-01'), color='orange', linestyle='--', label='Forecast Start (Mar 2025)')

# Add Monthly Dividers
for month_start in pd.date_range(start='2024-11-01', end='2025-03-31', freq='MS'):
    plt.axvline(month_start, color='gray', linestyle=':', alpha=0.6)
    plt.text(
        month_start,
        plt.ylim()[1] * 0.95,
        month_start.strftime('%b %Y'),
        rotation=90,
        verticalalignment='center',
        fontsize=9,
        color='gray'
    )

# Format the x-axis dates properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gcf().autofmt_xdate()  # Rotate date labels for clarity

# Labels and Legend
plt.title('Daily MXN/USD Exchange Rate Forecast with Realistic Fluctuations (Nov 2024 - Mar 2025)')
plt.xlabel('Date')
plt.ylabel('MXN/USD')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

