# Sandbox API URL
API_URL = "https://public.sandbox.pro.coinbase.com"

# Replace with your API credentials
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# Create a Coinbase Pro API client
client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_URL)

# Function to buy a specific amount of cryptocurrency
def buy_crypto(product_id, size):
  try:
    order = client.place_order(product_id=product_id,
                               side="buy",
                               size=size,
                               type="market")
    print(f"Bought {size} {product_id.split('-')[0]} at market price. Order ID: {order['id']}")
  except Exception as e:
    print(f"Error placing buy order: {e}")

# Function to sell a specific amount of cryptocurrency
def sell_crypto(product_id, size):
  try:
    order = client.place_order(product_id=product_id,
                               side="sell",
                               size=size,
                               type="market")
    print(f"Sold {size} {product_id.split('-')[0]} at market price. Order ID: {order['id']}")
  except Exception as e:
    print(f"Error placing sell order: {e}")

# Product IDs (replace with desired tokens)


def execute_trades(product_id = "BTC-USD", prev_position, target_position):
  # Simulate order execution based on signals
  ZERO = 0.0001 ### to avoid excessive trading

  delta_qty = target_position - prev_position 
  if delta_qty > ZERO:
    # Buy
    buy_crypto(product_id, delta_qty)

  if delta_qty < -(ZERO):
  # Sell 0.1 SOL (assuming you have some)
    sell_crypto(product_id, delta_qty)

  final_position = prev_position + delta_qty
  return (final_position)

