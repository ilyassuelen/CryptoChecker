import crypto_storage_sql as storage
from rich.table import Table
from rich.console import Console
from rich import box

console = Console()

# ---------------
# Program Menu
# ---------------
def interface(user_id):
    while True:
        print("""
Menu:
0. Exit
1. List all Cryptocurrencies
2. Add Cryptocurrency
3. Delete Cryptocurrency
4. Portfolio Stats
5. Search Cryptocurrency
""")
        choice = input("Enter choice (0-5): ")

        if choice == "0":
            print(f"Bye {user_id}!")
            break
        elif choice == "1":
            list_cryptos(user_id)
        elif choice == "2":
            add_crypto(user_id)
        elif choice == "3":
            delete_crypto(user_id)
        elif choice == "4":
            crypto_stats(user_id)
        elif choice == "5":
            search_crypto(user_id)
        else:
            print("Invalid choice, please enter a number between 0 and 5")

        input("\nPress Enter to continue...")


# ----------------
# Functions
# ----------------
def select_user():
    """Let the user select an existing user or create a new one."""
    users = storage.list_users()

    print("Welcome to CryptoChecker!\n")
    if not users:
        print("No users found. Let's create one!")
        name = input("Enter your name: ")
        storage.add_user(name)
        users = storage.list_users()

    print("Select a user: ")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user[1]}")
    print(f"{len(users)+1}. Create new user")

    choice = int(input("Enter choice: "))

    if choice == len(users) + 1:
        name = input("Enter new user name: ")
        storage.add_user(name)
        users = storage.list_users()
        return next(user[0] for user in users if user[1] == name)

    return users[choice - 1][0]


def list_cryptos(user_id):
    cryptos = storage.list_cryptos(user_id)
    if not cryptos:
        console.print("No cryptocurrencies found.", style="bold red")
        return

    table = Table(title="Cryptocurrency List", box=box.ROUNDED)
    table.add_column("Symbol", style="bold")
    table.add_column("Price", justify="right")
    table.add_column("Daily %", justify="right")
    table.add_column("Lowest", justify="right")
    table.add_column("Highest", justify="right")
    table.add_column("Exchange", justify="center")

    for symbol, data in cryptos.items():
        daily_color = "green" if data['daily_change_percentage'] >= 0 else "red"
        table.add_row(
            symbol,
            f"{data['last_price']:.4f}",
            f"[{daily_color}]{data['daily_change_percentage']:+.2f}%",
            f"{data['lowest_price']:.4f}",
            f"{data['highest_price']:.4f}",
            data['source_exchange'].capitalize()
        )

    console.print(table)


def add_crypto(user_id):
    """Add a new Cryptocurrency using FreeCryptoAPI."""
    crypto_symbol = input("Enter crypto symbol: ")

    # Fetch data from FreeCryptoAPI
    crypto_data = storage.fetch_crypto_data(crypto_symbol)
    if crypto_data is None:
        print("Cryptocurrency not found at FreeCryptoAPI.")
        return

    # Check if the Cryptocurrency already exists in the database
    cryptos = storage.list_cryptos(user_id)
    for symbol in cryptos:
        if symbol.lower() == crypto_symbol.lower():
            print(f"Cryptocurrency '{crypto_symbol}' already exists!")
            return

    # Ask for amount and investment
    amount = float(input("Enter amount owned: "))
    investment = float(input("Enter total investment amount: "))

    # Add Cryptocurrency to the database
    storage.add_crypto(
        crypto_data["symbol"],
        crypto_data["last_price"],
        crypto_data["lowest_price"],
        crypto_data["highest_price"],
        crypto_data["daily_change_percentage"],
        crypto_data["source_exchange"],
        amount,
        investment,
        user_id
    )
    print(f"Cryptocurrency '{crypto_data['symbol']}' successfully added.")


def delete_crypto(user_id):
    """Delete a Cryptocurrency by symbol."""
    symbol_name = input("Symbol name from Cryptocurrency: ")

    storage.delete_crypto(symbol_name, user_id)


