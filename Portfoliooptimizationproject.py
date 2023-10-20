import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class PortfolioOptimization:
    def __init__(self, stock_symbols):
        self.stock_symbols = stock_symbols
        # Initialize any other necessary variables or data structures
        self.stock_data = {}  # Placeholder for storing fetched stock data
        self.returns_data = {}  # Placeholder for storing calculated returns data
        self.portfolios = {}  # Placeholder for storing constructed portfolios

    def fetch_stock_data(self):
        api_key = "TgRodikWHFRGhoE85aGqipHK9PZbHbtz"  # Replace with your actual API key from polygon.io

        for symbol in self.stock_symbols:
            url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/month/20180101/20231016?apiKey={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                # Assuming the API returns data in JSON format
                stock_data = response.json()
                self.stock_data[symbol] = stock_data
            else:
                print(f"Failed to fetch data for {symbol}. Status Code: {response.status_code}")

    def calculate_monthly_returns(self, stock_data, years=5):
        # Implement function to calculate monthly returns from stock data
        monthly_returns = {}

        for symbol, data in stock_data.items():
            monthly_returns[symbol] = []
            for i in range(1, len(data)):
                close_price_prev = data[i - 1]["c"]
                close_price_current = data[i]["c"]
                monthly_return = (close_price_current - close_price_prev) / close_price_prev
                monthly_returns[symbol].append(monthly_return)

        return monthly_returns

        pass

    def construct_naive_portfolio(self, returns_data):
        # Implement Naive portfolio construction
        num_stocks = len(returns_data)
        weight = 1.0 / num_stocks

        naive_portfolio = {}
        for symbol in returns_data:
            naive_portfolio[symbol] = weight

        return naive_portfolio
        pass

    def construct_min_variance_portfolio(self, returns_data):
        # Implement Minimum Variance portfolio construction
        returns = np.array(list(returns_data.values()))

        cov_matrix = np.cov(returns)
        inv_cov_matrix = np.linalg.inv(cov_matrix)

        weights = inv_cov_matrix.dot(np.ones(len(returns))) / (
            np.ones(len(returns)).dot(inv_cov_matrix).dot(np.ones(len(returns))))

        min_variance_portfolio = {}
        for i, symbol in enumerate(returns_data):
            min_variance_portfolio[symbol] = weights[i]

        return min_variance_portfolio
        pass

    def construct_tangent_portfolio(self, returns_data):
        # Implement Tangent portfolio construction
        returns = np.array(list(returns_data.values()))
        mean_returns = np.mean(returns, axis=1)
        cov_matrix = np.cov(returns)
        rf_rate = 0.02  # Risk-free rate, assuming 2% in this example

        weights = np.linalg.inv(cov_matrix).dot(mean_returns - rf_rate) / (
            np.ones(len(mean_returns)).dot(np.linalg.inv(cov_matrix)).dot(mean_returns - rf_rate))

        tangent_portfolio = {}
        for i, symbol in enumerate(returns_data):
            tangent_portfolio[symbol] = weights[i]

        return tangent_portfolio
        pass

    def monte_carlo_simulation(self, returns_data, num_simulations, years=2):
        # Implement Monte Carlo simulation for predicting future portfolio performance
        returns = np.array(list(returns_data.values()))

        mean_returns = np.mean(returns, axis=1)
        cov_matrix = np.cov(returns)

        portfolio_returns = []
        portfolio_volatility = []

        for _ in range(num_simulations):
            weights = np.random.random(len(mean_returns))
            weights /= np.sum(weights)

            portfolio_return = np.sum(weights * mean_returns) * years
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(years)

            portfolio_returns.append(portfolio_return)
            portfolio_volatility.append(portfolio_vol)

        return portfolio_returns, portfolio_volatility
        pass

class PortfolioGUI:
    def __init__(self, root, portfolio_optimizer):
        self.root = root
        self.root.title("Portfolio Optimization and Prediction")
        self.portfolio_optimizer = portfolio_optimizer
        # Initialize any other necessary variables or widgets

        self.create_gui_components()

    def create_gui_components(self):
        # Add widgets and components here for the GUI
        # ...

        # Example graph with Matplotlib
        fig, ax = plt.subplots()
        # Plotting example data, replace this with your own data
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    # Sample usage of classes
    stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "FB", "TSLA", "JPM", "V", "JNJ", "BABA"]
    portfolio_optimizer = PortfolioOptimization(stock_symbols)
    portfolio_gui_root = tk.Tk()
    portfolio_gui = PortfolioGUI(portfolio_gui_root, portfolio_optimizer)
    # Run the main event loop
    portfolio_gui_root.mainloop()





