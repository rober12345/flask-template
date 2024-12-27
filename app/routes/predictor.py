from flask import Blueprint, jsonify, send_file, current_app
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2
import os

# Define Blueprint
predictor_bp = Blueprint('predictor', __name__)

# Database connection function
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
        # Step 1: Fetch historical and forecast data
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch Historical Data
        cursor.execute("""
            SELECT date, MXN_USD FROM economic_data
            WHERE date >= '2023-11-01'
            ORDER BY date;
        """)
        historical_data = cursor.fetchall()

        # Fetch Forecast Data
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

        # Step 3: Plot Data
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

        # Add Key Markers
        plt.axvline(pd.Timestamp('2024-11-01'), color='green', linestyle='--', label='Forecast Start')
        plt.axvline(pd.Timestamp('2025-01-01'), color='purple', linestyle='--', label='Forecast Midpoint')
        plt.axvline(pd.Timestamp('2025-03-01'), color='orange', linestyle='--', label='Forecast End')

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
        plt.gcf().autofmt_xdate()

        # Labels and Legend
        plt.title('Daily MXN/USD Exchange Rate Forecast (Nov 2024 - Mar 2025)')
        plt.xlabel('Date')
        plt.ylabel('MXN/USD')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Step 4: Save the Plot
        plot_path = os.path.join(current_app.root_path, 'static', 'plots', 'forecast_plot.png')
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plt.close()

        # Step 5: Serve the Plot
        return send_file(plot_path, mimetype='image/png', as_attachment=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
