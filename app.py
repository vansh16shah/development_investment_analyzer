import json
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import copy
import time


# Logo
st.image("creospan_logo_main.png", use_column_width=True)

def calculate_G(W_E, E, W_F, F, W_R, R, W_SG, SG, W_AR, AR, W_MC, MC, W_TC, TC, W_RR, RR, W_MRA, MRA, C):
    G = (W_E*E*1000-C) - W_F*F + W_R*R + W_SG*SG + W_AR*AR - W_MC*MC - W_TC*TC - W_RR*RR + W_MRA*MRA
    return G

def calculate_G_prime(G, Tb):
    G_prime = G / Tb
    return G_prime

# Title and introduction
st.title('Project Feasibility Analysis Tool')
st.write("""
This tool helps you make the decision on whether your company should build new AI assets or wait until technology is more sophisticated before making a formal investment. It uses a number of various input factors to get the formula to equal G which is your net gain (positive or negative) from such an investment. 
""")

num_projects = st.number_input('Enter number of projects', min_value=1, value=1, step=1)
project_data = []

for i in range(num_projects):
    st.subheader(f'Project {i+1}')
    
    # Input sliders for each variable
    E = st.sidebar.slider(f"Expected value (ROI) of the project (E) for Project {i+1} in $1000s", 0.0, 1000.0, 200.0)
    W_E = st.sidebar.slider(f"Weight for E for Project {i+1}", 1.0, 5.0, 1.0)

    F = st.sidebar.slider(f"Risk of failure (F) for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_F = st.sidebar.slider(f"Weight for F for Project {i+1}", 1.0, 5.0, 1.0)

    R = st.sidebar.slider(f"Risk of R for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_R = st.sidebar.slider(f"Weight for R for Project {i+1}", 1.0, 5.0, 1.0)

    SG = st.sidebar.slider(f"SG for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_SG = st.sidebar.slider(f"Weight for SG for Project {i+1}", 1.0, 5.0, 1.0)

    AR = st.sidebar.slider(f"AR for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_AR = st.sidebar.slider(f"Weight for AR for Project {i+1}", 1.0, 5.0, 1.0)

    MC = st.sidebar.slider(f"MC for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_MC = st.sidebar.slider(f"Weight for MC for Project {i+1}", 1.0, 5.0, 1.0)

    TC = st.sidebar.slider(f"TC for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_TC = st.sidebar.slider(f"Weight for TC for Project {i+1}", 1.0, 5.0, 1.0)

    RR = st.sidebar.slider(f"RR for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_RR = st.sidebar.slider(f"Weight for RR for Project {i+1}", 1.0, 5.0, 1.0)

    MRA = st.sidebar.slider(f"MRA for Project {i+1} as a fraction", 0.0, 1.0, 0.1)
    W_MRA = st.sidebar.slider(f"Weight for MRA for Project {i+1}", 1.0, 5.0, 1.0)

    Tb = st.sidebar.slider(f"Time to break even (Tb) for Project {i+1} in years", 0.0, 5.0, 1.0)

    AHW = st.sidebar.slider(f"Average hourly wage (AHW) for Project {i+1} in $", 0.0, 100.0, 20.0)
    NP = st.sidebar.slider(f"Number of personnel (NP) for Project {i+1}", 1, 100, 10)
    IC = st.sidebar.slider(f"Implementation costs (IC) for Project {i+1} in $1000s", 0.0, 1000.0, 100.0)
    SC = st.sidebar.slider(f"Support costs (SC) for Project {i+1} in $1000s", 0.0, 1000.0, 100.0)
    MCost = st.sidebar.slider(f"Maintenance costs (MCost) for Project {i+1} in $1000s", 0.0, 1000.0, 100.0)

    # Calculate the cost
    C = AHW*NP*(Tb*4)+IC+SC+MCost

    # Calculate net gain and time-adjusted gain
    G = calculate_G(W_E, E, W_F, F, W_R, R, W_SG, SG, W_AR, AR, W_MC, MC, W_TC, TC, W_RR, RR, W_MRA, MRA, C)
    G_prime = calculate_G_prime(G, Tb)

project_data.append([G, G_prime])

# Display individual project results
st.write(f"The net gain (G) for Project {i+1}: {G} units")
st.write(f"The time-adjusted gain (G') for Project {i+1}: {G_prime} units per quarter")

df = pd.DataFrame(project_data, columns=['G', 'G_prime'])
st.dataframe(df)

# Display results
st.write(f"The net gain (G) from building the tool internally is: {G} units")
st.write(f"The time-adjusted gain (G') is: {G_prime} units per quarter")

# Sensitivity analysis
st.write("## Sensitivity Analysis")
variables = ["E", "F", "C", "R", "Tb", "SG", "AR", "NP", "MC", "TC", "RR", "MRA"]
values = [E, F, C, R, Tb, SG, AR, NP, MC, TC, RR, MRA]
sensitivity = []
for i in range(len(variables)):
    new_values = values.copy()
    new_values[i] *= 1.1  # Increase the variable by 10%
    new_G = sum(new_values) / Tb
    sensitivity.append((new_G - G_prime) / G_prime)
st.bar_chart(pd.DataFrame(sensitivity, index=variables, columns=["Sensitivity"]))

# Monte Carlo simulation
st.write("## Monte Carlo Simulation")
N = st.slider("Number of simulations", 1000, 10000, 5000)
simulations = []
for _ in range(N):
    sim_values = np.random.normal(values, 0.1 * np.array(values))  # Assume 10% standard deviation
    sim_G = sum(sim_values) / Tb
    simulations.append(sim_G)
plt.hist(simulations, bins=50)
plt.xlabel('Time-adjusted Gain')
plt.ylabel('Frequency')
# st.pyplot()


# Explanation of formulas
st.write("## Explanation of Formulas")
st.write("""
- The net gain (G) from building the tool internally is calculated as the expected value of the project (E) minus the risk of failure (F) and the cost of the project (C), plus the expected revenue from selling the tool (R), the potential impact on customer satisfaction (CS), the alignment with strategic goals (SG), and the availability of resources (AR).
- The time-adjusted gain (G') is calculated as the net gain (G) divided by the time to build the tool internally (Tb).
- The sensitivity of each variable is calculated as the percentage change in G' when the variable is increased by 10%.
- The Monte Carlo simulation generates a distribution of G' by randomly varying each variable according to a normal distribution with a standard deviation of 10% of its value.
""")

# Additional features
st.write("## Additional Features")
st.write("""
- **Scenario Analysis**: This allows you to define different scenarios (e.g., best case, worst case, most likely case) and see how they affect the results. You can define a scenario by specifying values for each variable, and the app will calculate G and G' for that scenario.
- **Risk Analysis**: This allows you to define different levels of risk tolerance and see how they affect the decision to build or hold. For example, if you have a high risk tolerance, you might be willing to proceed with a project even if G' is negative.
""")

# Save and load scenarios
st.write("## Save and Load Scenarios")

# Input for scenario name
scenario_name = st.text_input("Scenario name")

# Button to save scenario
if st.button("Save scenario"):
    # Save values to a JSON file
    scenario = {var: val for var, val in zip(variables, values)}
    with open(f"{scenario_name}.json", "w") as f:
        json.dump(scenario, f)
    st.write(f"Scenario '{scenario_name}' saved.")

# Button to load scenario
if st.button("Load scenario"):
    # Load values from a JSON file
    try:
        with open(f"{scenario_name}.json", "r") as f:
            scenario = json.load(f)
        for var, val in scenario.items():
            st.write(f"{var}: {val}")
        st.write(f"Scenario '{scenario_name}' loaded.")
    except FileNotFoundError:
        st.write(f"Scenario '{scenario_name}' not found.")
