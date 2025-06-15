import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

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


# Sidebar for page selection
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Read me",
        "Full/Partial Load Specifications",
        "Ramp HOT Specifications",
        "Ramp WARM Specifications",
        "Ramp COLD Specifications",
        "Constraints and Costs",
        "Summary",
        "Optimal Dispatch",
        "Other page (placeholder)",
    ],
)

# Page 1: Plant's specifications
if page == "Full/Partial Load Specifications":

    st.title("Plant's Specifications")

    st.info(
        "On this page you can change the plant's emission factor (in t/MWh_gas), as well as power "
        "and efficiency for full load, partial load and stop ramp."
    )

    # Emission factor
    emission_factor = st.number_input(
        "Emission factor (t / MWh_gas)",
        min_value=0.0,
        max_value=10.0,
        value=emission_factor_default,
        step=0.01,
    )
    st.session_state["emission_factor"] = emission_factor

    st.subheader("Power by Load State (MW)")
    power_full = st.number_input(
        "FULL LOAD Power (MW)",
        min_value=20.0,
        max_value=600.0,
        value=power_full_default,
        step=1.0,
    )
    st.session_state["power_full"] = power_full

    power_partial = st.number_input(
        "PARTIAL LOAD Power (MW)",
        min_value=20.0,
        max_value=600.0,
        value=power_partial_default,
        step=1.0,
    )
    st.session_state["power_partial"] = power_partial

    power_stop = st.number_input(
        "STOP Power (MW)",
        min_value=1.0,
        max_value=power_full,
        value=power_stop_default,
        step=1.0,
    )
    st.session_state["power_stop"] = power_stop

    st.subheader("Efficiency by Load State (%)")
    efficiency_full = st.number_input(
        "FULL LOAD Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=efficiency_full_default,
        step=0.1,
    )
    st.session_state["efficiency_full"] = efficiency_full

    efficiency_partial = st.number_input(
        "PARTIAL LOAD Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=efficiency_partial_default,
        step=0.1,
    )
    st.session_state["efficiency_partial"] = efficiency_partial

    efficiency_stop = st.number_input(
        "STOP Efficiency (%)",
        min_value=1.0,
        max_value=100.0,
        value=efficiency_stop_default,
        step=0.1,
    )
    st.session_state["efficiency_stop"] = efficiency_stop


elif page == "Ramp HOT Specifications":

    st.title("Ramp HOT Specifications")

    st.info(
        "On this page you can change parameters related to the hot ramp, which is generally the fastest ramp mode. "
        "You can select the limit of off hours to use this ramp, the required time to reach full load, and the power "
        "and efficiency at each step of the ramp"
    )

    power_full = st.session_state.get("power_full", power_full_default)
    efficiency_full = st.session_state.get("efficiency_full", efficiency_full_default)

    # Offline time limit (XX hours)
    offline_limit_hours_hot = st.number_input(
        "Apply when offline for less than (hours)",
        min_value=1,
        max_value=100,
        value=offline_limit_hours_hot_default,
        step=1,
    )
    st.session_state["offline_limit_hours_hot"] = offline_limit_hours_hot

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_hot = st.number_input(
        "Hours to reach full load",
        min_value=1,
        max_value=3,
        value=ramp_hours_hot_default,
        step=1,
    )
    st.session_state["ramp_hours_hot"] = ramp_hours_hot

    # Power and efficiency inputs
    st.markdown("### Ramp Profile per Hour")

    # Hour 1 (always enabled)
    st.markdown("**Hour 1**")
    power_hour_1_hot = st.number_input(
        "Power Hour 1 (MW)",
        min_value=0.0,
        max_value=power_full,
        value=power_full / 2.0,
        step=1.0,
    )
    st.session_state["power_hour_1_hot"] = power_hour_1_hot

    efficiency_hour_1_hot = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=efficiency_full / 2.2,
        step=0.1,
    )
    st.session_state["efficiency_hour_1_hot"] = efficiency_hour_1_hot

    # Hour 2
    if ramp_hours_hot >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_hot = st.number_input(
            "Power Hour 2 (MW)",
            min_value=power_hour_1_hot,
            max_value=power_full,
            value=power_full / 1.5,
            step=1.0,
        )

        efficiency_hour_2_hot = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=efficiency_hour_1_hot,
            max_value=efficiency_full,
            value=efficiency_full / 2.0,
            step=0.1,
        )

    else:
        power_hour_2_hot = power_full
        efficiency_hour_2_hot = efficiency_full
        st.info("Hour 2 → Full Load parameters applied automatically.")

    st.session_state["power_hour_2_hot"] = power_hour_2_hot
    st.session_state["efficiency_hour_2_hot"] = efficiency_hour_2_hot

    # Hour 3
    if ramp_hours_hot == 3:

        st.markdown("**Hour 3**")
        power_hour_3_hot = st.number_input(
            "Power Hour 3 (MW)",
            min_value=power_hour_2_hot,
            max_value=power_full,
            value=power_full / 1.2,
            step=1.0,
        )
        efficiency_hour_3_hot = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=efficiency_hour_2_hot,
            max_value=efficiency_full,
            value=efficiency_full / 1.5,
            step=0.1,
        )
    else:
        power_hour_3_hot = power_full
        efficiency_hour_3_hot = efficiency_full
        st.info("Hour 3 → Full Load parameters applied automatically.")

    st.session_state["power_hour_3_hot"] = power_hour_3_hot
    st.session_state["efficiency_hour_3_hot"] = efficiency_hour_3_hot


