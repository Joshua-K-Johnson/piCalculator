# Updated Streamlit app with auto and manual method selection including timing
import streamlit as st
from mpmath import mp
import time

st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")
st.title("🔢 Smart Pi Calculator")

# Sidebar: User input for digits
st.sidebar.header("Settings")
digits = st.sidebar.slider("How many digits of π do you want?", 1, 200, 50)

# Auto-method selection
if digits <= 10:
    method = "Machin"
elif digits <= 40:
    method = "Machin"
else:
    method = "Chudnovsky"

st.sidebar.write(f"Auto-selected method: **{method}**")

# Set precision
mp.dps = digits + 5

# Pi Calculation Methods
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
    from random import random
    inside = 0
    for _ in range(samples):
        x, y = random(), random()
        if x*x + y*y <= 1:
            inside += 1
    return mp.mpf(4 * inside / samples)

# Smart calculation
st.subheader("🎯 Smart Mode Result")
with st.spinner("Calculating (smart selection)..."):
    start = time.time()
    if method == "Leibniz":
        terms = digits * 100
        pi = leibniz_pi(terms)
    elif method == "Machin":
        terms = digits + 10
        pi = machin_pi(terms)
    else:
        terms = digits // 14 + 2
        pi = chudnovsky_pi(terms)
    elapsed = time.time() - start
    st.code(str(pi)[:digits + 2])
    st.success(f"Completed in {elapsed:.4f} seconds")

# Manual comparison section
with st.expander("🧪 Compare Algorithms Manually (Optional)"):
    manual_method = st.selectbox("Choose a method to compare:", ["Leibniz", "Machin", "Chudnovsky", "Monte Carlo"])
    if st.button("Recalculate with selected method"):
        with st.spinner("Calculating..."):
            start = time.time()
            if manual_method == "Leibniz":
                terms = digits * 100
                pi_manual = leibniz_pi(terms)
            elif manual_method == "Machin":
                terms = digits + 10
                pi_manual = machin_pi(terms)
            elif manual_method == "Chudnovsky":
                terms = digits // 14 + 2
                pi_manual = chudnovsky_pi(terms)
            elif manual_method == "Monte Carlo":
                pi_manual = monte_carlo_pi(digits * 10000)
            elapsed_manual = time.time() - start
            st.code(str(pi_manual)[:digits + 2])
            st.success(f"{manual_method} took {elapsed_manual:.4f} seconds")

st.caption("Built with ❤️ using Streamlit & mpmath")
