import pandas as pd


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

                elif i == ramp_to_full and i == min_hours_on:
                    next_state = "FULL_LOAD"
                    label = f"{state}-{i}"
                    startup = False

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
