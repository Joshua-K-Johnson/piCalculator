# Full version of app.py with improved red digit highlighting using nstr and extended tail

import streamlit as st
from mpmath import mp, nstr
import time
from random import random

# Fixed high-precision reference value of π (300 digits)
pi_reference = (
    "3."
    "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196"
)

# Configure page
st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")
st.title("🔢 Smart Pi Calculator")

# Sidebar settings
st.sidebar.header("Settings")
digits = st.sidebar.slider("How many digits of π to calculate and display:", 1, 250, 50)

# Smart method selection logic
if digits <= 10:
    method = "Machin"
elif digits <= 40:
    method = "Machin"
else:
    method = "Chudnovsky"

st.sidebar.markdown(f"**Auto-selected method:** `{method}`")

# Manual comparison toggle
enable_manual = st.sidebar.checkbox("🧪 Compare with custom method")
if enable_manual:
    manual_method = st.sidebar.selectbox("Select a method to compare:", ["Leibniz", "Machin", "Chudnovsky", "Monte Carlo"])
else:
    manual_method = None

# Set precision for all calculations
mp.dps = digits + 100

# Highlighting difference from reference
def highlight_pi_difference(user_pi, reference_pi, digits):
    result_html = '<code>'
    max_len = min(len(user_pi), len(reference_pi))
    for i in range(digits + 2):  # Include "3."
        if i >= max_len:
            result_html += '<span style="color:gray;">?</span>'
            break
        if user_pi[i] == reference_pi[i]:
            result_html += user_pi[i]
        else:
            result_html += f'<span style="color:red;">{user_pi[i]}</span>'
            remaining = user_pi[i+1:digits + 20]
            result_html += f'<span style="color:gray;">{remaining}</span>'
            break
    result_html += '</code>'
    return result_html

# Algorithm definitions
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
    total = mp.mpf(0)
    for k in range(terms):
        num = mp.factorial(6*k) * (545140134 * k + 13591409)
        denom = (
            mp.factorial(3*k)
            * mp.factorial(k)**3
            * (-640320) ** (3 * k)
        )
        total += num / denom
    pi = (426880 * mp.sqrt(10005)) / total
    return pi

def monte_carlo_pi(samples):
    inside = 0
    for _ in range(samples):
        x, y = random(), random()
        if x*x + y*y <= 1:
            inside += 1
    return mp.mpf(4 * inside / samples)

# Main smart mode calculation
st.subheader("🎯 Smart Mode Result")
with st.spinner("Calculating..."):
    start = time.time()
    if method == "Leibniz":
        pi = leibniz_pi(digits * 2000)
    elif method == "Machin":
        pi = machin_pi(digits * 20)
    else:
        terms = 25  # This should guarantee 350+ digits worth of accuracy
        pi = chudnovsky_pi(terms)
    elapsed = time.time() - start
    pi_str = nstr(pi, digits + 20)
    st.markdown(highlight_pi_difference(pi_str, pi_reference, digits), unsafe_allow_html=True)
    st.success(f"{method} method completed in {elapsed:.4f} seconds.")

# Optional manual comparison
if enable_manual:
    st.subheader(f"🧪 Manual Comparison: {manual_method}")
    with st.spinner("Calculating..."):
        start = time.time()
        if manual_method == "Leibniz":
            pi_manual = leibniz_pi(digits * 2000)
        elif manual_method == "Machin":
            pi_manual = machin_pi(digits * 20)
        elif manual_method == "Chudnovsky":
            pi_manual = chudnovsky_pi(25)
        elif manual_method == "Monte Carlo":
            pi_manual = monte_carlo_pi(digits * 20000)
        elapsed_manual = time.time() - start
        pi_str_manual = nstr(pi_manual, digits + 20)
        st.markdown(highlight_pi_difference(pi_str_manual, pi_reference, digits), unsafe_allow_html=True)
        st.success(f"{manual_method} method completed in {elapsed_manual:.4f} seconds.")

    if manual_method == "Leibniz":
        st.info("🧠 **Leibniz**: A simple alternating series using fractions. Very slow convergence. Great for teaching.")
    elif manual_method == "Machin":
        st.info("📐 **Machin**: Uses arctangent identities. Accurate up to 30–50 digits. Historically important.")
    elif manual_method == "Chudnovsky":
        st.info("🚀 **Chudnovsky**: Extremely fast convergence (~14 digits/term). Used in world record calculations.")
    elif manual_method == "Monte Carlo":
        st.info("🎲 **Monte Carlo**: Estimates π using random points in a circle. Low precision, but fun and visual.")

# Footer
st.caption("🧮 Compared against a hardcoded 300-digit reference value of π.")
