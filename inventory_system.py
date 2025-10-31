import json
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable
stock_data = {}


def addItem(item=None, qty=0, logs=None):
    if logs is None:
        logs = []
    if not isinstance(item, str) or not item:
        logging.warning("Invalid item name: %s", item)
        return
    if not isinstance(qty, int):
        logging.warning("Quantity must be an integer, got %s", type(qty).__name__)
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def removeItem(item, qty):
    if not isinstance(item, str):
        logging.warning("Invalid item name: %s", item)
        return
    if not isinstance(qty, int):
        logging.warning("Quantity must be an integer, got %s", type(qty).__name__)
        return
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
            logging.info("Removed %d of %s", qty, item)
        else:
            logging.warning("Item %s not found in stock", item)
    except Exception as e:
        logging.error("Error removing item: %s", e)


def getQty(item):
    if not isinstance(item, str):
        logging.warning("Invalid item name: %s", item)
        return 0
    return stock_data.get(item, 0)


def loadData(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r") as f:
            stock_data = json.load(f)
        logging.info("Data loaded from %s", file)
    except FileNotFoundError:
        logging.warning("File %s not found, starting with empty stock", file)
        stock_data = {}
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON from %s: %s", file, e)
        stock_data = {}


def saveData(file="inventory.json"):
    try:
        with open(file, "w") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Data saved to %s", file)
    except Exception as e:
        logging.error("Error saving data to %s: %s", file, e)


def printData():
    logging.info("Items Report")
    if not stock_data:
        print("No items in stock.")
    else:
        for item, qty in stock_data.items():
            print(f"{item} -> {qty}")


def checkLowItems(threshold=5):
    if not isinstance(threshold, int) or threshold < 0:
        logging.warning("Invalid threshold: %s", threshold)
        threshold = 5
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    logs = []
    addItem("apple", 10, logs)
    addItem("banana", -2, logs)
    addItem("123", 10, logs)
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()


if __name__ == "__main__":
    main()
