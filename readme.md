# 📈 Stock Data Plotter and Price Predictor

This Python application allows users to visualize historical stock data and predict future prices for selected Indian companies using **Yahoo Finance** data and simple linear regression. The app features a **Tkinter GUI** with interactive plotting and zooming capabilities.

---

## 🚀 Features

- Select from a predefined list of popular Indian companies (TCS, Reliance, Infosys, etc.).
- Choose a historical data duration: 1 year, 2 years, or 5 years.
- Fetches historical stock data from Yahoo Finance using `yfinance`.
- Calculates and plots:
  - Closing stock prices
  - 50-day and 200-day moving averages
- Predicts stock prices for the next 30 days using **Linear Regression**.
- Interactive plot with zoom and pan features.
- Displays predicted future prices in the GUI.
- Saves predictions to a CSV file (`predictions.csv`) and displays previous predictions on demand.

---

## 🛠️ How It Works

### Data Fetching and Preprocessing

- Based on the selected company ticker and duration, the app fetches stock data from Yahoo Finance.
- Calculates 50-day and 200-day moving averages to visualize trends.
- Cleans data by dropping rows with missing values caused by moving average calculations.

### Visualization

- Plots the closing price along with the moving averages.
- Uses Matplotlib embedded inside the Tkinter GUI to render interactive charts.
- Enables zoom and pan on the plot via `SpanSelector`.

### Price Prediction

- Uses `sklearn.linear_model.LinearRegression` to fit a model on historical closing prices.
- Predicts closing prices for the next 30 days.
- Displays the predicted prices on the plot and in a text widget.
- Saves predictions to a CSV file for future reference.

### GUI Components

- **Company Selection Dropdown:** Choose from a list of Indian company stocks.
- **Duration Selection Dropdown:** Choose data duration (1, 2, or 5 years).
- **Plot Button:** Fetches data, plots charts, predicts prices, and updates GUI.
- **Plot Area:** Shows historical and predicted stock prices with moving averages.
- **Prediction Display:** Lists predicted prices for the next 30 days and previous predictions from file.

---

## ⚙️ Installation & Setup

1. Clone the repository or download the script.
2. Install required Python packages (preferably in a virtual environment):

```bash
pip install yfinance pandas matplotlib scikit-learn numpy tk
```
Note: tkinter is often included with Python installations. If not, install it using your OS package manager.

## 📋 Code Overview
Key Functions
get_start_date(duration)
Returns the start date string based on the user-selected duration (1, 2, or 5 years).

predict_future_prices(data, days=30)
Fits a linear regression model to historical closing prices and predicts future prices for the next days days.

plot_stock_data(ticker, duration)
Fetches historical stock data, calculates moving averages, plots data, and calls the prediction function to add predicted prices on the plot.

save_predictions(ticker, future_dates, future_prices)
Saves the predicted prices to a CSV file (predictions.csv). It appends new predictions and loads existing data if available.

display_previous_predictions(ticker)
Loads and displays previously saved predictions for the selected company.

on_plot_button_click()
Main GUI callback to update plots and predictions based on user selections.

🖥️ Running the Application
Run the Python script to open the GUI window:
```
python your_script_name.py
```
Select a company from the dropdown.
Select a data duration.
Click Plot Data.
View the historical stock prices with moving averages and predicted future prices.
Zoom into the plot by clicking and dragging on the plot area.

## 🧩 Dependencies
yfinance: For fetching historical stock data from Yahoo Finance.
pandas: Data manipulation and CSV file handling.
matplotlib: Plotting stock data and predictions.
scikit-learn: Linear regression model for predictions.
numpy: Numerical operations.
tkinter: GUI framework.

## 🔍 Notes & Considerations
The prediction model uses a simple linear regression on closing prices and is primarily for demonstration; real stock price prediction is far more complex.
The app saves predictions to a CSV file in the working directory. Ensure write permissions.
If no data is found for a ticker/duration, the app handles it gracefully with console messages.
Zooming uses Matplotlib's SpanSelector for intuitive range selection.

## 🎯 Future Enhancements
Use more advanced models (e.g., LSTM, ARIMA) for price prediction.
Add more interactive GUI elements and styling.
Include additional stock indicators (RSI, MACD).
Enable export of plots and reports.
Add error handling for internet connection issues.

## 📚 References
Yahoo Finance (yfinance) Documentation
Matplotlib Embed in Tkinter
scikit-learn Linear Regression
Tkinter Documentation
