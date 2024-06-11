def mean_reverting_strategy(data = df_temp, window=60*24, multiplier=2):
  """
  Simulates a mean reverting trading strategy.

  Args:
      prices: A pandas Series of historical prices.
      window: The number of periods used to calculate the moving average.
      multiplier: A factor to scale the difference between the price and the moving average.

  Returns:
      A pandas DataFrame with buy, sell, and hold signals.
  """
  signals = pd.DataFrame(index=data.index, columns=['signal', 'price', 'next_price'])
  signals['close'] = data['close']
  signals['next_price'] = signals['close'].shift(-1)

  signals['moving_average'] = data['close'].rolling(window=window).mean()
  signals['zscore'] = (signals['close'] - signals['moving_average']) / signals['close'].rolling(window=window).std()

  signals['signal'] = 0  # 0: hold, 1: buy, -1: sell
  signals.loc[signals['zscore'] < -multiplier, 'signal'] = 1
  signals.loc[signals['zscore'] > multiplier, 'signal'] = -1

  # Calculate profit and loss
  signals['return'] = signals['next_price'] / signals['price'] - 1
  signals['strategy_return'] = signals['signal'] * signals['return']
  total_return = (signals['strategy_return'] + 1).prod() - 1

  print(f"Total return of the strategy: {total_return:.2%}")
  return signals

# Simulate some historical prices
#prices = pd.Series([10, 12, 15, 11, 8, 9, 13, 16, 14, 12], index=pd.date_range('2023-01-01', periods=10))

# Run the mean reverting strategy
signals = mean_reverting_strategy(df_temp.copy())

# Print the DataFrame with buy, sell, and hold signals
print(signals)