def crypto_stats(user_id):
    """Show portfolio stats including gain/loss per coin and total portfolio in a table with top gainers/losers."""
    cryptos = storage.list_cryptos(user_id)
    if not cryptos:
        console.print("No cryptocurrencies found.", style="bold red")
        return

    # Berechne Profit/Loss pro Coin
    stats_list = []
    total_value = 0
    total_investment = 0
    for symbol, data in cryptos.items():
        amount = data.get("amount", 0)
        investment = data.get("investment", 0)
        current_value = amount * data['last_price']
        profit_loss = current_value - investment
        profit_loss_percent = (profit_loss / investment * 100) if investment else 0

        stats_list.append({
            "symbol": symbol,
            "amount": amount,
            "price": data['last_price'],
            "current_value": current_value,
            "investment": investment,
            "profit_loss": profit_loss,
            "profit_loss_percent": profit_loss_percent,
            "daily_change": data['daily_change_percentage'],
            "exchange": data['source_exchange']
        })

        total_value += current_value
        total_investment += investment

    # Sortiere nach Tagesgewinn für Top Gewinner/Verlierer
    sorted_by_profit = sorted(stats_list, key=lambda x: x['profit_loss_percent'], reverse=True)
    top_gainers = sorted_by_profit[:3]
    top_losers = sorted_by_profit[-3:]

    # Tabelle für Portfolio
    table = Table(title="Portfolio Stats", box=box.ROUNDED)
    table.add_column("Symbol", style="bold")
    table.add_column("Amount", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Value", justify="right")
    table.add_column("Investment", justify="right")
    table.add_column("P/L", justify="right")
    table.add_column("Daily %", justify="right")
    table.add_column("Exchange", justify="center")

    for stat in stats_list:
        pl_color = "green" if stat['profit_loss'] >= 0 else "red"
        daily_color = "green" if stat['daily_change'] >= 0 else "red"
        table.add_row(
            stat['symbol'],
            f"{stat['amount']:.2f}",
            f"{stat['price']:.4f}",
            f"{stat['current_value']:.2f}",
            f"{stat['investment']:.2f}",
            f"[{pl_color}]{stat['profit_loss']:.2f} ({stat['profit_loss_percent']:.2f}%)",
            f"[{daily_color}]{stat['daily_change']:+.2f}%",
            stat['exchange'].capitalize()
        )

    console.print(table)

    # Gesamtportfolio
    total_profit_loss = total_value - total_investment
    total_profit_loss_percent = (total_profit_loss / total_investment * 100) if total_investment else 0
    total_color = "green" if total_profit_loss >= 0 else "red"

    console.print(f"\nTotal Portfolio Value: {total_value:.2f}", style="bold")
    console.print(f"Total Investment: {total_investment:.2f}", style="bold")
    console.print(f"Total P/L: [{total_color}]{total_profit_loss:.2f} ({total_profit_loss_percent:.2f}%)\n")

    # Top 3 Gewinner
    console.print("Top 3 Gainers:", style="bold green")
    for g in top_gainers:
        console.print(f"{g['symbol']}: {g['profit_loss_percent']:.2f}%")

    # Top 3 Verlierer
    console.print("Top 3 Losers:", style="bold red")
    for l in reversed(top_losers):
        console.print(f"{l['symbol']}: {l['profit_loss_percent']:.2f}%")


def search_crypto(user_id):
    """Search for Cryptocurrencies containing a substring in their symbol."""
    cryptos = storage.list_cryptos(user_id)

    search_crypto_symbol = input("Enter part of currency symbol: ").lower()
    found = False

    for symbol, data in cryptos.items():
        if search_crypto_symbol in symbol.lower():
            print(f"{symbol} (Last Price: {data['last_price']}$ | Change percentage today: {data['daily_change_percentage']:+.1f}% | Lowest Price today: {data['lowest_price']}$ | Highest Price today: {data['highest_price']}$ | Source Exchange: {data['source_exchange']})")
            found = True

    if not found:
        print("No Cryptocurrency found. Try again.")


def cryptos_sorted_by_source_exchange(user_id):
    pass


def main():
    """Main program loop for the Cryptocurrency Database application."""
    # Choose user
    user_id = select_user()

    # Run the Menu
    interface(user_id)


if __name__ == "__main__":
    main()