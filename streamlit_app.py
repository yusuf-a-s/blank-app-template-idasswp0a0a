import math
from scipy.stats import norm
import tkinter as tk
from tkinter import messagebox

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

# Function to update the option prices
def update_prices():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        sigma = float(entry_sigma.get())

        call_price = call_option_price(S, K, T, r, sigma)
        put_price = put_option_price(S, K, T, r, sigma)

        label_call_price.config(text=f"Call Option Price: {call_price:.2f}")
        label_put_price.config(text=f"Put Option Price: {put_price:.2f}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for all fields")

# Create the main window
root = tk.Tk()
root.title("Black-Scholes Option Pricing")

# Create and place the input fields and labels
tk.Label(root, text="Stock Price (S):").grid(row=0, column=0, padx=10, pady=10)
entry_S = tk.Entry(root)
entry_S.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Strike Price (K):").grid(row=1, column=0, padx=10, pady=10)
entry_K = tk.Entry(root)
entry_K.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Time to Maturity (T):").grid(row=2, column=0, padx=10, pady=10)
entry_T = tk.Entry(root)
entry_T.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Risk-free Rate (r):").grid(row=3, column=0, padx=10, pady=10)
entry_r = tk.Entry(root)
entry_r.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Volatility (sigma):").grid(row=4, column=0, padx=10, pady=10)
entry_sigma = tk.Entry(root)
entry_sigma.grid(row=4, column=1, padx=10, pady=10)

# Create and place the button to calculate prices
button_calculate = tk.Button(root, text="Calculate", command=update_prices)
button_calculate.grid(row=5, columnspan=2, pady=10)

# Create and place the labels to display the results
label_call_price = tk.Label(root, text="Call Option Price: N/A")
label_call_price.grid(row=6, columnspan=2, pady=10)

label_put_price = tk.Label(root, text="Put Option Price: N/A")
label_put_price.grid(row=7, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
