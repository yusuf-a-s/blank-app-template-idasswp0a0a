import math
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

# Streamlit interface
st.title("Black-Scholes Option Pricing Calculator")

S = st.number_input("Current stock price (S):", value=100.0, min_value=0.0)
K = st.number_input("Strike price (K):", value=100.0, min_value=0.0)
T = st.number_input("Time to maturity (T) in years:", value=1.0, min_value=0.0)
r = st.number_input("Risk-free interest rate (r):", value=0.05, min_value=0.0, max_value=1.0)
sigma = st.number_input("Volatility (sigma):", value=0.2, min_value=0.0, max_value=1.0)

if st.button("Calculate"):
    call_price = call_option_price(S, K, T, r, sigma)
    put_price = put_option_price(S, K, T, r, sigma)
    
    st.write(f"Call Option Price: {call_price:.2f}")
    st.write(f"Put Option Price: {put_price:.2f}")
