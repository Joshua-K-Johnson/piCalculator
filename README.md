# 🧮 High-Precision Pi Calculator

A Python + Streamlit web app that calculates the value of π (Pi) to up to 300 digits using multiple algorithms, with real-time performance feedback and visual highlighting of digit accuracy.

🔗 **Live App**: [picalculator.streamlit.app](https://picalculator.streamlit.app)

---

## 🚀 Features

- Calculate π to up to **300 digits**
- **Auto-selects the most efficient algorithm** based on your input
- Option to **manually compare** different methods:
  - Leibniz Series
  - Machin Formula
  - Chudnovsky Algorithm
  - Monte Carlo Method
- Highlights the **first incorrect digit in red**
- Displays **calculation time**
- Lightweight and accessible from any device

---

## 🧠 How to Use

1. Visit [https://picalculator.streamlit.app](https://picalculator.streamlit.app)
2. Use the **slider in the sidebar** to select the number of digits (1–300)
3. View the result in Smart Mode, or enable **“Compare with custom method”** to try different algorithms
4. Observe:
   - The result
   - Which algorithm was used
   - Calculation time
   - Visual feedback on where the output diverges from the true value of π

---

## ⚙️ Tech Stack

- **Python 3**
- **Streamlit**
- **mpmath** (for arbitrary precision math)
- Optional: Run locally using:

```bash
pip install streamlit mpmath
streamlit run app.py
