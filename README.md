# Catastrophe Risk Simulator

An interactive catastrophe risk model that simulates portfolio losses under extreme events and evaluates the impact of **insurance and reinsurance structures**.
The dashboard calculates EAL and PML and shows how insurance and reinsurance reduce losses.
Built using Python & Streamlit by **Gaurav Singh**

---

## Business Context

In the insurance and reinsurance industry, a key challenge is quantifying **low-frequency, high-severity risks** such as earthquakes, floods and cyclones.

Simple averages are insufficient because they fail to capture **extreme loss scenarios (tail risk)**.

This project presents a **simplified, simulation-based approach** to catastrophe risk modeling by:

- Simulating multiple years of stochastic events  
- Modeling uncertainty in both frequency and severity  
- Evaluating how insurance and reinsurance affect loss outcomes  

> The focus is on understanding **loss distributions**.

---

## Modeling Approach

The model uses a **Monte Carlo simulation framework**.

### 1. Event Frequency
- Modeled using a **Poisson distribution (λ)**  
- Represents the number of catastrophe events per year  

---

### 2. Event Severity
- Modeled using a **Lognormal distribution**  
- Captures the skewed nature of catastrophe losses  

---

### 3. Annual Loss Calculation

For each simulated year:

> Total Loss = Sum of (Event Loss × Portfolio Value)

This produces a **distribution of possible annual losses**.

---

### 4. Insurance Layer

Applies a simplified insurance structure:

- **Deductible:** Loss retained before coverage begins  
- **Limit:** Maximum payout by insurer  

---

### 5. Reinsurance Layer (Simplified)

- **Retention:** Threshold beyond which reinsurance applies  
- **Limit:** Maximum reinsurance coverage  

> Note: This is a simplified representation for demonstration purposes.

---

## Key Risk Metrics

- **Expected Annual Loss (EAL):** Average simulated loss  
- **PML 95%:** Loss exceeded in 5% of scenarios  
- **PML 99%:** Extreme tail-loss scenario  

These metrics help in understanding **risk exposure and variability**.

---

## Visualization

The dashboard compares:

- Gross Loss  
- Loss After Insurance  
- Loss After Reinsurance  

This illustrates how risk is reduced across layers.

---

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_LINK_HERE)

---

## What This Project Demonstrates

- Monte Carlo simulation for risk modeling  
- Frequency–severity modeling approach  
- Basic insurance and reinsurance mechanics  
- Tail-risk analysis using percentile metrics  
- Interactive data visualization  

---

## Project Structure

| File | Description |
|------|------------|
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Dependencies |
| `assets/` | Images / demo |
| `docs/` | Optional notes |

---

## Run Locally

```bash
git clone https://github.com/GauravSingh2410/cat-risk-simulator.git
cd cat-risk-simulator
pip install -r requirements.txt
streamlit run app.py
