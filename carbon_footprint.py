import streamlit as st
import pandas as pd
import altair as alt
import random

# Define emission factors (example values, replace with accurate data)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 0.6,  # kgCO2/meal
        "Waste": 0.9  # kgCO2/kg
    },
     "USA": {
        "Transportation": 0.22,
        "Electricity": 0.45,
        "Diet": 0.9,
        "Waste": 1.2
    },
    "China": {
        "Transportation": 0.17,
        "Electricity": 0.68,
        "Diet": 0.99,
        "Waste": 1.15
    },
    "Germany": {
        "Transportation": 0.18,
        "Electricity": 0.37,
        "Diet": 0.80,
        "Waste": 1.12 
    },
    "Brazil": {
        "Transportation": 0.12,
        "Electricity": 0.10,
        "Diet": 0.30,
        "Waste": 1.08
    },
    "Australia": {
        "Transportation": 0.21,
        "Electricity": 0.70,
        "Diet": 1.00,
        "Waste": 0.92
    },
    "UK": {
        "Transportation": 0.19,
        "Electricity": 0.23,
        "Diet": 0.75,
        "Waste": 0.84
    },
    "Japan": {
        "Transportation": 0.16,
        "Electricity": 0.50,
        "Diet": 0.60,
        "Waste": 0.73
    },
    "Canada": {
        "Transportation": 0.20,
        "Electricity": 0.15,
        "Diet": 0.98,
        "Waste": 1.18
    },
    "France": {
        "Transportation": 0.15,
        "Electricity": 0.05,
        "Diet": 0.70,
        "Waste": 1.10
    }
}

def calculate_sci(emissions, impact_factor, mitigation_actions, reduction_potential):
    """Calculate the Sustainability Consumption Index (SCI)."""
    sci = (emissions * impact_factor + mitigation_actions) / reduction_potential
    return round(sci, 2)

st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

st.title("Carbon Calculator")

# Initialize session state variables
if 'calculate_emissions' not in st.session_state:
    st.session_state.calculate_emissions = False

if 'calculate_sci' not in st.session_state:
    st.session_state.calculate_sci = False

# User inputs
st.subheader("Your Country")
country = st.selectbox("Select", list(EMISSION_FACTORS.keys()))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, 10.0, key="distance_input")

    st.subheader("Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, 100.0, key="electricity_input")

with col2:
    st.subheader("Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, 10.0, key="waste_input")

    st.subheader("Number of meals per day")
    meals = st.number_input("Meals", 0, 10, 3, key="meals_input")

# Normalize inputs
distance_yearly = distance * 365
electricity_yearly = electricity * 12
meals_yearly = meals * 365
waste_yearly = waste * 52

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance_yearly
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity_yearly
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals_yearly
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste_yearly

# Convert emissions to tonnes and round off to 2 decimal points
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Calculate total emissions
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

if st.button("Calculate CO2 Emissions"):
    st.session_state.calculate_emissions = True

if st.session_state.calculate_emissions:
    # Display results
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Category")
        st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    with col4:
        st.subheader("Total Carbon Footprint")
        st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
        st.warning("In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita. Between 1972 and 2021, CO2 emissions per capita of India grew substantially from 0.39 to 1.9 tons of CO2 per capita rising at an increasing annual rate that reached a maximum of 9.41% in 2021")

        # Get the category with the highest emissions
        category_emissions = {
            "Transportation": transportation_emissions,
            "Electricity": electricity_emissions,
            "Diet": diet_emissions,
            "Waste": waste_emissions
        }
        highest_category = max(category_emissions, key=category_emissions.get)

        # Suggest ways to reduce emissions
        advice = {
            "Transportation": [
                "Use public transport or switch to electric vehicles.",
                "Carpool with friends or colleagues to save fuel and lower emissions.",
                "Consider biking or walking for short distances."
            ],
            "Electricity": [
                "Opt for energy-efficient appliances.",
                "Use renewable energy sources like solar or wind.",
                "Turn off lights and appliances when not in use."
            ],
            "Diet": [
                "Reduce meat consumption, opt for plant-based meals.",
                "Buy organic foods that are grown without synthetic pesticides.",
                "Minimize food waste by planning meals ahead."
            ],
            "Waste": [
                "Recycle and compost organic waste.",
                "Reduce single-use plastics and opt for reusable items.",
                "Properly dispose of hazardous materials to avoid pollution."
            ]
        }

        random_advice = random.choice(advice[highest_category])

        st.subheader(f"Tips to Reduce Your Carbon Footprint in {highest_category}")
        st.markdown(f"- **{highest_category}**: {random_advice}")

        # Additional inputs for SCI calculation
        st.subheader("Sustainability Consumption Index (SCI) Calculation")

        col5, col6 = st.columns([1, 1])  # Adjust column width to make the table bigger

        with col5:
            impact_factor = st.number_input("Impact Factor (I)", 0.0, 10.0, 1.0, key="impact_factor_input")
            mitigation_actions = st.number_input("Mitigation Actions (M)", 0.0, 100.0, 10.0, key="mitigation_actions_input")
            reduction_potential = st.number_input("Reduction Potential (R)", 0.1, 100.0, 10.0, key="reduction_potential_input")

            if st.button("Calculate SCI"):
                st.session_state.calculate_sci = True

        with col3:
            # Display SCI Score Table
            st.subheader("SCI Score Table")
            sci_table = pd.DataFrame({
                "SCI Score": ["Good", "Average", "Bad"],
                "SCI Score Range": ["0.0 - 1.0", "1.1 - 3.0", "3.1 and above"]
            })

            # Make the table more visible
            st.dataframe(sci_table.style.set_properties(**{
                'background-color': 'white',
                'color': 'black',
                'border': '1px solid black'
            }), width=400)

    if st.session_state.calculate_sci:
        sci = calculate_sci(total_emissions, impact_factor, mitigation_actions, reduction_potential)
        st.success(f"Your Sustainability Consumption Index (SCI) is: {sci}")

        # Visualization
        df = pd.DataFrame({
            'Category': ['Transportation', 'Electricity', 'Diet', 'Waste'],
            'Emissions (tonnes CO2/year)': [transportation_emissions, electricity_emissions, diet_emissions, waste_emissions]
        })

        chart = alt.Chart(df).mark_bar().encode(
            x='Category',
            y='Emissions (tonnes CO2/year)',
            color='Category'
        ).properties(
            title='Carbon Emissions by Category'
        )

        st.altair_chart(chart, use_container_width=True)
