import streamlit as st
from mpmath import mp
import time
from random import random

# Configure page
st.set_page_config(page_title="Smart Pi Calculator", page_icon="🔢")
st.title("🔢 Smart Pi Calculator")

# Sidebar input
st.sidebar.header("Settings")
digits = st.sidebar.slider("How many digits of π do you want?", 1, 300, 50)

# Auto-selection logic
if digits <= 10:
    method = "Machin"
elif digits <= 40:
    method = "Machin"
else:
    method = "Chudnovsky"

st.sidebar.markdown(f"**Auto-selected method:** `{method}`")

# Manual method toggle
enable_manual = st.sidebar.checkbox("🧪 Compare with custom method")
if enable_manual:
    manual_method = st.sidebar.selectbox("Select a method to compare:", ["Leibniz", "Machin", "Chudnovsky", "Monte Carlo"])
else:
    manual_method = None

# Set high fixed precision for the reference value
mp.dps = 350
pi_reference = str(mp.pi)

# Reset precision to a dynamic level for calculation
internal_buffer = max(100, digits // 2)
mp.dps = digits + internal_buffer


# Highlight incorrect digits
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

# Pi calculation methods
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

# Smart result section
st.subheader("🎯 Smart Mode Result")
with st.spinner("Calculating..."):
    start = time.time()
    if method == "Leibniz":
        terms = digits * 800
        pi = leibniz_pi(terms)
    elif method == "Machin":
        terms = digits * 12
        pi = machin_pi(terms)
    else:
        terms = digits // 14 + 20
        pi = chudnovsky_pi(terms)
    elapsed = time.time() - start
    pi_str = str(pi)[:digits + 10]
    st.markdown(highlight_pi_difference(pi_str, pi_reference, digits), unsafe_allow_html=True)
    st.success(f"Smart method completed in {elapsed:.4f} seconds.")

# Manual method comparison
if enable_manual:
    st.subheader(f"🧪 Manual Comparison: {manual_method}")
    with st.spinner("Calculating..."):
        start = time.time()
        if manual_method == "Leibniz":
            terms = digits * 800
            pi_manual = leibniz_pi(terms)
        elif manual_method == "Machin":
            terms = digits * 12
            pi_manual = machin_pi(terms)
        elif manual_method == "Chudnovsky":
            terms = digits // 14 + 20
            pi_manual = chudnovsky_pi(terms)
        elif manual_method == "Monte Carlo":
            pi_manual = monte_carlo_pi(digits * 10000)
        elapsed_manual = time.time() - start
        pi_str_manual = str(pi_manual)[:digits + 10]
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
st.caption("🧮 All results are compared to `mpmath.pi`, accurate to over 200 digits.")
