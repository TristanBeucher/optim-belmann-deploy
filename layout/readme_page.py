import streamlit as st


def render_readme():

    st.title("Backtesting CCGTs Optimal Dispatch")

    st.info(
        "This app is still a work in progress and errors or inconsistencies may remain."
    )

    st.markdown("### Overview / Purpose")
    st.markdown(
        """
    This application simulates the optimal dispatch strategy for a Combined Cycle Gas Turbine (CCGT) using a Bellman recursion (dynamic programming) approach.
    
    **Goal:** Maximize net revenue while respecting physical and operational constraints.
    
    **Scope:** I assume the market prices are known and, because of that, the program is more related to a backtest of the strategy. For now, only Belgium and France are included in the study. 
                
    This page describes the structure of the application, for more details about the implementation or about the different constraints, please check the article on my blog:
    """
    )

    st.markdown(
        '<a href="https://tristanbeucher.github.io/ccgt-dispatch-optimization-with-bellman-algorithm" target="_blank"></a>',
        unsafe_allow_html=True,
    )

    st.markdown("### How It Works")
    st.markdown(
        """
    - **Inputs:** User-defined plant characteristics (efficiency, cost), ramp-up/down constraints, and market prices.
    - **Engine:** Bellman-based backward dynamic programming algorithm.
    - **Outputs:** Hourly dispatch schedule, revenue streams, and cumulative profit plots.
    """
    )

    st.markdown("### App Structure")
    st.markdown(
        """
    The Plant's characteristics and Ramp Specifications pages aim to help the user design a virtual power plant to run the backtest. 
    As a lot of parameters are involved, it's easy to be lost then make changes with caution.
    - **Plant's Characteristics:** Set power output levels, efficiency, cost parameters.
    - **Ramp Specifications:** Configure HOT, WARM, and COLD ramp behaviors.
    - **Summary:** Review a consolidated table of all configured parameters.
    - **Optimal Dispatch:** Run the optimization and view dispatch path and revenue plots.
    """
    )

    st.markdown("### Assumptions")
    st.markdown(
        """
    - Simulation horizon: fixed number of hours (e.g. 744 for a 31-day month).
    - Prices are deterministic and provided as input.
    - Single unit dispatch (one CCGT unit at a time).
    - Ramp transitions are defined in hours and are strictly respected.
    """
    )

    st.markdown("### Extensibility Ideas")
    st.markdown(
        """
    - Handle price uncertainty with Monte Carlo scenarios.
    - Add export feature (Excel, CSV, JSON).
    - Store/load plant configurations using session files.
    - Add CO2 budget constraints or multiple CCGT units.
    - Improve UI/UX to make the application more convenient
    """
    )

    st.markdown("### References")
    st.markdown(
        """
    - Bellman R. (1957). *Dynamic Programming*.
    - Power plant optimization literature.
    - ENTSO-E and EEX for market pricing data.
    """
    )
