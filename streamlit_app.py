import streamlit as st
import numpy as np
import yfinance as yf
from scipy.stats import norm

# Function to calculate the Black-Scholes option price
def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Function to fetch data from Yahoo Finance
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    spot_price = hist['Close'][-1]
    vol = hist['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
    return spot_price, vol

# Streamlit app
st.title('Phoenix Memory Structured Product Pricing')

# Input the underlyings
st.header('Underlyings')
underlyings = []
for i in range(1, 4):
    underlying = st.text_input(f'Underlying {i} Ticker', key=f'underlying_{i}')
    if underlying:
        underlyings.append(underlying)

# Input strikes and barriers
st.header('Strikes and Barriers')
put_strike = st.number_input('Put Strike', value=90)
autocall_barrier = st.number_input('Autocall Barrier', value=110)
coupon_barrier = st.number_input('Coupon Barrier', value=95)

# Input observation frequency and tenor
st.header('Observation Frequency and Tenor')
observation_frequency = st.number_input('Observation Frequency (times per year)', value=4)
tenor = st.number_input('Tenor (in years)', value=1.0)

# Input market data
st.header('Market Data')
interest_rate = st.number_input('Risk-Free Interest Rate', value=0.05)

# Fetch spot prices and volatilities from Yahoo Finance
spot_prices = []
volatilities = []
for underlying in underlyings:
    spot_price, vol = fetch_data(underlying)
    spot_prices.append(spot_price)
    volatilities.append(vol)
    st.write(f'Spot Price for {underlying}: {spot_price:.2f}')
    st.write(f'Volatility for {underlying}: {vol:.2%}')

# Calculate the coupon
if st.button('Calculate Coupon'):
    coupon = 0
    T = tenor
    r = interest_rate
    for i, underlying in enumerate(underlyings):
        S = spot_prices[i]
        K = put_strike
        sigma = volatilities[i]
        put_price = black_scholes(S, K, T, r, sigma, option_type="put")
        autocall_price = black_scholes(S, autocall_barrier, T, r, sigma, option_type="call")
        coupon += (put_price + autocall_price) / len(underlyings)
    
    st.subheader('Coupon Price')
    st.write(f'The coupon price for the Phoenix Memory Structured Product is: {coupon:.2f}')

# Instructions for the user
st.write("""
**Instructions:**
1. Enter the ticker symbols for up to three underlying stocks.
2. Input the put strike, autocall barrier, and coupon barrier values.
3. Provide the observation frequency and tenor.
4. The spot prices and volatilities will be fetched automatically from Yahoo Finance.
5. Provide the risk-free interest rate.
6. Click 'Calculate Coupon' to get the coupon price for the structured product.
""")
