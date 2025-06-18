import streamlit as st


def render_emission_factor():

    st.info("Select the quantity of CO2 release when a MWh of gas is consumed")
    # Emission factor
    emission_factor = st.number_input(
        "Emission factor (t / MWh_gas)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state["emission_factor"],
        step=0.01,
    )
    st.session_state["emission_factor"] = emission_factor


def render_loads():

    st.info("Select the power and efficiency for full load, partial load and stop mode")

    st.subheader("Power by Load State (%)")

    power_full = st.number_input(
        "FULL LOAD Power (MW)",
        min_value=20.0,
        max_value=600.0,
        value=st.session_state["power_full"],
        step=1.0,
    )
    st.session_state["power_full"] = power_full

    power_partial = st.number_input(
        "PARTIAL LOAD Power (MW)",
        min_value=20.0,
        max_value=600.0,
        value=st.session_state["power_partial"],
        step=1.0,
    )
    st.session_state["power_partial"] = power_partial

    power_stop = st.number_input(
        "STOP Power (MW)",
        min_value=1.0,
        max_value=power_full,
        value=st.session_state["power_stop"],
        step=1.0,
    )
    st.session_state["power_stop"] = power_stop

    st.subheader("Efficiency by Load State (%)")

    efficiency_full = st.number_input(
        "FULL LOAD Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=st.session_state["efficiency_full"],
        step=0.1,
    )
    st.session_state["efficiency_full"] = efficiency_full

    efficiency_partial = st.number_input(
        "PARTIAL LOAD Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=st.session_state["efficiency_partial"],
        step=0.1,
    )
    st.session_state["efficiency_partial"] = efficiency_partial

    efficiency_stop = st.number_input(
        "STOP Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=st.session_state["efficiency_stop"],
        step=0.1,
    )
    st.session_state["efficiency_stop"] = efficiency_stop


def render_min_off_on():

    st.info(
        "In this section, you can change change additionnal constraints such as the minimum hours on (meaning that that if the "
        "plant starts, it has to stay on for at least XX hours), or the similar minimum hours off."
    )

    min_hours_on = st.number_input(
        "Minimum Hours ON",
        min_value=0,
        max_value=100,
        value=st.session_state["min_hours_on"],
        step=1,
    )
    st.session_state["min_hours_on"] = min_hours_on

    min_hours_off = st.number_input(
        "Minimum Hours OFF",
        min_value=0,
        max_value=100,
        value=st.session_state["min_hours_off"],
        step=1,
    )
    st.session_state["min_hours_off"] = min_hours_off


def render_costs():

    st.info(
        "In this section, you can modify the cost of a startup and the costs associated to an hour on and to a MWH produced"
    )
    startup_cost = st.number_input(
        "Startup Cost (€)",
        min_value=0.0,
        max_value=1e6,
        value=st.session_state["startup_cost"],
        step=100.0,
    )
    st.session_state["startup_cost"] = startup_cost

    variable_cost = st.number_input(
        "Variable Cost (€/MWh)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state["variable_cost"],
        step=0.1,
    )
    st.session_state["variable_cost"] = variable_cost

    hourly_fixed_cost = st.number_input(
        "Hourly Fixed Cost (€)",
        min_value=0.0,
        max_value=10000.0,
        value=st.session_state["hourly_fixed_cost"],
        step=10.0,
    )
    st.session_state["hourly_fixed_cost"] = hourly_fixed_cost
