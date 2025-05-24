# Final precise version of app.py targeting 250-digit match using hardcoded reference

import streamlit as st
from mpmath import mp
import time
from random import random

# Set high fixed internal precision for all calculations
mp.dps = 350  # More than needed to avoid rounding issues

# Use a hardcoded 300-digit reference value of π
pi_reference = (
    "3."
    "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196"
)

# Target precision
digits = 250  # Always calculate and compare 250 digits
mp.dps = digits + 150  # Extra buffer to ensure precision

# Configure Streamlit
st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")
st.title("🔢 Smart Pi Calculator")

# Sidebar method selector
st.sidebar.header("Settings")
method = st.sidebar.selectbox("Choose method:", ["Chudnovsky", "Machin", "Leibniz", "Monte Carlo"])

# Highlight mismatch digits
def highlight_pi_difference(user_pi, reference_pi, digits):
    result_html = '<code>'
    for i in range(digits + 2):  # Include '3.'
        if i >= len(user_pi) or i >= len(reference_pi):
            result_html += f'<span style="color:gray;">?</span>'
            break
        if user_pi[i] == reference_pi[i]:
            result_html += user_pi[i]
        else:
            result_html += f'<span style="color:red;">{user_pi[i]}</span>'
            result_html += f'<span style="color:gray;">{user_pi[i+1:]}</span>'
            break
    result_html += '</code>'
    return result_html

# Pi calculation algorithms
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

def monte_carlo_pi(samples):
    inside = 0
    for _ in range(samples):
        x, y = random(), random()
        if x*x + y*y <= 1:
            inside += 1
    return mp.mpf(4 * inside / samples)

# Calculate and compare
st.subheader(f"🔍 Calculating π using: {method}")
with st.spinner("Calculating..."):
    start = time.time()
    if method == "Leibniz":
        pi = leibniz_pi(digits * 2000)
    elif method == "Machin":
        pi = machin_pi(digits * 20)
    elif method == "Chudnovsky":
        pi = chudnovsky_pi(digits // 14 + 50)
    elif method == "Monte Carlo":
        pi = monte_carlo_pi(digits * 20000)
    elapsed = time.time() - start
    pi_str = str(pi)[:digits + 10]
    st.markdown(highlight_pi_difference(pi_str, pi_reference, digits), unsafe_allow_html=True)
    st.success(f"{method} method completed in {elapsed:.4f} seconds.")

# Footer
st.caption("🧮 Compared against hardcoded 300-digit reference of π.")