elif page == "Ramp WARM Specifications":

    st.title("Ramp WARM Specifications")

    st.info(
        "On this page you can change parameters related to warm hot ramp, which is applied when the offline limit for using "
        "hot ramp has been exceeded. "
        "You can select the limit of off hours to use this ramp, the required time to reach full load, and the power "
        "and efficiency at each step of the ramp."
    )

    power_full = st.session_state.get("power_full", power_full_default)
    efficiency_full = st.session_state.get("efficiency_full", efficiency_full_default)
    offline_limit_hours_hot = st.session_state.get(
        "offline_limit_hours_hot", offline_limit_hours_hot_default
    )
    ramp_hours_hot = st.session_state.get("ramp_hours_hot", ramp_hours_hot_default)

    # Offline time limit (XX hours)
    offline_limit_hours_warm = st.number_input(
        "Apply when offline for less than (hours)",
        min_value=offline_limit_hours_hot + 1,
        max_value=200,
        value=offline_limit_hours_warm_default,
        step=1,
    )
    st.session_state["offline_limit_hours_warm"] = offline_limit_hours_warm

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_warm = st.number_input(
        "Hours to reach full load",
        min_value=1,
        max_value=4,
        value=ramp_hours_warm_default,
        step=1,
    )
    st.session_state["ramp_hours_warm"] = ramp_hours_warm

    # Power and efficiency inputs
    st.markdown("### Ramp Profile per Hour")

    # Hour 1 (always enabled)
    st.markdown("**Hour 1**")
    power_hour_1_warm = st.number_input(
        "Power Hour 1 (MW)",
        min_value=0.0,
        max_value=power_full,
        value=power_full / 3.0,
        step=1.0,
    )
    st.session_state["power_hour_1_warm"] = power_hour_1_warm

    efficiency_hour_1_warm = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=efficiency_full / 3.5,
        step=0.1,
    )
    st.session_state["efficiency_hour_1_warm"] = efficiency_hour_1_warm

    # Hour 2
    if ramp_hours_warm >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_warm = st.number_input(
            "Power Hour 2 (MW)",
            min_value=power_hour_1_warm,
            max_value=power_full,
            value=power_full / 2.0,
            step=1.0,
        )

        efficiency_hour_2_warm = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=efficiency_hour_1_warm,
            max_value=efficiency_full,
            value=efficiency_full / 2.5,
            step=0.1,
        )

    else:
        power_hour_2_warm = power_full
        efficiency_hour_2_warm = efficiency_full
        st.info("Hour 2 → Full Load parameters applied automatically.")

    st.session_state["power_hour_2_warm"] = power_hour_2_warm
    st.session_state["efficiency_hour_2_warm"] = efficiency_hour_2_warm

    # Hour 3
    if ramp_hours_warm >= 3:

        st.markdown("**Hour 3**")
        power_hour_3_warm = st.number_input(
            "Power Hour 3 (MW)",
            min_value=power_hour_2_warm,
            max_value=power_full,
            value=power_full / 1.5,
            step=1.0,
        )
        efficiency_hour_3_warm = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=efficiency_hour_2_warm,
            max_value=efficiency_full,
            value=efficiency_full / 1.8,
            step=0.1,
        )
    else:
        power_hour_3_warm = power_full
        efficiency_hour_3_warm = efficiency_full
        st.info("Hour 3 → Full Load parameters applied automatically.")

    st.session_state["power_hour_3_warm"] = power_hour_3_warm
    st.session_state["efficiency_hour_3_warm"] = efficiency_hour_3_warm

    # Hour 4
    if ramp_hours_warm == 4:

        st.markdown("**Hour 4**")
        power_hour_4_warm = st.number_input(
            "Power Hour 4 (MW)",
            min_value=power_hour_3_warm,
            max_value=power_full,
            value=power_full / 1.2,
            step=1.0,
        )
        efficiency_hour_4_warm = st.number_input(
            "Efficiency Hour 4 (%)",
            min_value=efficiency_hour_3_warm,
            max_value=efficiency_full,
            value=efficiency_full / 1.3,
            step=0.1,
        )
    else:
        power_hour_4_warm = power_full
        efficiency_hour_4_warm = efficiency_full
        st.info("Hour 4 → Full Load parameters applied automatically.")

    st.session_state["power_hour_4_warm"] = power_hour_4_warm
    st.session_state["efficiency_hour_4_warm"] = efficiency_hour_4_warm


