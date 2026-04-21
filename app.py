import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Track 4: Stock Portfolio Tool", layout="wide")
st.title("Stock Portfolio Analysis Tool (ATVI vs RBLX)")
st.subheader("Track 4 - Interactive Python Tool")

# ----------------------
# Load data
# ----------------------
df = pd.read_csv("RBLX_ATVI.csv.csv")

df_atvi = df[df["Ticker"] == "ATVI"].copy()
df_rblx = df[df["Ticker"] == "RBLX"].copy()

df_atvi["DlyCalDt"] = pd.to_datetime(df_atvi["DlyCalDt"])
df_rblx["DlyCalDt"] = pd.to_datetime(df_rblx["DlyCalDt"])

df_atvi.set_index("DlyCalDt", inplace=True)
df_rblx.set_index("DlyCalDt", inplace=True)

# Align dates
combined = pd.DataFrame({
    "ret_ATVI": df_atvi["DlyRetx"],
    "ret_RBLX": df_rblx["DlyRetx"]
}).dropna()

# ----------------------
# Interactive weight slider
# ----------------------
st.sidebar.header("Portfolio Weight")
w_atvi = st.sidebar.slider("Weight of ATVI (%)", 0, 100, 50)
w_rblx = 100 - w_atvi

w1 = w_atvi / 100
w2 = w_rblx / 100

combined["ret_Portfolio"] = w1 * combined["ret_ATVI"] + w2 * combined["ret_RBLX"]

# ----------------------
# Metrics
# ----------------------
mean_atvi = combined["ret_ATVI"].mean()
mean_rblx = combined["ret_RBLX"].mean()
mean_port = combined["ret_Portfolio"].mean()

std_atvi = combined["ret_ATVI"].std()
std_rblx = combined["ret_RBLX"].std()
std_port = combined["ret_Portfolio"].std()

sharpe_atvi = mean_atvi / std_atvi
sharpe_rblx = mean_rblx / std_rblx
sharpe_port = mean_port / std_port

# ----------------------
# Show metrics table
# ----------------------
st.subheader("Key Performance Metrics")
metrics_df = pd.DataFrame({
    "Stock": ["ATVI", "RBLX", "Portfolio"],
    "Mean Return": [mean_atvi, mean_rblx, mean_port],
    "Std (Risk)": [std_atvi, std_rblx, std_port],
    "Sharpe Ratio": [sharpe_atvi, sharpe_rblx, sharpe_port]
})
st.dataframe(metrics_df.round(6))

# ----------------------
# Plot 1: Price Trend
# ----------------------
st.subheader("Stock Price Trend")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df_atvi["DlyPrc"], label="ATVI", color="blue")
ax1.plot(df_rblx["DlyPrc"], label="RBLX", color="red")
ax1.set_title("Price Comparison")
ax1.set_xlabel("Date")
ax1.set_ylabel("Price")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ----------------------
# Plot 2: Return Distribution
# ----------------------
st.subheader("Return Distribution Comparison")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.hist(combined["ret_ATVI"], bins=40, alpha=0.5, label="ATVI", color="blue")
ax2.hist(combined["ret_RBLX"], bins=40, alpha=0.5, label="RBLX", color="red")
ax2.hist(combined["ret_Portfolio"], bins=40, alpha=0.5, label="Portfolio", color="purple")
ax2.set_title("Return Distribution")
ax2.set_xlabel("Daily Return")
ax2.set_ylabel("Frequency")
ax2.legend()
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ----------------------
# Plot 3: Metrics Bar Chart
# ----------------------
st.subheader("Metrics Bar Chart (Return / Risk / Sharpe)")
labels = ["Mean Return", "Std (Risk)", "Sharpe Ratio"]
atvi_vals = [mean_atvi, std_atvi, sharpe_atvi]
rblx_vals = [mean_rblx, std_rblx, sharpe_rblx]
port_vals = [mean_port, std_port, sharpe_port]

x = [0, 1, 2]
width = 0.25

fig3, ax3 = plt.subplots(figsize=(11, 6))
ax3.bar([i-width for i in x], atvi_vals, width, label="ATVI", color="blue")
ax3.bar(x, rblx_vals, width, label="RBLX", color="red")
ax3.bar([i+width for i in x], port_vals, width, label="Portfolio", color="purple")
ax3.set_xticks(x)
ax3.set_xticklabels(labels)
ax3.set_title("Track 4 Comparison")
ax3.legend()
ax3.grid(axis='y', alpha=0.3)
st.pyplot(fig3)

st.sidebar.info("This is an interactive tool for Track 4: Portfolio Diversification Analysis")