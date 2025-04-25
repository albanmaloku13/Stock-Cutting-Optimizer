import json
import os
import sys

# Define the base directory where the 'data' folder should be located
# For development, this will point to the same directory as the script; for executable, it will point to the dist folder
base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

# Define the path to the stock.json file within the 'data' folder
STOCK_FILE = os.path.join(base_dir, 'data', 'stock.json')

def create_default_stock():
    print(f"STOCK_FILE is set to: {STOCK_FILE}")
    stock = {
        "13.5": 2,
        "13": 3,
        "12.5": 1,
        "12.3": 1,
        "12": 2,
        "11.5": 1,
        "11": 2,
        "10.5": 2,
        "10": 3
    }

    # Ensure the 'data' directory exists
    if not os.path.exists(os.path.dirname(STOCK_FILE)):
        os.makedirs(os.path.dirname(STOCK_FILE))  # Create the 'data' directory if it doesn't exist
    
    # Write the stock data to the stock.json file
    with open(STOCK_FILE, 'w') as f:
        json.dump(stock, f, indent=4)
        print(f"Default stock file created at {STOCK_FILE}.")

def load_stock():
    print(f"Checking for stock file at {STOCK_FILE}")  # Debugging line
    if not os.path.exists(STOCK_FILE):
        # If the stock file doesn't exist, create it with default data
        print(f"Stock file not found at {STOCK_FILE}. Creating default stock...")
        create_default_stock()
    else:
        print(f"Stock file found at {STOCK_FILE}. Loading existing stock...")
    
    with open(STOCK_FILE, 'r') as f:
        return json.load(f)

def save_stock(stock):
    # Ensure the 'data' directory exists
    if not os.path.exists(os.path.dirname(STOCK_FILE)):
        os.makedirs(os.path.dirname(STOCK_FILE))  # Create the 'data' directory if it doesn't exist
    
    with open(STOCK_FILE, 'w') as f:
        json.dump(stock, f, indent=4)

def show_stock():
    stock = load_stock()
    if not stock:
        print("No stock available.")
    else:
        print("Current Stock:")
        for length, qty in sorted(stock.items(), key=lambda x: -float(x[0])):
            print(f"{length}m x {qty}")

def add_stock(length, quantity):
    stock = load_stock()
    length = str(length)
    if length in stock:
        stock[length] += quantity
    else:
        stock[length] = quantity
    save_stock(stock)
    print(f"Added {quantity}x {length}m to stock.")

def use_stock(length, quantity):
    stock = load_stock()
    length = str(length)
    if length not in stock or stock[length] < quantity:
        print(f"Not enough stock of {length}m.")
        return False
    stock[length] -= quantity
    if stock[length] == 0:
        del stock[length]
        print(f"{length}m table is now out of stock.")
    save_stock(stock)
    print(f"Used {quantity}x {length}m table(s).")
    return True

def remove_stock(length, quantity):
    stock = load_stock()
    length = str(length)
    if length in stock:
        stock[length] -= quantity
        if stock[length] <= 0:
            del stock[length]
            print(f"{length}m table is now out of stock.")
        else:
            print(f"Removed {quantity}x {length}m from stock.")
        save_stock(stock)
    else:
        print(f"No stock of {length}m found to remove.")