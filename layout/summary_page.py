import streamlit as st
from utils.dataframes import (
    build_constraints_df,
    build_efficiency_df,
    build_power_df,
    build_state_df,
)
from utils.plots import plot_ramp_profiles


def render_summary(defaults):

    st.info(
        "Use this page to check the caracteristics and constraints of the virtual power plant."
    )

    constraints_df = build_constraints_df(defaults)
    efficiency_df = build_efficiency_df(defaults)
    power_df = build_power_df(defaults)
    state_df = build_state_df(defaults)

    st.markdown(
        f"""
- **Minimum ON duration**: when the plant starts, it must stay on for a minimum of {st.session_state.get("min_hours_on", defaults["min_hours_on"])} hours  
- **Minimum OFF duration**: when the plant is shut down, it must stay off for a minimum of {st.session_state.get("min_hours_off", defaults['min_hours_off'])} hours  
- **Startup cost**: each startup costs {st.session_state.get("startup_cost", defaults['startup_cost']):,.0f} €
- **Variable cost**: each MWh produced costs {st.session_state.get("variable_cost", defaults['variable_cost'])} € / MWh  
- **Hourly fixed cost**: for each hour on we have a cost of {st.session_state.get("hourly_fixed_cost", defaults['hourly_fixed_cost']):,.0f} €  
- **Full load**: the power at full load is {st.session_state.get("power_full", defaults['power_full'])} MW at {st.session_state.get("efficiency_full", defaults['efficiency_full']):.2f} % efficiency  
- **Min load**: the power at partial load is  {st.session_state.get("power_partial", defaults['power_partial'])} MW at {st.session_state.get("efficiency_partial", defaults['efficiency_partial']):.2f} % efficiency  
- **Stop state**: the power during the stop ramp is {st.session_state.get("power_stop", defaults['power_stop'])} MW at {st.session_state.get("efficiency_stop", defaults['efficiency_stop']):.2f} % efficiency  
"""
    )

    st.pyplot(plot_ramp_profiles(power_df, efficiency_df))

    st.markdown("### Ramp State Logic Table")
    st.dataframe(state_df)

    st.markdown("### Constraints Table")
    st.dataframe(constraints_df)

    st.markdown("### Ramp Power Table")
    st.dataframe(power_df)

    st.markdown("### Ramp Efficiency Table")
    st.dataframe(efficiency_df)
