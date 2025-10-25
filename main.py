from trading_strategy import AlgoTradingAdventure

if __name__ == "__main__":
    trader = AlgoTradingAdventure("AAPL", "2018-01-01", "2023-12-31", 5000)
    trader.download_data()
    trader.calculate_moving_averages()
    trader.simulate_trading()
    trader.results()
