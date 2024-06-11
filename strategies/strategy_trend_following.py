import pandas as pd
import numpy as np

def trend_following_strategy(data = df_temp, fast_ma = 10, slow_ma = 50,transaction_cost = 0.003):
  """
  Implements a trend-following strategy using moving averages.

  Args:
      data (pandas.DataFrame): DataFrame containing price data (e.g., 'Open', 'Close')
      fast_ma (int): Period for the fast moving average
      slow_ma (int): Period for the slow moving average
      transaction_cost(float):  Adjust for your broker's fees (per share)

  Returns:
      pandas.DataFrame: DataFrame with buy/sell signals and P&L calculations
  """

  # Calculate moving averages
  data['fast_ma'] = data['close'].rolling(window=fast_ma).mean()
  data['slow_ma'] = data['close'].rolling(window=slow_ma).mean()

  # Generate buy/sell signals based on crossovers
  data['signal'] = 0  # 0 for hold, 1 for buy, -1 for sell
  data['signal'] = np.where(data['fast_ma'] > data['slow_ma'], 1, data['signal'])
  data['signal'] = np.where(data['fast_ma'] < data['slow_ma'], -1, data['signal'])

  # Shift signals by one day to avoid lookahead bias
  data['signal'] = data['signal'].shift(5)

  # Calculate positions (assuming constant position size for simplicity)
  data['position'] = data['signal'] * 1
  data['position'] = np.where(data['signal'] < 0, 0, data['position'])



  # Calculate cumulative returns based on positions and daily returns
  data['cumulative_returns'] = (data['position'] * data['daily_returns']).cumsum()

  # Calculate profit and loss (assuming constant transaction costs for simplicity)
    
  data['gross_returns'] = (data['position'] * data['daily_returns'])
  data['net_returns'] = data['gross_returns'] - (data['position'].abs() * transaction_cost)
  data['profit'] = data['net_returns'].cumsum()

  return data

# Example usage (replace with your actual data source)
#data = pd.read_csv('your_price_data.csv', index_col='Date', parse_dates=True)
