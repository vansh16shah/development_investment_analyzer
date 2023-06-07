import json
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and introduction
st.title("AI Project Evaluation Tool")
st.write("""
This tool helps you make the decision on whether your company should build new AI assets or wait until technology is more sophisticated before making a formal investment. It uses a number of various input factors to get the formula to equal G which is your net gain (positive or negative) from such an investment. 
""")

# Input sliders for each variable
E = st.sidebar.slider("Expected value (ROI) of the project (E) in $1000s", 0.0, 1000.0, 200.0)
F = st.sidebar.slider("Risk of failure (F) as a fraction", 0.0, 1.0, 0.1)
C = st.sidebar.slider("Cost of the project (C) per month in $1000s", 0.0, 100.0, 10.0)
R = st.sidebar.slider("Expected revenue from selling the tool (R) per year in $1000s", 0.0, 1000.0, 200.0)
Tb = st.sidebar.slider("Time to build the tool internally (Tb) in months", 1, 48, 12)
CS = st.sidebar.slider("Potential impact on customer satisfaction (CS) on a scale of 0 to 10", 0.0, 10.0, 0.0)
SG = st.sidebar.slider("Alignment with strategic goals (SG) on a scale of 0 to 10", 0.0, 10.0, 0.0)
AR = st.sidebar.slider("Availability of resources (AR) on a scale of 0 to 10", 0.0, 10.0, 0.0)
NP = st.sidebar.slider("Number of People (NP) on a scale of 1 to 100", 1, 10000, 1)
MC = st.sidebar.slider("Market Competition (MC) on a scale of 0 to 10", 0.0, 10.0, 0.0)
TC = st.sidebar.slider("Technical Complexity (TC) on a scale of 0 to 10", 0.0, 10.0, 0.0)
RR = st.sidebar.slider("Regulatory Risks (RR) on a scale of 0 to 10", 0.0, 10.0, 0.0)
SA = st.sidebar.slider("Skills Availability (SA) on a scale of 0 to 10", 0.0, 10.0, 0.0)
INP = st.sidebar.slider("Impact of Not Doing the Project (INP) on a scale of 0 to 10", 0.0, 10.0, 0.0)
MRA = st.sidebar.slider("Market Readiness and Acceptance (MRA) on a scale of 0 to 10", 0.0, 10.0, 0.0)


# Calculate net gain and time-adjusted gain
# G = E - F*C*Tb + R + CS + SG + AR
# G_prime = G / Tb
G = E - F*C*Tb + R + CS + SG + AR + NP + MC + TC + RR + SA + INP + MRA
G_prime = G / Tb


# Display results
st.write(f"The net gain (G) from building the tool internally is: {G} units")
st.write(f"The time-adjusted gain (G') is: {G_prime} units per quarter")

# Interpretation
if G_prime > 10:
    st.success("This project is a good investment.")
elif G_prime < 0:
    st.error("This project is a poor investment.")
else:
    st.warning("This project is a moderate investment, and the decision to build or hold would depend on other factors, such as the organization's strategic goals, the availability of resources, and the potential impact on customers and employees.")

# Sensitivity analysis
st.write("## Sensitivity Analysis")
variables = ["E", "F", "C", "R", "Tb", "CS", "SG", "AR", "NP", "MC", "TC", "RR", "SA", "INP", "MRA"]
values = [E, F, C, R, Tb, CS, SG, AR, NP, MC, TC, RR, SA, INP, MRA]
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
st.pyplot()


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
- **Interactive Visualization**: This allows you to explore the relationship between the variables and the results in a more interactive way. For example, you could use a scatter plot to visualize the relationship between E and G', or a bar chart to compare the sensitivity of different variables.
""")


# Interactive real-time impact visualization
st.write("## Real-time Impact Visualization")

# Create a figure
fig = go.Figure()

# Add traces for net gain and time-adjusted gain
fig.add_trace(go.Scatter(x=variables, y=[G]*len(variables), mode='lines', name='Net Gain'))
fig.add_trace(go.Scatter(x=variables, y=[G_prime]*len(variables), mode='lines', name='Time-adjusted Gain'))

# Update layout
fig.update_layout(title='Real-time Impact of Changes in Variables',
                   xaxis_title='Variables',
                   yaxis_title='Value',
                   autosize=False,
                   width=500,
                   height=500,
                   margin=dict(l=50, r=50, b=100, t=100, pad=4))

# Add sliders
sliders = [dict(active=0, pad={"t": 1}, steps=[])]
for i, var in enumerate(variables):
    step = dict(method="update", label = f"{var}", args=[{"x": [variables], "y": [[G]*len(variables), [G_prime]*len(variables)]}])
    sliders[0]["steps"].append(step)
fig.update_layout(sliders=sliders)

st.plotly_chart(fig)


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


# Correlation matrix
#st.write("## Correlation Matrix")
#variables = ["E", "F", "C", "R", "Tb", "CS", "SG", "AR"]
#values = [E, F, C, R, Tb, CS, SG, AR]
#df = pd.DataFrame(np.column_stack([values]), columns=variables)
#corrMatrix = df.corr()
#sns.heatmap(corrMatrix, annot=True)
#st.pyplot()

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

