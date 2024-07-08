import math
import yfinance as yf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st

# Function to calculate the d1 and d2 parameters
def calculate_d1_d2(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return d1, d2

# Function to calculate the price of a European call option
def call_option_price(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price

# Function to calculate the price of a European put option
def put_option_price(S, K, T, r, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# Function to fetch historical data and calculate volatility
def fetch_volatility(ticker):
    # Fetch historical data for the last year
    data = yf.download(ticker, period="1y")["Adj Close"].dropna()
    
    # Calculate daily returns
    returns = data.pct_change().dropna()
    
    # Annualized volatility
    volatility = returns.std() * np.sqrt(252)
    
    return volatility[-1]  # Return the most recent volatility

# Streamlit interface
st.title("Black-Scholes Option Pricing Calculator")

# Allow user to input a ticker symbol
ticker = st.text_input("Enter a ticker symbol (e.g., AAPL):")

# Fetch price and volatility data if ticker is provided
if ticker:
    try:
        underlying = yf.Ticker(ticker)
        current_price = underlying.history(period="1d")["Close"].iloc[-1]
        volatility = fetch_volatility(ticker)
        
        st.write(f"Current Price ({ticker}): ${current_price:.2f}")
        st.write(f"Current Volatility ({ticker}): {volatility:.2%}")
        
        # User inputs for option pricing
        S = st.number_input("Current stock price (S):", value=current_price, min_value=0.0)
        K = st.number_input("Strike price (K):", value=current_price, min_value=0.0)
        T = st.number_input("Time to maturity (T) in years:", value=1.0, min_value=0.0)
        r = st.number_input("Risk-free interest rate (r):", value=0.05, min_value=0.0, max_value=1.0)
        sigma = st.number_input("Volatility (sigma):", value=volatility, min_value=0.0, max_value=1.0)
        
        if st.button("Calculate"):
            call_price = call_option_price(S, K, T, r, sigma)
            put_price = put_option_price(S, K, T, r, sigma)
            
            st.markdown(f"<div style='padding: 10px; background-color: #dff0d8; border-radius: 5px; border: 1px solid #d6e9c6;'>Call Option Price: <b>${call_price:.2f}</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='padding: 10px; background-color: #f2dede; border-radius: 5px; border: 1px solid #ebccd1;'>Put Option Price: <b>${put_price:.2f}</b></div>", unsafe_allow_html=True)
            
            st.subheader("Option Price Heatmaps")
            
            # Generate heatmaps
            spot_prices = np.linspace(S * 0.5, S * 1.5, 50)
            volatilities = np.linspace(sigma * 0.5, sigma * 1.5, 50)
            
            call_prices = np.zeros((len(spot_prices), len(volatilities)))
            put_prices = np.zeros((len(spot_prices), len(volatilities)))
            
            for i, sp in enumerate(spot_prices):
                for j, vol in enumerate(volatilities):
                    call_prices[i, j] = call_option_price(sp, K, T, r, vol)
                    put_prices[i, j] = put_option_price(sp, K, T, r, vol)
            
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))
            
            sns.heatmap(call_prices, ax=ax[0], cmap="YlGnBu", xticklabels=np.round(volatilities, 2), yticklabels=np.round(spot_prices, 2))
            ax[0].set_title("Call Option Prices")
            ax[0].set_xlabel("Volatility")
            ax[0].set_ylabel("Spot Price")
            
            sns.heatmap(put_prices, ax=ax[1], cmap="YlOrRd", xticklabels=np.round(volatilities, 2), yticklabels=np.round(spot_prices, 2))
            ax[1].set_title("Put Option Prices")
            ax[1].set_xlabel("Volatility")
            ax[1].set_ylabel("Spot Price")
            
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
