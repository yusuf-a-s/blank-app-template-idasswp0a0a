import streamlit as st
import numpy as np
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

# Input market data
st.header('Market Data')
spot_prices = [st.number_input(f'Spot Price for {underlying}', value=100.0) for underlying in underlyings]
volatilities = [st.number_input(f'Volatility for {underlying}', value=0.2) for underlying in underlyings]
interest_rate = st.number_input('Risk-Free Interest Rate', value=0.05)
time_to_maturity = st.number_input('Time to Maturity (in years)', value=1.0)

# Calculate the coupon
if st.button('Calculate Coupon'):
    coupon = 0
    for i, underlying in enumerate(underlyings):
        S = spot_prices[i]
        K = put_strike
        T = time_to_maturity
        r = interest_rate
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
2. Input the put strike and autocall barrier values.
3. Provide the spot prices, volatilities, and risk-free interest rate.
4. Click 'Calculate Coupon' to get the coupon price for the structured product.
""")
