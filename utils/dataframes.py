import pandas as pd
import streamlit as st


def build_constraints_df(defaults: dict) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Use": {
                "Min hours on": st.session_state.get(
                    "min_hours_on", defaults["min_hours_on"]
                ),
                "Min hours off": st.session_state.get(
                    "min_hours_off", defaults["min_hours_off"]
                ),
                "Max Nb Starts A day": 100,
                "Startup Cost": st.session_state.get(
                    "startup_cost", defaults["startup_cost"]
                ),
                "Variable Cost": st.session_state.get(
                    "variable_cost", defaults["variable_cost"]
                ),
                "Hourly fixed cost": st.session_state.get(
                    "hourly_fixed_cost", defaults["hourly_fixed_cost"]
                ),
                "Emission Factor": st.session_state.get(
                    "emission_factor", defaults["emission_factor"]
                ),
            }
        }
    )


def build_efficiency_df(defaults: dict) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Hour 1": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_1_hot", defaults["efficiency_full"] / 2.2
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_1_warm", defaults["efficiency_full"] / 3.5
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_1_cold", defaults["efficiency_full"] / 4.0
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", defaults["efficiency_full"]
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", defaults["efficiency_partial"]
                ),
                "STOP": st.session_state.get(
                    "efficiency_stop", defaults["efficiency_stop"]
                ),
            },
            "Hour 2": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_2_hot", defaults["efficiency_full"]
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_2_warm", defaults["efficiency_full"] / 2.5
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_2_cold", defaults["efficiency_full"] / 3.0
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", defaults["efficiency_full"]
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", defaults["efficiency_partial"]
                ),
                "STOP": defaults["efficiency_stop"],
            },
            "Hour 3": {
                "RAMP_H": st.session_state.get(
                    "efficiency_hour_3_hot", defaults["efficiency_full"]
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_3_warm", defaults["efficiency_full"] / 1.8
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_3_cold", defaults["efficiency_full"] / 2.2
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", defaults["efficiency_full"]
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", defaults["efficiency_partial"]
                ),
                "STOP": defaults["efficiency_stop"],
            },
            "Hour 4": {
                "RAMP_H": st.session_state.get(
                    "efficiency_full", defaults["efficiency_full"]
                ),
                "RAMP_W": st.session_state.get(
                    "efficiency_hour_4_warm",
                    st.session_state.get(
                        "efficiency_full", defaults["efficiency_full"]
                    ),
                ),
                "RAMP_C": st.session_state.get(
                    "efficiency_hour_4_cold",
                    st.session_state.get(
                        "efficiency_full", defaults["efficiency_full"]
                    ),
                ),
                "FULL_LOAD": st.session_state.get(
                    "efficiency_full", defaults["efficiency_full"]
                ),
                "MIN_LOAD": st.session_state.get(
                    "efficiency_partial", defaults["efficiency_partial"]
                ),
                "STOP": defaults["efficiency_stop"],
            },
        }
    )


def build_power_df(defaults: dict) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Hour 1": {
                "RAMP_H": st.session_state.get(
                    "power_hour_1_hot", defaults["power_full"] / 2.0
                ),
                "RAMP_W": st.session_state.get(
                    "power_hour_1_warm", defaults["power_full"] / 3.0
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_1_cold", defaults["power_full"] / 4.0
                ),
                "FULL_LOAD": st.session_state.get("power_full", defaults["power_full"]),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", defaults["power_partial"]
                ),
                "STOP": st.session_state.get("power_stop", defaults["power_stop"]),
            },
            "Hour 2": {
                "RAMP_H": st.session_state.get(
                    "power_hour_2_hot", defaults["power_full"]
                ),
                "RAMP_W": st.session_state.get(
                    "power_hour_2_warm", defaults["power_full"] / 2.0
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_2_cold", defaults["power_full"] / 2.5
                ),
                "FULL_LOAD": st.session_state.get("power_full", defaults["power_full"]),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", defaults["power_partial"]
                ),
                "STOP": defaults["power_stop"],
            },
            "Hour 3": {
                "RAMP_H": st.session_state.get(
                    "power_hour_3_hot", defaults["power_full"]
                ),
                "RAMP_W": st.session_state.get(
                    "power_hour_3_warm", defaults["power_full"] / 1.5
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_3_cold", defaults["power_full"] / 2.0
                ),
                "FULL_LOAD": st.session_state.get("power_full", defaults["power_full"]),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", defaults["power_partial"]
                ),
                "STOP": defaults["power_stop"],
            },
            "Hour 4": {
                "RAMP_H": st.session_state.get("power_full", defaults["power_full"]),
                "RAMP_W": st.session_state.get(
                    "power_hour_4_warm",
                    st.session_state.get("power_full", defaults["power_full"]),
                ),
                "RAMP_C": st.session_state.get(
                    "power_hour_4_cold",
                    st.session_state.get("power_full", defaults["power_full"]),
                ),
                "FULL_LOAD": st.session_state.get("power_full", defaults["power_full"]),
                "MIN_LOAD": st.session_state.get(
                    "power_partial", defaults["power_partial"]
                ),
                "STOP": defaults["power_stop"],
            },
        }
    )


def build_state_df(defaults: dict) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Use < XX off hours": {
                "RAMP_H": st.session_state.get(
                    "offline_limit_hours_hot", defaults["offline_limit_hours_hot"]
                ),
                "RAMP_W": st.session_state.get(
                    "offline_limit_hours_warm", defaults["offline_limit_hours_warm"]
                ),
                "RAMP_C": st.session_state.get(
                    "offline_limit_hours_cold", defaults["offline_limit_hours_cold"]
                ),
                "FULL_LOAD": 0,
                "MIN_LOAD": 0,
                "STOP": 0,
            },
            "Hours to Reach Full Load": {
                "RAMP_H": st.session_state.get(
                    "ramp_hours_hot", defaults["ramp_hours_hot"]
                ),
                "RAMP_W": st.session_state.get(
                    "ramp_hours_warm", defaults["ramp_hours_warm"]
                ),
                "RAMP_C": st.session_state.get(
                    "ramp_hours_cold", defaults["ramp_hours_cold"]
                ),
                "FULL_LOAD": 0,
                "MIN_LOAD": 0,
                "STOP": 0,
            },
        }
    )


def load_price_df(
    csv_path: str, country: str, trading_point: str, year: int, month: int
) -> pd.DataFrame:
    """
    Load and filter the unified energy dataset for a specific year and month.
    Returns a DataFrame indexed by an incremental hour column.
    """

    countries_dic = {"Belgium": "BE", "France": "FR"}

    country_short = countries_dic[country]

    price_df = pd.read_csv(csv_path)
    price_df["Datetime"] = pd.to_datetime(price_df["Datetime"])

    filtered = price_df[
        (price_df["Datetime"].dt.year == year)
        & (price_df["Datetime"].dt.month == month)
    ][["Datetime", country_short, trading_point, "EUA Prices"]]

    filtered = filtered.rename(
        columns={
            country_short: "power_price",
            trading_point: "gas_price",
            "EUA Prices": "co2_price",
        }
    )

    filtered["hour"] = range(len(filtered))
    filtered = filtered.set_index("hour")

    return filtered
