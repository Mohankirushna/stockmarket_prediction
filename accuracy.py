import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import SpanSelector
from sklearn.linear_model import LinearRegression
import numpy as np

# Define a list of companies and their ticker symbols
COMPANIES = {
    'Tata Consultancy Services': 'TCS.NS',
    'Reliance Industries': 'RELIANCE.NS',
    'Infosys': 'INFY.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Larsen & Toubro': 'LT.NS',
    'Mahindra & Mahindra': 'M&M.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'Wipro': 'WIPRO.NS',
    'Sun Pharmaceuticals': 'SUNPHARMA.NS',
    'Tata Motors': 'TATAMOTORS.NS',
}

# Define the path to save the predictions
PREDICTIONS_FILE = 'predictions.csv'

# Global variable to hold the axis reference
global_ax = None

def get_start_date(duration):
    """Returns the start date based on the selected duration."""
    today = datetime.today()
    if duration == '1 year':
        start_date = today - timedelta(days=365)
    elif duration == '2 years':
        start_date = today - timedelta(days=2*365)
    elif duration == '5 years':
        start_date = today - timedelta(days=5*365)
    else:
        raise ValueError('Unsupported duration. Use "1 year", "2 years", or "5 years".')
    return start_date.strftime('%Y-%m-%d')

def predict_future_prices(data, days=30):
    """Predict future prices using LinearRegression."""
    data = data.reset_index()
    data['Date'] = data['Date'].map(datetime.toordinal)
    X = data['Date'].values.reshape(-1, 1)
    y = data['Close'].values
    model = LinearRegression()
    model.fit(X, y)

    future_dates = [datetime.today() + timedelta(days=i) for i in range(1, days + 1)]
    future_dates_ordinal = np.array([date.toordinal() for date in future_dates]).reshape(-1, 1)
    future_prices = model.predict(future_dates_ordinal)

    return future_dates, future_prices

def plot_stock_data(ticker, duration):
    # Define the end date and calculate the start date based on the duration
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = get_start_date(duration)

    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")  # Debug information

    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        print(f"No data available for {ticker} from {start_date} to {end_date}.")
        return None, None, None

    # Create new features (e.g., moving averages)
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # Drop rows with NaN values resulting from the moving averages
    data.dropna(inplace=True)

    # Plot the stock closing price and moving averages
    fig, ax = plt.subplots(figsize=(10, 5))
    global global_ax
    global_ax = ax  # Assign the global variable to the local axis

    # Plot closing price
    ax.plot(data.index, data['Close'], label='Close Price', color='blue')

    # Plot 50-day moving average
    ax.plot(data.index, data['MA50'], label='50-Day Moving Average', color='red', linestyle='--')

    # Plot 200-day moving average
    ax.plot(data.index, data['MA200'], label='200-Day Moving Average', color='green', linestyle='--')

    # Add title and labels
    ax.set_title(f'{ticker} Stock Price and Moving Averages ({duration})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (INR)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # Predict future prices
    future_dates, future_prices = predict_future_prices(data)
    ax.plot(future_dates, future_prices, label='Predicted Prices', color='orange', linestyle='--')

    return fig, future_dates, future_prices

def save_predictions(ticker, future_dates, future_prices):
    """Save the predictions to a CSV file."""
    if not future_dates or not future_prices:
        return

    # Load existing predictions if the file exists
    try:
        predictions_df = pd.read_csv(PREDICTIONS_FILE)
        print(f"Loaded existing predictions from {PREDICTIONS_FILE}.")  # Debug information
    except FileNotFoundError:
        predictions_df = pd.DataFrame(columns=['Date', 'Ticker', 'Predicted_Price'])
        print(f"Created new DataFrame for predictions.")  # Debug information

    # Create a DataFrame for the new predictions
    new_predictions = pd.DataFrame({
        'Date': [date.strftime('%Y-%m-%d') for date in future_dates],
        'Ticker': [ticker] * len(future_dates),
        'Predicted_Price': future_prices
    })

    # Append new predictions to the existing DataFrame
    predictions_df = pd.concat([predictions_df, new_predictions], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    predictions_df.to_csv(PREDICTIONS_FILE, index=False)
    print(f"Saved predictions to {PREDICTIONS_FILE}.")  # Debug information

def display_previous_predictions(ticker):
    """Display previous predictions for the selected company."""
    try:
        predictions_df = pd.read_csv(PREDICTIONS_FILE)
        print(f"Loaded predictions from {PREDICTIONS_FILE}.")  # Debug information
    except FileNotFoundError:
        prediction_label.config(text="No previous predictions found.")
        print(f"File {PREDICTIONS_FILE} not found.")  # Debug information
        return

    print(f"Filtering predictions for {ticker}.")  # Debug information
    company_predictions = predictions_df[predictions_df['Ticker'] == ticker]

    if company_predictions.empty:
        prediction_label.config(text="No previous predictions found.")
        print(f"No predictions found for {ticker}.")  # Debug information
        return

    prediction_text = "Previous Predictions:\n\n"
    for index, row in company_predictions.iterrows():
        prediction_text += f"{row['Date']}: {row['Predicted_Price']:.2f} INR\n"

    prediction_label.config(text=prediction_text)

def on_plot_button_click():
    selected_company = company_combobox.get()
    ticker = COMPANIES.get(selected_company)
    duration = duration_combobox.get()
    if ticker:
        fig, future_dates, future_prices = plot_stock_data(ticker, duration)
        if fig:
            # Clear the old plot if any
            for widget in plot_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            toolbar_frame = tk.Frame(plot_frame)
            toolbar_frame.pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Add zoom and pan functionality
            def onselect(xmin, xmax):
                global global_ax
                global_ax.set_xlim(xmin, xmax)
                fig.canvas.draw_idle()

            span = SpanSelector(global_ax, onselect, 'horizontal', useblit=True, minspan=5, props=dict(color='red', alpha=0.5))
            
            # Display prediction details and save predictions
            prediction_text = "Predicted Prices for Next 30 Days:\n\n"
            for date, price in zip(future_dates, future_prices):
                prediction_text += f"{date.strftime('%Y-%m-%d')}: {price:.2f} INR\n"
            prediction_label.config(text=prediction_text)

            # Save predictions
            save_predictions(ticker, future_dates, future_prices)
            
            # Display previous predictions
            display_previous_predictions(ticker)
    else:
        print("Invalid company selected.")

# Create the GUI application
root = tk.Tk()
root.title("Stock Data Plotter")

# Create and place widgets
tk.Label(root, text="Select Company:").grid(row=0, column=0, padx=10, pady=10)
company_combobox = ttk.Combobox(root, values=list(COMPANIES.keys()))
company_combobox.grid(row=0, column=1, padx=10, pady=10)
company_combobox.set(list(COMPANIES.keys())[0])  # Default selection

tk.Label(root, text="Duration:").grid(row=1, column=0, padx=10, pady=10)
duration_combobox = ttk.Combobox(root, values=['1 year', '2 years', '5 years'])
duration_combobox.grid(row=1, column=1, padx=10, pady=10)
duration_combobox.set('1 year')  # Default selection

plot_button = tk.Button(root, text="Plot Data", command=on_plot_button_click)
plot_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Placeholder for the plot
plot_frame = tk.Frame(root)
plot_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Placeholder for the prediction details
prediction_label = tk.Label(root, text="", justify=tk.LEFT, anchor="w")
prediction_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Configure grid to expand properly
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()


