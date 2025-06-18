import numpy as np

print("optimization.py successfully loaded.")


def bellman_optimization(transition_df, prices_df, start_state, window, ef=0.18):

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
            total_cost = row["fixed_cost"] + row["variable_cost"] + fuel_cost + co2_cost
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
