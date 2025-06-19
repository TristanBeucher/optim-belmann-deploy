import streamlit as st
from utils.dataframes import (
    build_constraints_df,
    build_efficiency_df,
    build_power_df,
    build_state_df,
    load_price_df,
)
from utils.optimization import bellman_optimization
from utils.plots import plot_dispatch_chart
from utils.transition import create_list_states


def render_optimal_dispatch(defaults, initial_state):

    st.title("Optimal Dispatch")

    # --- Selectors ---
    st.markdown("### Select Simulation Parameters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        country = st.selectbox("Country", options=["Belgium", "France"], index=0)

    with col2:
        trading_point = st.selectbox(
            "Gas Trading Point", options=["ZTP", "PEG"], index=0
        )

    with col3:
        month_label = st.selectbox("Month", options=["April", "May", "June"], index=1)

    with col4:
        year = st.selectbox("Year", options=[2025], index=0)

    # Map month label to numerical value
    month_map = {"April": 4, "May": 5, "June": 6}
    month = month_map[month_label]

    st.markdown(
        f"**Selected Period**: {month_label} {year} for {country} and {trading_point} gas trading point"
    )

    offline_limit_hours_warm = st.session_state.get(
        "offline_limit_hours_warm", st.session_state["offline_limit_hours_warm"]
    )

    initial_mode = st.radio("Is the plant initially ON or OFF?", ["ON", "OFF"])

    if initial_mode == "ON":
        initial_state = "FULL_LOAD"
    else:
        off_hours = st.number_input(
            "How many hours has the plant been OFF?",
            min_value=0,
            max_value=9999,
            value=20,
        )
        # Get limit from defaults
        if off_hours > offline_limit_hours_warm:
            initial_state = "OFF"
        else:
            initial_state = f"OFF_{off_hours}"

    if st.button("Run Optimization"):

        efficiency = (
            st.session_state.get("efficiency_full", defaults["efficiency_full"]) / 100
        )
        emission_factor = st.session_state.get(
            "emission_factor", defaults["emission_factor"]
        )

        constraints_df = build_constraints_df(defaults)
        efficiency_df = build_efficiency_df(defaults)
        power_df = build_power_df(defaults)
        state_df = build_state_df(defaults)
        filtered_price_df = load_price_df(
            "data/unified_energy_dataset.csv", country, trading_point, year, month
        )

        transition_df = create_list_states(
            state_df, constraints_df, power_df, efficiency_df
        )

        v, policy = bellman_optimization(
            transition_df,
            filtered_price_df,
            initial_state,
            filtered_price_df.shape[0],
            emission_factor,
        )
        path = []
        state = initial_state
        for t in range(filtered_price_df.shape[0]):
            path.append(state)
            state = policy[t].get(state, None)
            if state is None:
                break

        final_df = filtered_price_df.copy()
        final_df["Path"] = path

        # Ensure merged_df is sorted by time
        merged_df = final_df.merge(transition_df, left_on="Path", right_index=True)
        merged_df = merged_df.sort_values("Datetime").reset_index(drop=True)

        # --- Compute CSS ---
        merged_df["CSS"] = merged_df["power_price"] - (
            merged_df["gas_price"] / efficiency
            + merged_df["co2_price"] * emission_factor
        )

        # --- Compute fuel cost only ---
        merged_df["fuel_cost"] = merged_df["load"] * (
            merged_df["gas_price"] / efficiency
            + merged_df["co2_price"] * emission_factor
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

        total_revenue = merged_df["cumulative_net"].iloc[-1]
        total_production = merged_df["load"].cumsum().iloc[-1]
        revenue_per_MWh = total_revenue / total_production
        nb_hours_on = len(merged_df[merged_df["load"] > 0]["load"])
        nb_start = len(
            merged_df[merged_df["Path"].isin(["RAMP_H-1", "RAMP_W-1", "RAMP_C-1"])][
                "Path"
            ]
        )

        st.markdown(
            f"""
        - **Initital state**: at the first hour of the month the plant was in state {merged_df["Path"].iloc[0]}   
        - **Total revenue**: the expected revenue from the application of the optimal program is {int(total_revenue)} €  
        - **Total production**: the expected revenue from the application of the optimal program is {total_production} MWh
        - **Revenue per MWh**: the revenue per MWh is then {round(revenue_per_MWh,2)} € / MWh  
        - **Number of hours on**: during the month, the plant has been running for {nb_hours_on} hours 
        - **Number of starts**: during the month, the plant has started {nb_start} times 
        - **Final state**: at the last hour of the month, the plant is in state {merged_df["Path"].iloc[-1]}  
        """
        )

        st.info(
            "The charts below represent the production profile derived from the optimal program and the associated revenue "
            "(on the second graph). The production (in light blue) is put in perspective with Clean Spark Spreads (dashed black line and green fill when positive) "
            "for the considered period."
        )

        st.pyplot(plot_dispatch_chart(merged_df))

        st.subheader("Results raw data ")

        st.info(
            "In the table below, you can check the market and production data for the considered period."
        )

        st.dataframe(merged_df.drop(columns=["off", "minload", "fullload"]))

        st.subheader("Transition Matrix")

        st.info(
            "Below is the transition between states matrix created from the different parameters you can find "
            "on the Summary page"
        )

        st.dataframe(transition_df)

    else:
        st.info("Press the button above to run optimization.")
