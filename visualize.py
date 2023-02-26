import pandas as pd                     
import matplotlib.pyplot as plt
import yfinance as yf

# Define the list of stocks to analyze
stockList = ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'GOOGL', 'CSCO', 'PYPL', 'NFLX', 'INTC', 'AMD']

# Read the insider transaction data from an Excel file
insiderTransactions = pd.read_excel('insider_transactions.xlsx')

# Sort the DataFrame by the 'purchaseDate' column in ascending order (oldest to newest)
insiderTransactions.sort_values(by='purchaseDate', inplace=True)

# Remove any rows where the 'pricePerShare' column is not a valid numeric value
insiderTransactions['pricePerShare'] = pd.to_numeric(insiderTransactions['pricePerShare'], errors='coerce')
insiderTransactions = insiderTransactions[pd.notnull(insiderTransactions['pricePerShare'])]

# Convert the 'purchaseDate' column to datetime format
insiderTransactions['purchaseDate'] = pd.to_datetime(insiderTransactions['purchaseDate'])

# Create a figure and grid of subplots for the plot
fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(15, 20))
fig.suptitle('Stock Price Over Time')

# Define a function to display a plot for a given stock
def plot_stock(tickerSymbol, ax):
    # Get data on this stock
    tickerData = yf.Ticker(tickerSymbol)

    # Get the historical prices for this stock
    df = tickerData.history(period='1d', start='2020-1-1', end='2023-2-25')

    # Plot the stock price over time
    ax.plot(df['Close'], label=tickerSymbol)

    # Plot each insider transaction as a red dot on the plot
    transactions = insiderTransactions[(insiderTransactions['ticker'] == tickerSymbol) & (insiderTransactions['securityType'] == 'Common Stock')]
    ax.scatter(transactions['purchaseDate'], transactions['pricePerShare'], c='red', s=10)

    # Set the title and ylabel of the subplot
    ax.set_title(tickerSymbol)
    ax.set_ylabel('Price ($)')

    # Hide the xticks and tick labels for the subplot
    ax.tick_params(labelbottom=False)

# Plot each stock on a separate subplot of the same figure
for i, tickerSymbol in enumerate(stockList):
    row = i // 2
    col = i % 2
    plot_stock(tickerSymbol, axs[row, col])

# Adjust the spacing between the subplots
fig.tight_layout()

# Display the plot
plt.show()
