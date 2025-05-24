# Final version of app.py with fixed 250-digit accuracy enforcement

import streamlit as st
from mpmath import mp
import time
from random import random

# Reference setup
mp.dps = 350
pi_reference = str(mp.pi)

# Display precision fixed
digits = 250

# Set precision for calculation
mp.dps = digits + 100

# Streamlit page config
st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")
st.title("🔢 Smart Pi Calculator")

# Sidebar options
st.sidebar.header("Settings")
method = st.sidebar.selectbox("Choose method (auto-default is Chudnovsky):", ["Chudnovsky", "Machin", "Leibniz", "Monte Carlo"])

# Highlight comparison
def highlight_pi_difference(user_pi, reference_pi, digits):
    result_html = '<code>'
    for i in range(digits + 2):  # Include "3."
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

# Algorithms
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

# Run selected method
st.subheader(f"🔍 Result Using: {method}")
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
st.caption("🧮 Compared against mpmath.pi accurate to 300+ digits.")
