import streamlit as st
import math
from scipy.stats import norm

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

# Placeholder numbers for required variables
S = 150     # Current stock price
K = 100     # Strike price
T = 1       # Time to maturity in years
r = 0.05    # Risk-free interest rate (5%)
sigma = 0.2 # Volatility of the stock (20%)

# Calculate call and put option prices
call_price = call_option_price(S, K, T, r, sigma)
put_price = put_option_price(S, K, T, r, sigma)

print(f"Call Option Price: {call_price:.2f}")
print(f"Put Option Price: {put_price:.2f}")