elif page == "Ramp COLD Specifications":

    st.title("Ramp COLD Specifications")

    st.info(
        "On this page, you can change parameters related to cold ramp, which is applied when the offline limit for using "
        "warm ramp has been exceeded. As this is the last ramp then there is not need to define a limit for using it. "
        "You can modify the required time to reach full load, and the power "
        "and efficiency at each step of the ramp"
    )

    power_full = st.session_state.get("power_full", power_full_default)
    efficiency_full = st.session_state.get("efficiency_full", efficiency_full_default)
    ramp_hours_warm = st.session_state.get("ramp_hours_warm", ramp_hours_warm_default)

    # Offline time limit (XX hours)
    offline_limit_hours_cold = 9999
    st.session_state["offline_limit_hours_cold"] = offline_limit_hours_cold

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_cold = st.number_input(
        "Hours to reach full load",
        min_value=1,
        max_value=4,
        value=ramp_hours_cold_default,
        step=1,
    )
    st.session_state["ramp_hours_cold"] = ramp_hours_cold

    # Power and efficiency inputs
    st.markdown("### Ramp Profile per Hour")

    # Hour 1 (always enabled)
    st.markdown("**Hour 1**")
    power_hour_1_cold = st.number_input(
        "Power Hour 1 (MW)",
        min_value=0.0,
        max_value=power_full,
        value=power_full / 3.5,
        step=1.0,
    )
    st.session_state["power_hour_1_cold"] = power_hour_1_cold

    efficiency_hour_1_cold = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=efficiency_full / 4.0,
        step=0.1,
    )
    st.session_state["efficiency_hour_1_cold"] = efficiency_hour_1_cold

    # Hour 2
    if ramp_hours_cold >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_cold = st.number_input(
            "Power Hour 2 (MW)",
            min_value=power_hour_1_cold,
            max_value=power_full,
            value=power_full / 2.5,
            step=1.0,
        )

        efficiency_hour_2_cold = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=efficiency_hour_1_cold,
            max_value=efficiency_full,
            value=efficiency_full / 3.0,
            step=0.1,
        )

    else:
        power_hour_2_cold = power_full
        efficiency_hour_2_cold = efficiency_full
        st.info("Hour 2 → Full Load parameters applied automatically.")

    st.session_state["power_hour_2_cold"] = power_hour_2_cold
    st.session_state["efficiency_hour_2_cold"] = efficiency_hour_2_cold

    # Hour 3
    if ramp_hours_cold >= 3:

        st.markdown("**Hour 3**")
        power_hour_3_cold = st.number_input(
            "Power Hour 3 (MW)",
            min_value=power_hour_2_cold,
            max_value=power_full,
            value=power_full / 2.0,
            step=1.0,
        )
        efficiency_hour_3_cold = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=efficiency_hour_2_cold,
            max_value=efficiency_full,
            value=efficiency_full / 2.2,
            step=0.1,
        )
    else:
        power_hour_3_cold = power_full
        efficiency_hour_3_cold = efficiency_full
        st.info("Hour 3 → Full Load parameters applied automatically.")

    st.session_state["power_hour_3_cold"] = power_hour_3_cold
    st.session_state["efficiency_hour_3_cold"] = efficiency_hour_3_cold

    # Hour 4
    if ramp_hours_cold == 4:

        st.markdown("**Hour 4**")
        power_hour_4_cold = st.number_input(
            "Power Hour 4 (MW)",
            min_value=power_hour_3_cold,
            max_value=power_full,
            value=power_full / 1.5,
            step=1.0,
        )
        efficiency_hour_4_cold = st.number_input(
            "Efficiency Hour 4 (%)",
            min_value=efficiency_hour_3_cold,
            max_value=efficiency_full,
            value=efficiency_full / 1.7,
            step=0.1,
        )
    else:
        power_hour_4_cold = power_full
        efficiency_hour_4_cold = efficiency_full
        st.info("Hour 4 → Full Load parameters applied automatically.")

    st.session_state["power_hour_4_cold"] = power_hour_4_cold
    st.session_state["efficiency_hour_4_cold"] = efficiency_hour_4_cold

elif page == "Constraints and Costs":
    st.title("Constraints and Costs")

    st.info(
        "On this page, you can change change additionnal constraints such as the minimum hours on (meaning that that if the "
        "plant starts, it has to stay on for at least XX hours), the minimum hours off. "
        "You can also change costs linked to startup and production (hourly fixed cost and variable cost per MWH)."
    )

    min_hours_on = st.number_input(
        "Minimum Hours ON",
        min_value=0,
        max_value=100,
        value=min_hours_on_default,
        step=1,
    )
    st.session_state["min_hours_on"] = min_hours_on

    min_hours_off = st.number_input(
        "Minimum Hours OFF",
        min_value=0,
        max_value=100,
        value=min_hours_off_default,
        step=1,
    )
    st.session_state["min_hours_off"] = min_hours_off

    startup_cost = st.number_input(
        "Startup Cost (€)",
        min_value=0.0,
        max_value=1e6,
        value=startup_cost_default,
        step=100.0,
    )
    st.session_state["startup_cost"] = startup_cost

    variable_cost = st.number_input(
        "Variable Cost (€/MWh)",
        min_value=0.0,
        max_value=100.0,
        value=variable_cost_default,
        step=0.1,
    )
    st.session_state["variable_cost"] = variable_cost

    hourly_fixed_cost = st.number_input(
        "Hourly Fixed Cost (€)",
        min_value=0.0,
        max_value=10000.0,
        value=hourly_fixed_cost_default,
        step=10.0,
    )
    st.session_state["hourly_fixed_cost"] = hourly_fixed_cost

