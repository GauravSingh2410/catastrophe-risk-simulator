import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# PAGE CONFIG
st.set_page_config(page_title="CAT Risk Dashboard", layout="wide")

# TITLE & INTRO
st.title("Catastrophe Risk Simulator")

st.markdown("""
### Overview
This interactive dashboard by **Gaurav Singh** simulates **catastrophe losses** using Monte Carlo simulation.

It helps estimate:
- **Expected Annual Loss (EAL)** = average yearly loss  
- **Probable Maximum Loss (PML)** = extreme loss scenarios  
- Impact of **insurance & reinsurance**

""")

st.markdown("""
I built an interactive catastrophe risk model using Monte Carlo simulation where I modeled event frequency 
using a Poisson distribution and severity using a lognormal distribution. 
The dashboard calculates EAL and PML and shows how insurance and reinsurance reduce losses..""")

st.divider()

# SIDEBAR INPUTS
st.sidebar.info("Adjust parameters to simulate different catastrophe scenarios.")

st.sidebar.header("The Simulation Settings")

years = st.sidebar.slider("Simulation Years", 1000, 50000, 10000)
portfolio = st.sidebar.number_input("Portfolio Value (₹)", value=1_000_000_000)

mean_damage = st.sidebar.slider("Mean Damage Ratio", 0.0, 0.2, 0.02)
std_damage = st.sidebar.slider("Volatility", 0.0, 0.2, 0.05)
lambda_events = st.sidebar.slider("Event Frequency (λ)", 0.5, 5.0, 2.0)

st.sidebar.header("The Insurance Settings")

deductible = st.sidebar.number_input("Deductible (₹)", value=10_000_000)
limit = st.sidebar.number_input("Policy Limit (₹)", value=100_000_000)

st.sidebar.header("The Reinsurance Settings")

reins_retention = st.sidebar.number_input("Reinsurance Retention (₹)", value=100_000_000)
reins_limit = st.sidebar.number_input("Reinsurance Limit (₹)", value=200_000_000)


# SIMULATION
np.random.seed(42)

annual_losses = []

for _ in range(years):
    events = np.random.poisson(lambda_events)
    
    if events > 0:
        losses = np.random.lognormal(
            mean=np.log(mean_damage + 1e-6),
            sigma=std_damage,
            size=events
        )
        total_loss = losses.sum() * portfolio
    else:
        total_loss = 0
        
    annual_losses.append(total_loss)

annual_losses = np.array(annual_losses)


# INSURANCE CALCULATIONS
insured_loss = np.maximum(annual_losses - deductible, 0)
insured_loss = np.minimum(insured_loss, limit)

# Reinsurance
reinsurer_payout = np.clip(annual_losses - reins_retention, 0, reins_limit)

net_loss = insured_loss - reinsurer_payout
net_loss = np.maximum(net_loss, 0)


# METRICS FUNCTION
def calculate_metrics(data):
    return {
        "EAL": np.mean(data),
        "PML_95": np.percentile(data, 95),
        "PML_99": np.percentile(data, 99)
    }

gross = calculate_metrics(annual_losses)
insured = calculate_metrics(insured_loss)
net = calculate_metrics(net_loss)


# METRICS DISPLAY
st.subheader("Key Risk Metrics (Gross Loss)")

col1, col2, col3 = st.columns(3)

col1.metric("EAL (Avg Loss)", f"₹{gross['EAL']:,.0f}")
col2.metric("PML 95%", f"₹{gross['PML_95']:,.0f}")
col3.metric("PML 99%", f"₹{gross['PML_99']:,.0f}")

st.info("""
**EAL** = average expected yearly loss  
**PML 95%** = loss exceeded only 5% of the time  
**PML 99%** = extreme worst-case scenario  
""")

# TABLE
st.subheader("Loss Comparison")

df = pd.DataFrame(
    [gross, insured, net],
    index=["Gross", "After Insurance", "After Reinsurance"]
)

st.dataframe(df.style.format("{:,.0f}"))

st.caption("Comparison of losses at different stages: Gross → After Insurance → After Reinsurance")


# PLOT
st.subheader("Loss Distribution Analysis")

fig = go.Figure()

fig.add_trace(go.Histogram(x=annual_losses, name="Gross Loss", opacity=0.5))
fig.add_trace(go.Histogram(x=insured_loss, name="After Insurance", opacity=0.5))
fig.add_trace(go.Histogram(x=net_loss, name="After Reinsurance", opacity=0.5))

fig.update_layout(
    barmode="overlay",
    xaxis_title="Loss Amount (₹)",
    yaxis_title="Frequency",
    legend_title="Loss Type",
    template="plotly_white"
)

st.plotly_chart(fig, width='stretch')

# INSIGHTS
st.subheader("Key Insights")

st.markdown("""
- Increasing **event frequency (λ)** increases total losses  
- Higher **damage ratio** increases extreme losses (PML)  
- **Insurance** reduces moderate losses  
- **Reinsurance** protects against large catastrophic losses  
""")
