import matplotlib.pyplot as plt
import pandas as pd


def plot_dispatch_chart(merged_df):

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
    ax2.plot(x, y, label="Clean Spark Spread (€/MWh)", color="black", linestyle="--")
    ax2.fill_between(x, 0, y, where=mask, interpolate=True, color="green", alpha=0.3)
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

    return fig


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

    return fig
