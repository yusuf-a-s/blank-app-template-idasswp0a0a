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
    data = yf.download(ticker, start="2023-01-01", end="2023-12-31")
    spot_price = data['Adj Close'][-1]
    return spot_price

# Function to fetch risk-free rate (10-year government bond yield) from Yahoo Finance
def fetch_yield(currency):
    if currency == 'USD':
        ticker = '^TNX'  # US 10-year Treasury yield
    elif currency == 'EUR':
        ticker = 'BUND.DE'  # German 10-year Bund yield
    elif currency == 'JPY':
        ticker = '^JGB10Y'  # Japanese 10-year JGB yield
    else:
        st.warning(f'No bond yield data available for {currency}. Using default risk-free rate.')
        return 0.02  # Default risk-free rate if no data is available
    
    data = yf.download(ticker, start="2023-01-01", end="2023-12-31")
    yield_rate = data['Adj Close'][-1] / 100  # Convert percentage to decimal
    return yield_rate

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

# Input currency
st.header('Currency Option')
currency = st.selectbox('Select Currency', ['USD', 'EUR', 'JPY'])

# Fetch spot prices from Yahoo Finance
st.header('Market Data')
spot_prices = []
for underlying in underlyings:
    spot_price = fetch_data(underlying)
    spot_prices.append(spot_price)
    st.write(f'Spot Price for {underlying}: {spot_price:.2f}')

# Fetch risk-free rate (10-year government bond yield)
risk_free_rate = fetch_yield(currency)
st.write(f'Risk-Free Rate (10-year {currency} Bond Yield): {risk_free_rate:.2%}')

# Calculate the coupon
if st.button('Calculate Coupon'):
    coupon = 0
    T = tenor
    r = risk_free_rate
    for i, underlying in enumerate(underlyings):
        S = spot_prices[i]
        K = put_strike
        sigma = 0.2  # Hardcoded volatility for demonstration
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
4. Select the currency for which you want to fetch the risk-free rate.
5. The spot prices will be fetched automatically from Yahoo Finance.
6. The risk-free rate will be fetched based on the 10-year government bond yield of the selected currency.
7. Click 'Calculate Coupon' to get the coupon price for the structured product.
""")
