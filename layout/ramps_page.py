import streamlit as st


def render_hot_ramp():

    st.info(
        "In this section you can change parameters related to the hot ramp, which is generally the fastest ramp mode. "
        "You can select the limit of off hours to use this ramp, the required time to reach full load, and the power "
        "and efficiency at each step of the ramp"
    )

    power_full = st.session_state.get("power_full", st.session_state["power_full"])
    efficiency_full = st.session_state.get(
        "efficiency_full", st.session_state["efficiency_full"]
    )

    # Offline time limit (XX hours)
    offline_limit_hours_hot = st.number_input(
        "Apply when offline for less than (hours)",
        min_value=1,
        max_value=40,
        value=st.session_state["offline_limit_hours_hot"],
        step=1,
    )
    st.session_state["offline_limit_hours_hot"] = offline_limit_hours_hot

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_hot = st.number_input(
        "Hours to reach full load",
        min_value=1,
        max_value=3,
        value=st.session_state["ramp_hours_hot"],
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
        value=min(st.session_state["power_hour_1_hot"], power_full),
        step=1.0,
    )
    st.session_state["power_hour_1_hot"] = power_hour_1_hot

    efficiency_hour_1_hot = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=min(st.session_state["efficiency_hour_1_hot"], efficiency_full),
        step=0.1,
    )
    st.session_state["efficiency_hour_1_hot"] = efficiency_hour_1_hot

    # Hour 2
    if ramp_hours_hot >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_hot = st.number_input(
            "Power Hour 2 (MW)",
            min_value=min(power_hour_1_hot, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_2_hot"], power_full),
            step=1.0,
        )

        efficiency_hour_2_hot = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=min(efficiency_hour_1_hot, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_2_hot"], efficiency_full),
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
            min_value=min(power_hour_2_hot, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_3_hot"], power_full),
            step=1.0,
        )
        efficiency_hour_3_hot = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=min(efficiency_hour_2_hot, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_3_hot"], efficiency_full),
            step=0.1,
        )
    else:
        power_hour_3_hot = power_full
        efficiency_hour_3_hot = efficiency_full
        st.info("Hour 3 → Full Load parameters applied automatically.")

    st.session_state["power_hour_3_hot"] = power_hour_3_hot
    st.session_state["efficiency_hour_3_hot"] = efficiency_hour_3_hot


def render_warm_ramp():

    st.info(
        "In this section you can change parameters related to warm hot ramp, which is applied when the offline limit for using "
        "hot ramp has been exceeded. "
        "You can select the limit of off hours to use this ramp, the required time to reach full load, and the power "
        "and efficiency at each step of the ramp."
    )

    power_full = st.session_state.get("power_full", st.session_state["power_full"])
    efficiency_full = st.session_state.get(
        "efficiency_full", st.session_state["efficiency_full"]
    )
    offline_limit_hours_hot = st.session_state.get(
        "offline_limit_hours_hot", st.session_state["offline_limit_hours_hot"]
    )
    ramp_hours_hot = st.session_state.get(
        "ramp_hours_hot", st.session_state["ramp_hours_hot"]
    )

    # Offline time limit (XX hours)
    offline_limit_hours_warm = st.number_input(
        "Apply when offline for less than (hours)",
        min_value=offline_limit_hours_hot + 1,
        max_value=200,
        value=st.session_state["offline_limit_hours_warm"],
        step=1,
    )
    st.session_state["offline_limit_hours_warm"] = offline_limit_hours_warm

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_warm = st.number_input(
        "Hours to reach full load",
        min_value=ramp_hours_hot,
        max_value=4,
        value=st.session_state["ramp_hours_warm"],
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
        value=min(st.session_state["power_hour_1_warm"], power_full),
        step=1.0,
    )
    st.session_state["power_hour_1_warm"] = power_hour_1_warm

    efficiency_hour_1_warm = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=min(st.session_state["efficiency_hour_1_warm"], efficiency_full),
        step=0.1,
    )
    st.session_state["efficiency_hour_1_warm"] = efficiency_hour_1_warm

    # Hour 2
    if ramp_hours_warm >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_warm = st.number_input(
            "Power Hour 2 (MW)",
            min_value=min(power_hour_1_warm, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_2_warm"], power_full),
            step=1.0,
        )

        efficiency_hour_2_warm = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=min(efficiency_hour_1_warm, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_2_warm"], efficiency_full),
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
            min_value=min(power_hour_2_warm, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_3_warm"], power_full),
            step=1.0,
        )
        efficiency_hour_3_warm = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=min(efficiency_hour_2_warm, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_3_warm"], efficiency_full),
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
            min_value=min(power_hour_3_warm, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_4_warm"], power_full),
            step=1.0,
        )
        efficiency_hour_4_warm = st.number_input(
            "Efficiency Hour 4 (%)",
            min_value=min(efficiency_hour_3_warm, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_4_warm"], efficiency_full),
            step=0.1,
        )
    else:
        power_hour_4_warm = power_full
        efficiency_hour_4_warm = efficiency_full
        st.info("Hour 4 → Full Load parameters applied automatically.")

    st.session_state["power_hour_4_warm"] = power_hour_4_warm
    st.session_state["efficiency_hour_4_warm"] = efficiency_hour_4_warm


def render_cold_ramp():

    st.info(
        "In this section, you can change parameters related to cold ramp, which is applied when the offline limit for using "
        "warm ramp has been exceeded. As this is the last ramp then there is not need to define a limit for using it. "
        "You can modify the required time to reach full load, and the power "
        "and efficiency at each step of the ramp"
    )

    power_full = st.session_state.get("power_full", st.session_state["power_full"])
    efficiency_full = st.session_state.get(
        "efficiency_full", st.session_state["efficiency_full"]
    )
    ramp_hours_warm = st.session_state.get(
        "ramp_hours_warm", st.session_state["ramp_hours_warm"]
    )

    # Offline time limit (XX hours)
    offline_limit_hours_cold = 9999
    st.session_state["offline_limit_hours_cold"] = offline_limit_hours_cold

    # Ramp duration to full load (XX hours to reach full load)
    ramp_hours_cold = st.number_input(
        "Hours to reach full load",
        min_value=ramp_hours_warm,
        max_value=4,
        value=st.session_state["ramp_hours_cold"],
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
        value=st.session_state["power_hour_1_cold"],
        step=1.0,
        key="power_hour_1_cold_input",
    )

    st.session_state["power_hour_1_cold"] = power_hour_1_cold

    efficiency_hour_1_cold = st.number_input(
        "Efficiency Hour 1 (%)",
        min_value=0.0,
        max_value=efficiency_full,
        value=min(st.session_state["efficiency_hour_1_cold"], efficiency_full),
        step=0.1,
        key="efficiency_hour_1_cold_input",
    )
    st.session_state["efficiency_hour_1_cold"] = efficiency_hour_1_cold

    # Hour 2
    if ramp_hours_cold >= 2:
        st.markdown("**Hour 2**")
        power_hour_2_cold = st.number_input(
            "Power Hour 2 (MW)",
            min_value=min(power_hour_1_cold, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_2_cold"], power_full),
            step=1.0,
            key="power_hour_2_cold_input",
        )

        efficiency_hour_2_cold = st.number_input(
            "Efficiency Hour 2 (%)",
            min_value=min(efficiency_hour_1_cold, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_2_cold"], efficiency_full),
            step=0.1,
            key="efficiency_hour_2_cold_input",
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
            min_value=min(power_hour_2_cold, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_3_cold"], power_full),
            step=1.0,
            key="power_hour_3_cold_input",
        )
        efficiency_hour_3_cold = st.number_input(
            "Efficiency Hour 3 (%)",
            min_value=min(efficiency_hour_2_cold, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_3_cold"], efficiency_full),
            step=0.1,
            key="efficiency_hour_3_cold_input",
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
            min_value=min(power_hour_3_cold, power_full),
            max_value=power_full,
            value=min(st.session_state["power_hour_4_cold"], power_full),
            step=1.0,
            key="power_hour_4_cold_input",
        )
        efficiency_hour_4_cold = st.number_input(
            "Efficiency Hour 4 (%)",
            min_value=min(efficiency_hour_3_cold, efficiency_full),
            max_value=efficiency_full,
            value=min(st.session_state["efficiency_hour_4_cold"], efficiency_full),
            step=0.1,
            key="efficiency_hour_4_cold_input",
        )
    else:
        power_hour_4_cold = power_full
        efficiency_hour_4_cold = efficiency_full
        st.info("Hour 4 → Full Load parameters applied automatically.")

    st.session_state["power_hour_4_cold"] = power_hour_4_cold
    st.session_state["efficiency_hour_4_cold"] = efficiency_hour_4_cold