elif page == "Summary":
    st.title("Summary")

    state_df = pd.DataFrame(
        {
            "Use < XX off hours": {
                "RAMP_H": st.session_state.get(
                    "offline_limit_hours_hot", offline_limit_hours_hot_default
                ),
                "RAMP_W": st.session_state.get(
                    "offline_limit_hours_warm", offline_limit_hours_warm_default
                ),
                "RAMP_C": st.session_state.get("offline_limit_hours_cold", 9999),
                "FULL_LOAD": 0,
                "MIN_LOAD": 0,
                "STOP": 0,
            },
            "Hours to Reach Full Load": {
                "RAMP_H": st.session_state.get(
                    "ramp_hours_hot", ramp_hours_hot_default
                ),
                "RAMP_W": st.session_state.get(
                    "ramp_hours_warm", ramp_hours_warm_default
                ),
                "RAMP_C": st.session_state.get(
                    "ramp_hours_cold", ramp_hours_cold_default
                ),
                "FULL_LOAD": 0,
                "MIN_LOAD": 0,
                "STOP": 0,
            },
        }
    )

    power_df = pd.DataFrame(
        {
            "Hour 1": {
                "RAMP_H": st.session_state.get(
                    "power_hour_1_hot", power_full_default / 2.0
                ),
                "RAMP_W": st.session_state.get(
                    "power_hour_1_warm", power_full_default / 3.0
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_1_cold", power_full_default / 4.0
                ),
                "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", power_partial_default
                ),
                "STOP": st.session_state.get("power_stop", power_stop_default),
            },
            "Hour 2": {
                "RAMP_H": st.session_state.get("power_hour_2_hot", power_full_default),
                "RAMP_W": st.session_state.get(
                    "power_hour_2_warm", power_full_default / 2.0
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_2_cold", power_full_default / 2.5
                ),
                "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", power_partial_default
                ),
                "STOP": power_stop_default,
            },
            "Hour 3": {
                "RAMP_H": st.session_state.get("power_hour_3_hot", power_full_default),
                "RAMP_W": st.session_state.get(
                    "power_hour_3_warm", power_full_default / 1.5
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_3_cold", power_full_default / 2.0
                ),
                "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", power_partial_default
                ),
                "STOP": power_stop_default,
            },
            "Hour 4": {
                "RAMP_H": st.session_state.get("power_full", power_full_default),
                "RAMP_W": st.session_state.get(
                    "power_hour_4_warm",
                    st.session_state.get("power_full", power_full_default),
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_4_cold",
                    st.session_state.get("power_full", power_full_default),
                ),
                "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", power_partial_default
                ),
                "STOP": power_stop_default,
            },
        }
    )

    efficiency_df = pd.DataFrame(
        {
            "Hour 1": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_1_hot", efficiency_full_default / 2.2
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_1_warm", efficiency_full_default / 3.5
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_1_cold", efficiency_full_default / 4.0
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", efficiency_full_default
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", efficiency_partial_default
                ),
                "STOP": st.session_state.get(
                    "efficiency_stop", efficiency_stop_default
                ),
            },
            "Hour 2": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_2_hot", efficiency_full_default
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_2_warm", efficiency_full_default / 2.5
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_2_cold", efficiency_full_default / 3.0
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", efficiency_full_default
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", efficiency_partial_default
                ),
                "STOP": efficiency_stop_default,
            },
            "Hour 3": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_3_hot", efficiency_full_default
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_3_warm", efficiency_full_default / 1.8
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_3_cold", efficiency_full_default / 2.2
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", efficiency_full_default
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", efficiency_partial_default
                ),
                "STOP": efficiency_stop_default,
            },
            "Hour 4": {
                "RAMP_H": st.session_state.get(
                    "efficiency_full", efficiency_full_default
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_4_warm",
                    st.session_state.get("efficiency_full", efficiency_full_default),
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_4_cold",
                    st.session_state.get("efficiency_full", efficiency_full_default),
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", efficiency_full_default
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", efficiency_partial_default
                ),
                "STOP": efficiency_stop_default,
            },
        }
    )

    constraints_df = pd.DataFrame(
        {
            "Use": {
                "Min hours on": st.session_state.get(
                    "min_hours_on", min_hours_on_default
                ),
                "Min hours off": st.session_state.get(
                    "min_hours_off", min_hours_off_default
                ),
                "Max Nb Starts A day": 100,
                "Startup Cost": st.session_state.get(
                    "startup_cost", startup_cost_default
                ),
                "Variable Cost": st.session_state.get(
                    "variable_cost", variable_cost_default
                ),
                "Hourly fixed cost": st.session_state.get(
                    "hourly_fixed_cost", hourly_fixed_cost_default
                ),
                "Emission Factor": st.session_state.get(
                    "emission_factor", emission_factor_default
                ),
            }
        }
    )

    st.markdown(
        f"""
- 🕒 **Minimum ON duration**: {st.session_state.get("min_hours_on", min_hours_on_default)} hours  
- 💤 **Minimum OFF duration**: {st.session_state.get("min_hours_off", min_hours_off_default)} hours  
- ⚡ **Startup cost**: {st.session_state.get("startup_cost", startup_cost_default):,.0f} €
- 🔧 **Variable cost**: {st.session_state.get("variable_cost", variable_cost_default)} € / MWh  
- 🏭 **Hourly fixed cost**: €{st.session_state.get("hourly_fixed_cost", hourly_fixed_cost_default):,.0f}  
- 🔋 **Full load**: {st.session_state.get("power_full", power_full_default)} MW at {st.session_state.get("efficiency_full", efficiency_full_default):.2f} % efficiency  
- 🌀 **Min load**: {st.session_state.get("power_partial", power_partial_default)} MW at {st.session_state.get("efficiency_partial", efficiency_partial_default):.2f} % efficiency  
- 🛑 **Stop state**: {st.session_state.get("power_stop", power_stop_default)} MW at {st.session_state.get("efficiency_stop", efficiency_stop_default):.2f} % efficiency  
"""
    )

    def plot_ramp_profiles(power_df, efficiency_df):
        fig, ax1 = plt.subplots()

        colors = {"RAMP_H": "tab:blue", "RAMP_W": "tab:green", "RAMP_C": "tab:purple"}

        hours = [1, 2, 3, 4]
        ax2 = ax1.twinx()

        for state in ["RAMP_H", "RAMP_W", "RAMP_C"]:
            power = power_df.loc[state, [f"Hour {h}" for h in hours]]
            eff = efficiency_df.loc[state, [f"Hour {h}" for h in hours]]

            ax1.plot(hours, power, label=f"Output {state}", color=colors[state])
            ax2.plot(hours, eff, "--", label=f"Eff. {state}", color=colors[state])

        ax1.set_xlabel("Hour since startup")
        ax1.set_ylabel("Power Output (MW)")
        ax2.set_ylabel("Efficiency")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower right")

        ax1.set_title("Ramp-Up Profiles: Output and Efficiency")
        ax1.grid(True)
        st.pyplot(fig)

    plot_ramp_profiles(power_df, efficiency_df)

    st.markdown("### Ramp State Logic Table")
    st.dataframe(state_df)

    st.markdown("### Constraints Table")
    st.dataframe(constraints_df)

    st.markdown("### Ramp Power Table")
    st.dataframe(power_df)

    st.markdown("### Ramp Efficiency Table")
    st.dataframe(efficiency_df)

