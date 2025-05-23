import streamlit as st
from mpmath import mp
import time

# Page config
st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")

# Title
st.title("🔢 Smart Pi Calculator")

# Sidebar: User Input
st.sidebar.header("Settings")
digits = st.sidebar.slider("How many digits of π do you want?", 1, 200, 50)

# Automatically choose method
if digits <= 10:
    method = "Machin"
elif digits <= 40:
    method = "Machin"
else:
    method = "Chudnovsky"

st.sidebar.write(f"Algorithm chosen: **{method}**")

# Set precision
mp.dps = digits + 5  # extra buffer to ensure final digit accuracy

# Pi Calculation Functions
def leibniz_pi(n_terms):
    pi = mp.mpf(0)
    for k in range(n_terms):
        pi += (-1) ** k / (2 * k + 1)
    return 4 * pi

def machin_pi(terms):
    def arctan(x, terms):
        x = mp.mpf(x)
        total = mp.mpf(0)
        for k in range(terms):
            term = (-1)**k * (x ** (2*k + 1)) / (2*k + 1)
            total += term
        return total
    return 16 * arctan(1/5, terms) - 4 * arctan(1/239, terms)

def chudnovsky_pi(terms):
    C = 426880 * mp.sqrt(10005)
    M = 1
    L = 13591409
    X = 1
    K = 6
    S = L
    for i in range(1, terms):
        M = (M * (K ** 3 - 16 * K)) // (i ** 3)
        L += 545140134
        X *= -262537412640768000
        S += (M * L) / X
        K += 12
    return C / S

# Trigger calculation
st.subheader("Result")

with st.spinner("Calculating..."):
    start = time.time()
    
    if method == "Leibniz":
        terms = digits * 100  # very slow converging
        pi = leibniz_pi(terms)
    elif method == "Machin":
        terms = digits + 10  # generally safe
        pi = machin_pi(terms)
    elif method == "Chudnovsky":
        terms = digits // 14 + 2  # ~14 digits per term
        pi = chudnovsky_pi(terms)
    
    elapsed = time.time() - start
    pi_str = str(pi)[:digits + 2]  # include "3."
    st.code(pi_str)

st.success(f"Done in {elapsed:.4f} seconds ✅")

# Optional: Copy/share
st.caption("Built with 🧠 by [You] using Streamlit & mpmath")
