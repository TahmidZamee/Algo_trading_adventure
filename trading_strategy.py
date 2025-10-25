import yfinance as yf
import pandas as pd

class AlgoTradingAdventure:
    def __init__(self, symbol, start_date, end_date, budget=5000):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.data = pd.DataFrame()
        self.position = False
        self.buy_price = 0
        self.shares = 0
        self.profit = 0

    def download_data(self):
        print(f"Downloading data for {self.symbol}...")
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)

        # Handle multi-index column issue (yfinance sometimes returns multi-level columns)
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)

        # Clean data
        self.data = self.data[~self.data.index.duplicated(keep='first')]
        self.data = self.data.ffill()
        print(f"Data download complete. Rows: {len(self.data)} | Columns: {self.data.columns.tolist()}")

    def calculate_moving_averages(self):
        if self.data.empty:
            print("No data available. Please run download_data() first.")
            return

        if 'Close' not in self.data.columns:
            print("Error: 'Close' column not found in data. Columns present:", self.data.columns.tolist())
            return

        print("Calculating moving averages...")
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
        print("Moving averages added successfully.")

    def simulate_trading(self):
        print("Starting simulation...")

        # Auto-calculate moving averages if missing
        if 'MA50' not in self.data.columns or 'MA200' not in self.data.columns:
            print("Moving averages not found — calculating now.")
            self.calculate_moving_averages()

        # Check again
        if 'MA50' not in self.data.columns or 'MA200' not in self.data.columns:
            print("❌ Error: MA50 or MA200 columns still missing. Aborting simulation.")
            print("Columns currently available:", self.data.columns.tolist())
            return

        # Drop rows with missing MAs
        self.data = self.data.dropna(subset=['MA50', 'MA200'])
        print(f"Simulation rows after cleaning: {len(self.data)}")

        for i in range(1, len(self.data)):
            row_yesterday = self.data.iloc[i - 1]
            row_today = self.data.iloc[i]

            ma50_prev = float(row_yesterday['MA50'])
            ma200_prev = float(row_yesterday['MA200'])
            ma50_today = float(row_today['MA50'])
            ma200_today = float(row_today['MA200'])

            # Golden Cross (Buy)
            if not self.position and ma50_prev < ma200_prev and ma50_today > ma200_today:
                self.buy(float(row_today['Close']), row_today.name)

            # Death Cross (Sell)
            elif self.position and ma50_prev > ma200_prev and ma50_today < ma200_today:
                self.sell(float(row_today['Close']), row_today.name)

        # Force close at end if still open
        if self.position:
            self.sell(float(self.data.iloc[-1]['Close']), self.data.index[-1])

    def buy(self, price, date):
        self.shares = int(self.budget // price)
        if self.shares == 0:
            print("Not enough budget to buy shares.")
            return
        self.buy_price = price
        self.position = True
        print(f"BUY: {self.shares} shares at ${price:.2f} on {date.date()}")

    def sell(self, price, date):
        if not self.position or self.shares == 0:
            return
        revenue = self.shares * price
        cost = self.shares * self.buy_price
        trade_profit = revenue - cost
        self.profit += trade_profit
        self.position = False
        print(f"SELL: {self.shares} shares at ${price:.2f} on {date.date()} | Trade Profit: ${trade_profit:.2f}")

    def results(self):
        print("\n--- Final Report ---")
        print(f"Total Profit/Loss: ${self.profit:.2f}")
        return self.profit
