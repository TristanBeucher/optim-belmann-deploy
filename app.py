import streamlit as st
from layout.optimal_dispatch_page import render_optimal_dispatch
from layout.plant_caracteristics_page import (
    render_costs,
    render_emission_factor,
    render_loads,
    render_min_off_on,
)
from layout.ramps_page import render_cold_ramp, render_hot_ramp, render_warm_ramp
from layout.readme_page import render_readme
from layout.summary_page import render_summary

# Default values
emission_factor_default = 0.18
power_full_default = 400.0
power_partial_default = 250.0
power_stop_default = 70.0
efficiency_full_default = 55.0
efficiency_partial_default = 45.0
efficiency_stop_default = 30.0

offline_limit_hours_hot_default = 10
ramp_hours_hot_default = 1

offline_limit_hours_warm_default = 40
ramp_hours_warm_default = 3

ramp_hours_cold_default = 4

min_hours_on_default = 4
min_hours_off_default = 4
startup_cost_default = 2500.0
variable_cost_default = 0.5
hourly_fixed_cost_default = 250.0

power_hour_1_hot_default = 170.0
power_hour_2_hot_default = power_full_default
power_hour_3_hot_default = power_full_default
efficiency_hour_1_hot_default = 35.0
efficiency_hour_2_hot_default = efficiency_full_default
efficiency_hour_3_hot_default = efficiency_full_default

power_hour_1_warm_default = 90.0
power_hour_2_warm_default = 215.0
power_hour_3_warm_default = 350.0
power_hour_4_warm_default = power_full_default
efficiency_hour_1_warm_default = 25.0
efficiency_hour_2_warm_default = 37.0
efficiency_hour_3_warm_default = 45.0
efficiency_hour_4_warm_default = efficiency_full_default

power_hour_1_cold_default = 85.0
power_hour_2_cold_default = 160.0
power_hour_3_cold_default = 275.0
power_hour_4_cold_default = 350.0
efficiency_hour_1_cold_default = 23.0
efficiency_hour_2_cold_default = 33.0
efficiency_hour_3_cold_default = 40.0
efficiency_hour_4_cold_default = 48.0

# Default dic
defaults = {
    "min_hours_on": min_hours_on_default,
    "min_hours_off": min_hours_off_default,
    "startup_cost": startup_cost_default,
    "variable_cost": variable_cost_default,
    "hourly_fixed_cost": hourly_fixed_cost_default,
    "emission_factor": emission_factor_default,
    "efficiency_full": efficiency_full_default,
    "efficiency_partial": efficiency_partial_default,
    "efficiency_stop": efficiency_stop_default,
    "power_full": power_full_default,
    "power_partial": power_partial_default,
    "power_stop": power_stop_default,
    "offline_limit_hours_hot": offline_limit_hours_hot_default,
    "offline_limit_hours_warm": offline_limit_hours_warm_default,
    "offline_limit_hours_cold": 9999,
    "ramp_hours_hot": ramp_hours_hot_default,
    "ramp_hours_warm": ramp_hours_warm_default,
    "ramp_hours_cold": ramp_hours_cold_default,
    "power_hour_1_hot": power_hour_1_hot_default,
    "power_hour_2_hot": power_hour_2_hot_default,
    "power_hour_3_hot": power_hour_3_hot_default,
    "efficiency_hour_1_hot": efficiency_hour_1_hot_default,
    "efficiency_hour_2_hot": efficiency_hour_2_hot_default,
    "efficiency_hour_3_hot": efficiency_hour_3_hot_default,
    "power_hour_1_warm": power_hour_1_warm_default,
    "power_hour_2_warm": power_hour_2_warm_default,
    "power_hour_3_warm": power_hour_3_warm_default,
    "power_hour_4_warm": power_hour_4_warm_default,
    "efficiency_hour_1_warm": efficiency_hour_1_warm_default,
    "efficiency_hour_2_warm": efficiency_hour_2_warm_default,
    "efficiency_hour_3_warm": efficiency_hour_3_warm_default,
    "efficiency_hour_4_warm": efficiency_hour_4_warm_default,
    "power_hour_1_cold": power_hour_1_cold_default,
    "power_hour_2_cold": power_hour_2_cold_default,
    "power_hour_3_cold": power_hour_3_cold_default,
    "power_hour_4_cold": power_hour_4_cold_default,
    "efficiency_hour_1_cold": efficiency_hour_1_cold_default,
    "efficiency_hour_2_cold": efficiency_hour_2_cold_default,
    "efficiency_hour_3_cold": efficiency_hour_3_cold_default,
    "efficiency_hour_4_cold": efficiency_hour_4_cold_default,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Sidebar for page selection
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Read me",
        "Plant's Caracteristics, Constraints and Costs",
        "Ramp Specifications",
        "Summary",
        "Optimal Dispatch",
    ],
)
if page == "Read me":

    render_readme()

# Page 1: Plant's specifications
if page == "Plant's Caracteristics, Constraints and Costs":

    st.title("Plant's Specifications")

    st.info("Use the sections below to configure parameters for the virtual plant.")

    with st.expander("Emission factor", expanded=False):
        render_emission_factor()

    with st.expander("FULL/PARTIAL Load and STOP", expanded=False):
        render_loads()

    with st.expander("Costs", expanded=False):
        render_costs()

    with st.expander("Other constraints", expanded=False):
        render_min_off_on()


elif page == "Ramp Specifications":

    st.title("Ramp Specifications")

    st.info(
        "Use the sections below to configure parameters for HOT, WARM, and COLD ramp scenarios."
    )

    with st.expander("HOT Ramp Configuration", expanded=False):
        render_hot_ramp()

    with st.expander("WARM Ramp Configuration", expanded=False):
        render_warm_ramp()

    with st.expander("COLD Ramp Configuration", expanded=False):
        render_cold_ramp()


elif page == "Summary":
    st.title("Summary")

    render_summary(defaults)

# Page 2: Placeholder for future pages
elif page == "Optimal Dispatch":

    render_optimal_dispatch(defaults, initial_state="OFF_20")
