
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

