from sqlalchemy import create_engine, text
import requests

DB_URL = "sqlite:///cryptos.db"

engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))

    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS cryptos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            last_price REAL NOT NULL,
            lowest_price REAL NOT NULL,
            highest_price REAL NOT NULL,
            daily_change_percentage REAL NOT NULL,
            source_exchange TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """))
    connection.commit()


def fetch_crypto_data(symbol):
    api_key = "gl0zi6ri81x7k65hli89"
    url = f"https://api.freecryptoapi.com/v1/getData?symbol={symbol}&token={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "success":
            print(f"Cryptocurrency '{symbol}' not found in FreeCryptoAPI Database.")
            return None

        return {
            "symbol": data.get("symbol", symbol),
            "last_price": last_price,
            "lowest_price": lowest_price,
            "highest_price": highest_price,
            "daily_change_percentage": daily_change_percentage,
            "source_exchange": source_exchange
        }

    except requests.RequestException as e:
        print(f"Error accessing FreeCryptoAPI: {e}")
        return None
