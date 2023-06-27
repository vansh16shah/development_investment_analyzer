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


# Title and introduction
st.title("AI Project Evaluation Tool")
st.write("""
This tool helps you make the decision on whether your company should build new AI assets or wait until technology is more sophisticated before making a formal investment. It uses a number of various input factors to get the formula to equal G which is your net gain (positive or negative) from such an investment. 
""")

# Input sliders for each variable
E = st.sidebar.slider("Expected value (ROI) of the project (E) in $1000s", 0.0, 1000.0, 200.0)
W_E = st.sidebar.slider("Weight for E", 1.0, 5.0, 1.0)

F = st.sidebar.slider("Risk of failure (F) as a fraction", 0.0, 1.0, 0.1)
W_F = st.sidebar.slider("Weight for F", 1.0, 5.0, 1.0)

NP = st.sidebar.slider("Number of People (NP) on a scale of 1 to 10000", 1, 10000, 1)
W_NP = st.sidebar.slider("Weight for NP", 1.0, 5.0, 1.0)

AHW = st.sidebar.slider("Average Hourly Wage for Development Team (AHW) in $", 20.0, 200.0, 20.0)

Tb = st.sidebar.slider("Time to build the tool internally (Tb) in months", 1, 48, 12)

IC = st.sidebar.slider("Infrastructure Costs (IC) in $1000s", 0.0, 1000.0, 100.0)

SC = st.sidebar.slider("Support Cost (SC) in $1000", 0.0, 1000.0, 100.0)

MCost = st.sidebar.slider("Miscellaneous Cost (MCost) in $1000", 0.0, 1000.0, 200.0)

# Calculate the cost
C = AHW*NP*(Tb*4)+IC+SC+MCost

# Define the range for displaying C
min_C = 0.0
max_C = 1000000.0

# Display C within the defined range
st.sidebar.write("## Total Cost (C):", max(min(C, max_C), min_C))

R = st.sidebar.slider("Expected revenue from selling the tool (R) per year in $1000s", 0.0, 1000.0, 200.0)
W_R = st.sidebar.slider("Weight for R", 1.0, 5.0, 1.0)

SG = st.sidebar.slider("Alignment with strategic goals (SG) on a scale of 0 to 10", 0.0, 10.0, 0.0)
W_SG = st.sidebar.slider("Weight for SG", 1.0, 5.0, 1.0)

AR = st.sidebar.slider("Availability of resources (AR) on a scale of 0 to 10", 0.0, 10.0, 0.0)
W_AR = st.sidebar.slider("Weight for AR", 1.0, 5.0, 1.0)

MC = st.sidebar.slider("Market Competition (MC) on a scale of 0 to 10", 0.0, 10.0, 0.0)
W_MC = st.sidebar.slider("Weight for MC", 1.0, 5.0, 1.0)

TC = st.sidebar.slider("Technical Complexity (TC) on a scale of 0 to 10", 0.0, 10.0, 0.0) #Possibly Delete 
W_TC = st.sidebar.slider("Weight for TC", 1.0, 5.0, 1.0) 

RR = st.sidebar.slider("Regulatory Risks (RR) on a scale of 0 to 10", 0.0, 10.0, 0.0)
W_RR = st.sidebar.slider("Weight for RR", 1.0, 5.0, 1.0)

MRA = st.sidebar.slider("Market Readiness and Acceptance (MRA) on a scale of 0 to 10", 0.0, 10.0, 0.0)
W_MRA = st.sidebar.slider("Weight for MRA", 1.0, 5.0, 1.0)


# Calculate net gain and time-adjusted gain
G = (W_E*E*1000-C) - W_F*F + W_R*R + W_SG*SG + W_AR*AR - W_MC*MC - W_TC*TC - W_RR*RR + W_MRA*MRA
G_prime = G / Tb



# Display results
st.write(f"The net gain (G) from building the tool internally is: {G} units")
st.write(f"The time-adjusted gain (G') is: {G_prime} units per quarter")

# Define the threshold values for the scorecard tiers
threshold_good = 1500  # Adjust this threshold based on your specific requirements
threshold_moderate = 200  # Adjust this threshold based on your specific requirements
threshold_poor = 0.0  # Adjust this threshold based on your specific requirements

# Create the scorecard based on G
if G >= threshold_good:
    scorecard_G = "Good"
elif G >= threshold_moderate:
    scorecard_G = "Moderate"
else:
    scorecard_G = "Poor"

# Create the scorecard based on G_prime
if G_prime >= threshold_good/Tb:
    scorecard_G_prime = "Good"
elif G_prime >= threshold_moderate/Tb:
    scorecard_G_prime = "Moderate"
else:
    scorecard_G_prime = "Poor"

# Display the scorecard results
st.write(f"Scorecard for G: {scorecard_G}")
st.write(f"Scorecard for G_prime: {scorecard_G_prime}")


# Interpretation
if G_prime > 40:
    st.success("This project is a good investment.")
elif G_prime < 0:
    st.error("This project is a poor investment.")
else:
    st.warning("This project is a moderate investment, and the decision to build or hold would depend on other factors, such as the organization's strategic goals, the availability of resources, and the potential impact on customers and employees.")

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


# Save and Load Scenarios
scenario_data = {}

# Function to save a scenario
def save_scenario(name, data):
    scenario_data[name] = copy.deepcopy(data)
    with open("scenarios.json", "w") as file:
        json.dump(scenario_data, file)

# Function to load a scenario
def load_scenario(name):
    global scenario_data  # Add this line to access the global scenario_data dictionary
    with open("scenarios.json", "r") as file:
        scenario_data = json.load(file)
        if name in scenario_data:
            return scenario_data[name]
        else:
            st.error("Scenario not found!")


# Save scenario
save_button = st.button("Save Scenario")

if save_button:
    scenario_name = st.text_input("Enter a name for the scenario:")

    # Load existing data from the JSON file
    with open("scenarios.json", "r") as file:
        scenario_data = json.load(file)

    if scenario_name:
        scenario_data[scenario_name] = {
            "E": E,
            "F": F,
            "C": C,
            "R": R,
            "Tb": Tb,
            "SG": SG,
            "AR": AR,
            "NP": NP,
            "MC": MC,
            "TC": TC,
            "RR": RR,
            "MRA": MRA
        }

        with open("scenarios.json", "w") as file:
            json.dump(scenario_data, file, indent=4)

        st.success("Scenario saved successfully!")




# Load scenario dropdown
load_button = st.button("Load Scenario")

if load_button:
    with open("scenarios.json", "r") as file:
        scenario_data = json.load(file)
    
    # scenario_names = [name for name in scenario_data.keys() if not isinstance(scenario_data[name], dict)]
    scenario_names = []
    for name in list(scenario_data.keys()):
        scenario_names.append(name)

    scenario_name = st.selectbox("Select a scenario to load:", scenario_names)
    if scenario_name:
        loaded_data = scenario_data[scenario_name]
        print(loaded_data)
        E = loaded_data['E']
        F = loaded_data['F']
        C = loaded_data['C']
        R = loaded_data['R']
        Tb = loaded_data['Tb']
        SG = loaded_data['SG']
        AR = loaded_data['AR']
        NP = loaded_data['NP']
        MC = loaded_data['MC']
        TC = loaded_data['TC']
        RR = loaded_data['RR']
        MRA = loaded_data['MRA']

        st.empty()
        st.sidebar.slider("Expected value (ROI) of the project (E) in $1000s", 0.0, 1000.0, E)
