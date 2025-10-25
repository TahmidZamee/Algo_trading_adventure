# Algorithmic Trading Adventure

This project simulates a simple **Golden Cross trading strategy** using Python.  
Developed as part of an internship recruitment task.

---

## Project Overview

Alex, a budding programmer, starts their algorithmic trading adventure with a budget of **$5000**.  
This Python tool uses **moving averages (MA50 & MA200)** to identify buy and sell opportunities in the stock market.

The strategy:

1. Buy when the 50-day moving average crosses **above** the 200-day moving average (Golden Cross).  
2. Sell when the 50-day moving average crosses **below** the 200-day moving average (Death Cross).  
3. Track profits and close any open positions at the end of the data range.

---

## Features

- Fetch historical stock data using **yfinance**  
- Clean and preprocess market data  
- Calculate 50-day and 200-day moving averages  
- Detect Golden Cross (buy) and Death Cross (sell) signals  
- Simulate trading based on a fixed **$5000 budget**  
- Calculate total profit/loss  


