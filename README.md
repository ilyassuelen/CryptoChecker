# CryptoChecker

[![GitHub Repository](https://img.shields.io/badge/GitHub-CryptoChecker-blue?logo=github)](https://github.com/ilyassuelen/CryptoChecker.git)

CryptoChecker is a Python terminal application to manage, monitor, and analyze your cryptocurrency portfolio. It uses **FreeCryptoAPI** to fetch current coin data and stores all coins locally in an SQLite database.

---

## Features

- **User management**: multiple users supported.
- **Add, delete, and search cryptocurrencies**.
- Fetch current coin data from FreeCryptoAPI:
  - Last price
  - Daily change (%)
  - Lowest and highest price of the day
  - Source exchange
- **Portfolio functionality**:
  - Store amount (`amount`) and invested value (`investment`) per coin
  - Calculate current value per coin
  - Calculate profit/loss per coin (absolute and percentage)
  - Calculate total portfolio statistics
- **Terminal UI with Rich tables**:
  - Color-coded: green = profit, red = loss
  - Easy-to-read tables with all key information
- **Top 3 gainers and losers** by percentage automatically displayed

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ilyassuelen/CryptoChecker.git
cd CryptoChecker