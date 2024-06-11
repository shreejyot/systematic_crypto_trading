from ta import bollinger_bands

def calculate_bb_signals(data, window=20, std=2):

  # Calculate Bollinger Bands
  bollinger_bands_indicator = bollinger_bands(data, window=20, std=2)
  upper_band = bollinger_bands_indicator[0]
  lower_band = bollinger_bands_indicator[1]

  # Generate buy/sell signals based on BB
  signals = []
  for i in range(len(data)):
    price = data.iloc[i]
    if price < lower_band.iloc[i]:
      signals.append(1)  # Buy signal
    elif price > upper_band.iloc[i]:
      signals.append(-1)  # Sell signal
    else:
      signals.append(0)  # Hold
  return signals