# Page 2: Placeholder for future pages
elif page == "Optimal Dispatch":

    st.title("Optimization Results")

    if st.button("Run Optimization"):

        state_df = pd.DataFrame(
            {
                "Use < XX off hours": {
                    "RAMP_H": st.session_state.get(
                        "offline_limit_hours_hot", offline_limit_hours_hot_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "offline_limit_hours_warm", offline_limit_hours_warm_default
                    ),
                    "RAMP_C": st.session_state.get("offline_limit_hours_cold", 9999),
                    "FULL_LOAD": 0,
                    "MIN_LOAD": 0,
                    "STOP": 0,
                },
                "Hours to Reach Full Load": {
                    "RAMP_H": st.session_state.get(
                        "ramp_hours_hot", ramp_hours_hot_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "ramp_hours_warm", ramp_hours_warm_default
                    ),
                    "RAMP_C": st.session_state.get(
                        "ramp_hours_cold", ramp_hours_cold_default
                    ),
                    "FULL_LOAD": 0,
                    "MIN_LOAD": 0,
                    "STOP": 0,
                },
            }
        )

        power_df = pd.DataFrame(
            {
                "Hour 1": {
                    "RAMP_H": st.session_state.get(
                        "power_hour_1_hot", power_full_default / 2.0
                    ),
                    "RAMP_W": st.session_state.get(
                        "power_hour_1_warm", power_full_default / 3.0
                    ),
                    "RAMP_C": st.session_state.get(
                        "power_hour_1_cold", power_full_default / 4.0
                    ),
                    "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                    "MIN_LOAD": st.session_state.get(
                        "power_partial", power_partial_default
                    ),
                    "STOP": st.session_state.get("power_stop", power_stop_default),
                },
                "Hour 2": {
                    "RAMP_H": st.session_state.get(
                        "power_hour_2_hot", power_full_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "power_hour_2_warm", power_full_default / 2.0
                    ),
                    "RAMP_C": st.session_state.get(
                        "power_hour_2_cold", power_full_default / 2.5
                    ),
                    "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                    "MIN_LOAD": st.session_state.get(
                        "power_partial", power_partial_default
                    ),
                    "STOP": power_stop_default,
                },
                "Hour 3": {
                    "RAMP_H": st.session_state.get(
                        "power_hour_3_hot", power_full_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "power_hour_3_warm", power_full_default / 1.5
                    ),
                    "RAMP_C": st.session_state.get(
                        "power_hour_3_cold", power_full_default / 2.0
                    ),
                    "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                    "MIN_LOAD": st.session_state.get(
                        "power_partial", power_partial_default
                    ),
                    "STOP": power_stop_default,
                },
                "Hour 4": {
                    "RAMP_H": st.session_state.get("power_full", power_full_default),
                    "RAMP_W": st.session_state.get(
                        "power_hour_4_warm",
                        st.session_state.get("power_full", power_full_default),
                    ),
                    "RAMP_C": st.session_state.get(
                        "power_hour_4_cold",
                        st.session_state.get("power_full", power_full_default),
                    ),
                    "FULL_LOAD": st.session_state.get("power_full", power_full_default),
                    "MIN_LOAD": st.session_state.get(
                        "power_partial", power_partial_default
                    ),
                    "STOP": power_stop_default,
                },
            }
        )

        efficiency_df = pd.DataFrame(
            {
                "Hour 1": {
                    "RAMP_H": st.session_state.get(
                        "efficiency_hour_1_hot", efficiency_full_default / 2.2
                    ),
                    "RAMP_W": st.session_state.get(
                        "efficiency_hour_1_warm", efficiency_full_default / 3.5
                    ),
                    "RAMP_C": st.session_state.get(
                        "efficiency_hour_1_cold", efficiency_full_default / 4.0
                    ),
                    "FULL_LOAD": st.session_state.get(
                        "efficiency_full", efficiency_full_default
                    ),
                    "MIN_LOAD": st.session_state.get(
                        "efficiency_partial", efficiency_partial_default
                    ),
                    "STOP": st.session_state.get(
                        "efficiency_stop", efficiency_stop_default
                    ),
                },
                "Hour 2": {
                    "RAMP_H": st.session_state.get(
                        "efficiency_hour_2_hot", efficiency_full_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "efficiency_hour_2_warm", efficiency_full_default / 2.5
                    ),
                    "RAMP_C": st.session_state.get(
                        "efficiency_hour_2_cold", efficiency_full_default / 3.0
                    ),
                    "FULL_LOAD": st.session_state.get(
                        "efficiency_full", efficiency_full_default
                    ),
                    "MIN_LOAD": st.session_state.get(
                        "efficiency_partial", efficiency_partial_default
                    ),
                    "STOP": efficiency_stop_default,
                },
                "Hour 3": {
                    "RAMP_H": st.session_state.get(
                        "efficiency_hour_3_hot", efficiency_full_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "efficiency_hour_3_warm", efficiency_full_default / 1.8
                    ),
                    "RAMP_C": st.session_state.get(
                        "efficiency_hour_3_cold", efficiency_full_default / 2.2
                    ),
                    "FULL_LOAD": st.session_state.get(
                        "efficiency_full", efficiency_full_default
                    ),
                    "MIN_LOAD": st.session_state.get(
                        "efficiency_partial", efficiency_partial_default
                    ),
                    "STOP": efficiency_stop_default,
                },
                "Hour 4": {
                    "RAMP_H": st.session_state.get(
                        "efficiency_full", efficiency_full_default
                    ),
                    "RAMP_W": st.session_state.get(
                        "efficiency_hour_4_warm",
                        st.session_state.get(
                            "efficiency_full", efficiency_full_default
                        ),
                    ),
                    "RAMP_C": st.session_state.get(
                        "efficiency_hour_4_cold",
                        st.session_state.get(
                            "efficiency_full", efficiency_full_default
                        ),
                    ),
                    "FULL_LOAD": st.session_state.get(
                        "efficiency_full", efficiency_full_default
                    ),
                    "MIN_LOAD": st.session_state.get(
                        "efficiency_partial", efficiency_partial_default
                    ),
                    "STOP": efficiency_stop_default,
                },
            }
        )

        constraints_df = pd.DataFrame(
            {
                "Use": {
                    "Min hours on": st.session_state.get(
                        "min_hours_on", min_hours_on_default
                    ),
                    "Min hours off": st.session_state.get(
                        "min_hours_off", min_hours_off_default
                    ),
                    "Max Nb Starts A day": 100,
                    "Startup Cost": st.session_state.get(
                        "startup_cost", startup_cost_default
                    ),
                    "Variable Cost": st.session_state.get(
                        "variable_cost", variable_cost_default
                    ),
                    "Hourly fixed cost": st.session_state.get(
                        "hourly_fixed_cost", hourly_fixed_cost_default
                    ),
                    "Emission Factor": st.session_state.get(
                        "emission_factor", emission_factor_default
                    ),
                }
            }
        )

        price_df = pd.read_csv("deploy/data/unified_energy_dataset.csv")
        price_df["Datetime"] = pd.to_datetime(price_df["Datetime"])

        # Filter for April 2025
        filtered_price_df = price_df[
            (price_df["Datetime"].dt.year == 2025)
            & (price_df["Datetime"].dt.month == 5)
        ][["Datetime", "BE", "ZTP", "EUA Prices"]]
        filtered_price_df = filtered_price_df.rename(
            columns={"BE": "power_price", "ZTP": "gas_price", "EUA Prices": "co2_price"}
        )

        # Add incremental hour column starting from 0
        filtered_price_df["hour"] = range(len(filtered_price_df))
        filtered_price_df = filtered_price_df.set_index("hour")

        def compute_state_values(
            state, hour, constraints_df, power_df, efficiency_df, startup=False
        ):

            load = power_df.loc[state, f"Hour {hour}"]
            efficiency = efficiency_df.loc[state, f"Hour {hour}"] / 100
            startup_cost = constraints_df.loc["Startup Cost", "Use"] if startup else 0
            fixed_cost = startup_cost + constraints_df.loc["Hourly fixed cost", "Use"]
            variable_cost = load * constraints_df.loc["Variable Cost", "Use"]
            gas = load / efficiency if efficiency != 0 else 0

            return load, efficiency, fixed_cost, variable_cost, gas

        def create_list_states(state_df, constraints_df, power_df, efficiency_df):

            columns = [
                "load",
                "efficiency",
                "fixed_cost",
                "variable_cost",
                "off",
                "minload",
                "fullload",
                "gas",
            ]
            df_status = pd.DataFrame(columns=columns)
            df_status.index.name = "status"

            # 3 transitions possibles

            min_hours_on = int(constraints_df.loc["Min hours on", "Use"])

            for state in state_df.index:

                # on commence pour les pentes
                if state.startswith("RAMP"):
                    ramp_to_full = state_df.loc[state, "Hours to Reach Full Load"]
                    for i in range(1, min_hours_on + 1):
                        if i < ramp_to_full:
                            next_state = f"{state}-{i+1}"
                            label = f"{state}-{i}"
                            startup = i == 1
                        elif i == ramp_to_full and i < min_hours_on:
                            next_state = f"FULL_LOAD-{i+1}"
                            label = f"{state}-{i}"
                            startup = i == 1
                        elif i > ramp_to_full and i < min_hours_on:
                            next_state = f"FULL_LOAD-{i+1}"
                            label = f"FULL_LOAD-{i}"
                            startup = False
                        elif i == min_hours_on:
                            next_state = "FULL_LOAD"
                            label = f"FULL_LOAD-{i}"
                            startup = False

                        load, eff, fixed, var_cost, gas = compute_state_values(
                            "FULL_LOAD" if i > ramp_to_full else state,
                            1 if i > ramp_to_full else i,
                            constraints_df,
                            power_df,
                            efficiency_df,
                            startup=startup,
                        )

                        df_status.loc[label] = [
                            load,
                            eff,
                            fixed,
                            var_cost,
                            next_state,
                            next_state,
                            next_state,
                            gas,
                        ]

                elif state in ["FULL_LOAD", "MIN_LOAD", "STOP"]:

                    load, eff, fixed, var_cost, gas = compute_state_values(
                        state, 1, constraints_df, power_df, efficiency_df, startup=False
                    )

                    next_states = {
                        "FULL_LOAD": ("STOP", "MIN_LOAD", "FULL_LOAD"),
                        "MIN_LOAD": ("STOP", "MIN_LOAD", "FULL_LOAD"),
                        "STOP": ("OFF_1", "OFF_1", "OFF_1"),
                    }

                    off, minload, fullload = next_states[state]
                    df_status.loc[state] = [
                        load,
                        eff,
                        fixed,
                        var_cost,
                        off,
                        minload,
                        fullload,
                        gas,
                    ]

            range_off = state_df["Use < XX off hours"].nlargest(2).iloc[-1]
            hot_limit = state_df["Use < XX off hours"].nlargest(3).iloc[-1]
            min_hours_off = int(constraints_df.loc["Min hours off", "Use"])

            for i in range(1, range_off + 1):

                status = f"OFF_{i}"
                load = eff = fixed = var_cost = gas = 0

                if i < min_hours_off:
                    target = f"OFF_{i+1}"
                    fullload = target
                elif i == range_off:
                    target = "OFF"
                    fullload = "RAMP_C-1"
                elif i < hot_limit:
                    target = f"OFF_{i+1}"
                    fullload = "RAMP_H-1"
                else:
                    target = f"OFF_{i+1}"
                    fullload = "RAMP_W-1"

                df_status.loc[status] = [
                    load,
                    eff,
                    fixed,
                    var_cost,
                    target,
                    target,
                    fullload,
                    gas,
                ]

            # Static OFF state
            df_status.loc["OFF"] = [0, 0, 0, 0, "OFF", "OFF", "RAMP_C-1", 0]

            return df_status

        transition_df = create_list_states(
            state_df, constraints_df, power_df, efficiency_df
        )

        st.dataframe(transition_df)

        def bellman_optimization(
            transition_df, prices_df, start_state, window, ef=0.18
        ):

            # Initialization: create value and policy tables
            V = [{} for _ in range(window + 1)]  # V[t][state] = value
            policy = [{} for _ in range(window)]

            # Terminal condition: V[window] = 0 for all states
            for state in transition_df.index:
                V[window][state] = 0

            for t in reversed(range(window)):
                power_price = prices_df.loc[t, "power_price"]
                gas_price = prices_df.loc[t, "gas_price"]
                co2_price = prices_df.loc[t, "co2_price"]

                for state in transition_df.index:
                    row = transition_df.loc[state]
                    # Compute revenue and cost
                    revenue = row["load"] * power_price
                    fuel_cost = row["gas"] * gas_price
                    co2_cost = row["gas"] * ef * co2_price
                    total_cost = (
                        row["fixed_cost"] + row["variable_cost"] + fuel_cost + co2_cost
                    )
                    profit = revenue - total_cost

                    # Check possible next states
                    next_states = [row["off"], row["minload"], row["fullload"]]
                    best_value = -np.inf
                    best_next = None

                    for next_state in next_states:
                        if next_state in V[t + 1]:
                            val = profit + V[t + 1][next_state]
                            if val > best_value:
                                best_value = val
                                best_next = next_state

                    V[t][state] = best_value
                    policy[t][state] = best_next

            return V, policy

        v, policy = bellman_optimization(
            transition_df, filtered_price_df, "OFF_20", 744, ef=0.18
        )
        path = []
        state = "OFF_20"
        for t in range(744):
            path.append(state)
            state = policy[t].get(state, None)
            if state is None:
                break

        final_df = filtered_price_df.copy()
        final_df["Path"] = path

        # Ensure merged_df is sorted by time
        merged_df = final_df.merge(transition_df, left_on="Path", right_index=True)
        merged_df = merged_df.sort_values("Datetime").reset_index(drop=True)

        # Constants
        EFFICIENCY = (
            st.session_state.get("efficiency_full", efficiency_full_default) / 100
        )
        EMISSION_FACTOR = st.session_state.get(
            "emission_factor", emission_factor_default
        )

        # --- Compute CSS ---
        merged_df["CSS"] = merged_df["power_price"] - (
            merged_df["gas_price"] / EFFICIENCY
            + merged_df["co2_price"] * EMISSION_FACTOR
        )

        # --- Compute fuel cost only ---
        merged_df["fuel_cost"] = merged_df["load"] * (
            merged_df["gas_price"] / EFFICIENCY
            + merged_df["co2_price"] * EMISSION_FACTOR
        )

        # --- Compute each revenue stream ---
        merged_df["gross_revenue"] = merged_df["power_price"] * merged_df["load"]
        merged_df["revenue_after_fuel"] = (
            merged_df["gross_revenue"] - merged_df["fuel_cost"]
        )
        merged_df["net_revenue"] = (
            merged_df["revenue_after_fuel"]
            - merged_df["fixed_cost"]
            - merged_df["variable_cost"]
        )

        # --- Compute cumulative sums ---
        merged_df["cumulative_gross"] = merged_df["gross_revenue"].cumsum()
        merged_df["cumulative_after_fuel"] = merged_df["revenue_after_fuel"].cumsum()
        merged_df["cumulative_net"] = merged_df["net_revenue"].cumsum()

        # --- Plot ---
        fig, axs = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

        # Subplot 1: Load + CSS
        x = pd.to_datetime(merged_df["Datetime"]).to_numpy()
        y = merged_df["CSS"].astype(float).to_numpy()
        mask = y > 0

        axs[0].bar(
            x, merged_df["load"], width=0.03, label="Optimal Load (MW)", color="#ADD8E6"
        )
        axs[0].set_ylabel("Load (MW)", color="black")
        axs[0].tick_params(axis="y", labelcolor="black")
        axs[0].set_ylim(-300, 500)

        ax2 = axs[0].twinx()
        ax2.plot(
            x, y, label="Clean Spark Spread (€/MWh)", color="black", linestyle="--"
        )
        ax2.fill_between(
            x, 0, y, where=mask, interpolate=True, color="green", alpha=0.3
        )
        ax2.set_ylabel("CSS (€/MWh)", color="black")
        ax2.tick_params(axis="y", labelcolor="black")
        ax2.set_ylim(-300, 500)

        axs[0].set_title("Optimal Load and Clean Spark Spread")

        # Subplot 2: Cumulative Revenues
        axs[1].plot(
            x,
            merged_df["cumulative_after_fuel"],
            label="Market revenues",
            color="orange",
            linestyle="-",
        )
        axs[1].plot(
            x,
            merged_df["cumulative_net"],
            label="Net Revenue (All Costs)",
            color="green",
            linewidth=2,
        )

        axs[1].set_ylabel("Cumulative Revenue (€)")
        axs[1].set_title("Cumulative Revenue Over Time")
        axs[1].legend()

        # Grid and formatting
        for ax in axs:
            ax.grid(True, linestyle="--", alpha=0.5)

        plt.xlabel("Datetime")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Press the button above to run optimization.")

# Page 2: Placeholder for future pages
elif page == "Other page (placeholder)":
    st.title("Other Page")
    st.write(
        "This is a placeholder for future pages (e.g. Input Tables, Optimisation, Results)."
    )
