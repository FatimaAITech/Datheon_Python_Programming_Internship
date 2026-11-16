
import csv
from pathlib import Path


# Get project folder path
BASE_DIR = Path(__file__).resolve().parent

TICKERS_FILE = BASE_DIR / "sp500_tickers.csv"
PRICES_FILE = BASE_DIR / "stock_prices.csv"
OUTPUT_FILE = BASE_DIR / "portfolio_summary.csv"


# Load valid stock symbols from S&P 500 dataset
def load_valid_tickers():

    valid_tickers = set()

    try:
        with open(TICKERS_FILE, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or "Symbol" not in reader.fieldnames:
                raise ValueError("Symbol column not found in ticker dataset.")

            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()

                if symbol:
                    valid_tickers.add(symbol)

    except FileNotFoundError:
        print("Error: sp500_tickers.csv not found!")
        return None

    except (ValueError, csv.Error) as error:
        print("Dataset error:", error)
        return None

    return valid_tickers


# Load stock prices from sample price dataset
def load_stock_prices():

    stock_prices = {}

    try:
        with open(PRICES_FILE, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or not {"Symbol", "CurrentPrice"}.issubset(reader.fieldnames):
                raise ValueError("Required columns are Symbol and CurrentPrice.")

            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()

                try:
                    price = float(row.get("CurrentPrice", ""))

                    if symbol and price > 0:
                        stock_prices[symbol] = price

                except (ValueError, TypeError):
                    continue

    except FileNotFoundError:
        print("Error: stock_prices.csv not found!")
        return None

    except (ValueError, csv.Error) as error:
        print("Price dataset error:", error)
        return None

    return stock_prices


# Get valid positive numeric input
def get_positive_number(message, number_type):

    while True:
        try:
            value = number_type(input(message).strip())

            if value <= 0:
                print("Please enter a value greater than zero.")
                continue

            return value

        except ValueError:
            print("Invalid input! Please enter a valid number.")


# Calculate performance for one stock
def calculate_stock_performance(buy_price, current_price, quantity):

    invested = buy_price * quantity
    current_value = current_price * quantity
    profit_loss = current_value - invested
    percentage = (profit_loss / invested) * 100

    return invested, current_value, profit_loss, percentage


# Display portfolio summary
def display_portfolio(portfolio):

    total_invested = sum(item["invested"] for item in portfolio)
    total_value = sum(item["current_value"] for item in portfolio)
    total_profit = total_value - total_invested

    total_percentage = (
        (total_profit / total_invested) * 100
        if total_invested > 0 else 0
    )

    print("\n" + "=" * 75)
    print("             STOCK PORTFOLIO PERFORMANCE REPORT")
    print("=" * 75)

    print(
        f"{'Symbol':<10}"
        f"{'Buy Price':>12}"
        f"{'Current':>12}"
        f"{'Shares':>10}"
        f"{'Profit/Loss':>15}"
        f"{'Return %':>12}"
    )

    print("-" * 75)

    for item in portfolio:
        print(
            f"{item['symbol']:<10}"
            f"{item['buy_price']:>12.2f}"
            f"{item['current_price']:>12.2f}"
            f"{item['quantity']:>10}"
            f"{item['profit_loss']:>15.2f}"
            f"{item['percentage']:>11.2f}%"
        )

    print("-" * 75)
    print(f"Total Invested:       ${total_invested:.2f}")
    print(f"Current Portfolio:    ${total_value:.2f}")
    print(f"Total Profit/Loss:    ${total_profit:.2f}")
    print(f"Overall Return:        {total_percentage:.2f}%")
    print("=" * 75)


# Save results to CSV file
def save_portfolio_to_csv(portfolio):

    fieldnames = [
        "Symbol",
        "BuyPrice",
        "CurrentPrice",
        "Quantity",
        "Invested",
        "CurrentValue",
        "ProfitLoss",
        "ReturnPercentage"
    ]

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for item in portfolio:
                writer.writerow({
                    "Symbol": item["symbol"],
                    "BuyPrice": f"{item['buy_price']:.2f}",
                    "CurrentPrice": f"{item['current_price']:.2f}",
                    "Quantity": item["quantity"],
                    "Invested": f"{item['invested']:.2f}",
                    "CurrentValue": f"{item['current_value']:.2f}",
                    "ProfitLoss": f"{item['profit_loss']:.2f}",
                    "ReturnPercentage": f"{item['percentage']:.2f}"
                })

        print(f"\nPortfolio saved successfully to: {OUTPUT_FILE.name}")

    except OSError as error:
        print("Unable to save portfolio:", error)


# Main application
def main():

    print("\n==========================================")
    print("     STOCK PORTFOLIO TRACKER")
    print("==========================================")

    valid_tickers = load_valid_tickers()
    stock_prices = load_stock_prices()

    if valid_tickers is None or stock_prices is None:
        print("\nPlease check your CSV files and try again.")
        return

    portfolio = []

    while True:

        symbol = input("\nEnter stock ticker symbol: ").strip().upper()

        if not symbol:
            print("Ticker symbol cannot be empty.")
            continue

        if symbol not in valid_tickers:
            print("Invalid ticker! Symbol not found in S&P 500 dataset.")
            continue

        if symbol not in stock_prices:
            print("Price unavailable for this ticker in sample dataset.")
            continue

        buy_price = get_positive_number("Enter purchase price: ", float)
        quantity = get_positive_number("Enter number of shares: ", int)

        current_price = stock_prices[symbol]

        invested, current_value, profit_loss, percentage = (
            calculate_stock_performance(
                buy_price,
                current_price,
                quantity
            )
        )

        portfolio.append({
            "symbol": symbol,
            "buy_price": buy_price,
            "current_price": current_price,
            "quantity": quantity,
            "invested": invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "percentage": percentage
        })

        print(f"\n{symbol} added successfully!")
        print(f"Current sample price: ${current_price:.2f}")
        print(f"Profit/Loss: ${profit_loss:.2f}")

        while True:
            choice = input("\nAdd another stock? (yes/no): ").strip().lower()

            if choice in ("yes", "y"):
                break

            elif choice in ("no", "n"):
                if portfolio:
                    display_portfolio(portfolio)
                    save_portfolio_to_csv(portfolio)

                print("\nThank you for using Stock Portfolio Tracker!")
                return

            else:
                print("Please enter yes or no.")


if __name__ == "__main__":
    main()
