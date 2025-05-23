import streamlit as st
import math
import pandas as pd
import numpy as np
import altair as alt

# --- Constants ---
AIR_DENSITY = 1.225  # kg/m^3
GRAVITY = 9.81       # m/s^2

# --- Page Configuration ---
st.set_page_config(page_title="Physics & Engineering Sim", layout="wide")

st.title("Interactive Physics & Engineering Simulation ⚙️")
st.markdown("Explore different physical models by adjusting the parameters below. Graphs update live!")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
simulation_choice = st.sidebar.radio(
    "Choose a Simulation:",
    ("🌬️ Wind Turbine Power",
     "☀️ Solar Panel Energy",
     "🚗 EV Battery Drain",
     "🎯 Projectile Motion")
)

# --- Simulation Components ---

def wind_turbine_power():
    st.header("🌬️ Wind Turbine Power Output")
    st.latex(r"P = \frac{1}{2} \cdot \rho \cdot A \cdot V^3")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Input Parameters")
        wind_speed_input = st.number_input("Current Wind Speed (V) (m/s):", min_value=0.0, value=10.0, step=0.5, format="%.1f")
        blade_length = st.number_input("Turbine Blade Length (r) (m):", min_value=0.1, value=50.0, step=1.0, format="%.1f")
        st.info(f"Air Density ($\\rho$) is set to {AIR_DENSITY} kg/m³")

    area = math.pi * (blade_length ** 2)
    power_watts = 0.5 * AIR_DENSITY * area * (wind_speed_input ** 3)
    power_kw = power_watts / 1000

    with col2:
        st.subheader("Current Results")
        st.metric(label="Swept Area (A)", value=f"{area:,.2f} m²")
        st.metric(label="Power Output (P)", value=f"{power_kw:,.2f} kW")

    st.markdown("---")
    st.subheader("Live Graph: Power vs. Wind Speed")

    # Generate data for the graph
    wind_speeds = np.linspace(0, wind_speed_input * 2 + 5, 50)
    power_data = [0.5 * AIR_DENSITY * area * (v ** 3) / 1000 for v in wind_speeds]
    df = pd.DataFrame({'Wind Speed (m/s)': wind_speeds, 'Power (kW)': power_data})

    # Debugging: Check the DataFrame
    st.write(df)

    # Create and display chart
    chart = alt.Chart(df).mark_line(point=True, tooltip=True).encode(
        x=alt.X('Wind Speed (m/s)', title='Wind Speed (m/s)'),
        y=alt.Y('Power (kW)', title='Power (kW)', scale=alt.Scale(zero=False)),
    ).properties(
        title='Wind Turbine Power Curve'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

def solar_panel_energy():
    st.header("☀️ Solar Panel Energy Production")
    st.latex(r"Energy = Area \cdot Irradiance \cdot Efficiency")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Input Parameters")
        irradiance_input = st.number_input("Current Solar Irradiance (W/m²):", min_value=0, value=1000, step=50)
        area = st.number_input("Area of Solar Panel (m²):", min_value=0.1, value=20.0, step=0.5, format="%.1f")
        efficiency = st.slider("Efficiency (%):", min_value=0, max_value=40, value=18, step=1)

    energy_wh = area * irradiance_input * (efficiency / 100)

    with col2:
        st.subheader("Current Results (for 1 hour)")
        st.metric(label="Energy Produced", value=f"{energy_wh:,.2f} Wh")

    st.markdown("---")
    st.subheader("Live Graph: Energy vs. Solar Irradiance")

    # Generate data for the graph
    irradiance_levels = np.linspace(0, 1400, 50)
    energy_data = [area * irr * (efficiency / 100) for irr in irradiance_levels]
    df = pd.DataFrame({'Solar Irradiance (W/m²)': irradiance_levels, 'Energy (Wh)': energy_data})

    # Debugging: Check the DataFrame
    st.write(df)

    # Create and display chart
    chart = alt.Chart(df).mark_line(point=True, tooltip=True).encode(
        x=alt.X('Solar Irradiance (W/m²)', title='Solar Irradiance (W/m²)'),
        y=alt.Y('Energy (Wh)', title='Energy (Wh)', scale=alt.Scale(zero=False)),
    ).properties(
        title='Solar Panel Output vs. Irradiance'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

def ev_battery_drain():
    st.header("🚗 EV Battery Drain Rate")
    st.latex(r"RemainingCapacity = Capacity - \left(\frac{Distance \cdot ConsumptionRate}{100}\right)")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Input Parameters")
        capacity = st.number_input("Battery Capacity (kWh):", min_value=0.1, value=75.0, step=1.0, format="%.1f")
        consumption = st.number_input("Avg. Consumption (kWh/100 km):", min_value=1.0, value=18.0, step=0.5, format="%.1f")
        distance_input = st.number_input("Current Distance Traveled (km):", min_value=0.0, value=150.0, step=5.0, format="%.1f")

    drained = (distance_input * consumption) / 100
    remaining = capacity - drained

    with col2:
        st.subheader("Current Results")
        st.metric(label="Energy Consumed", value=f"{drained:.2f} kWh")
        if remaining < 0:
            st.metric(label="Remaining Capacity", value="0.00 kWh", delta="-100%", delta_color="inverse")
            st.warning("Battery depleted! You've run out of charge.")
        else:
            st.metric(label="Remaining Capacity", value=f"{remaining:.2f} kWh", delta=f"-{((drained / capacity) * 100):.1f}%")

    st.markdown("---")
    st.subheader("Live Graph: Remaining Capacity vs. Distance")

    # Generate data for the graph
    max_range_est = (capacity * 100 / consumption) * 1.2
    distances = np.linspace(0, max_range_est, 100)
    remaining_data = [max(0, capacity - (d * consumption / 100)) for d in distances]
    df = pd.DataFrame({'Distance (km)': distances, 'Remaining Capacity (kWh)': remaining_data})

    # Debugging: Check the DataFrame
    st.write(df)

    # Create and display chart
    chart = alt.Chart(df).mark_line(point=True, tooltip=True).encode(
        x=alt.X('Distance (km)', title='Distance Traveled (km)'),
        y=alt.Y('Remaining Capacity (kWh)', title='Remaining Capacity (kWh)', scale=alt.Scale(zero=True)),
    ).properties(
        title='EV Battery Charge vs. Distance'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

def projectile_motion():
    st.header("🎯 Projectile Motion")
    st.latex(r"H = \frac{V_0^2 \sin^2(\theta)}{2g} \quad | \quad R = \frac{V_0^2 \sin(2\theta)}{g}")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Input Parameters")
        velocity = st.number_input("Initial Velocity (V₀) (m/s):", min_value=0.0, value=50.0, step=1.0, format="%.1f")
        angle_deg = st.slider("Launch Angle (θ) (degrees):", min_value=0, max_value=90, value=45, step=1)
        st.info(f"Gravity (g) is set to {GRAVITY} m/s²")

    angle_rad = math.radians(angle_deg)

    # Calculate projectile motion parameters
    if angle_deg == 0 or velocity == 0:
        max_height = 0
        range_val = 0
        time_of_flight = 0
    elif angle_deg == 90:
        max_height = (velocity ** 2) / (2 * GRAVITY)
        range_val = 0
        time_of_flight = (2 * velocity) / GRAVITY
    else:
        max_height = (velocity ** 2 * math.sin(angle_rad) ** 2) / (2 * GRAVITY)
        range_val = (velocity ** 2 * math.sin(2 * angle_rad)) / GRAVITY
        time_of_flight = (2 * velocity * math.sin(angle_rad)) / GRAVITY

    with col2:
        st.subheader("Current Results")
        st.metric(label="Maximum Height (H)", value=f"{max_height:.2f} m")
        st.metric(label="Range (R)", value=f"{range_val:.2f} m")
        st.metric(label="Time of Flight (T)", value=f"{time_of_flight:.2f} s")

    st.markdown("---")
    st.subheader("Live Graph: Projectile Trajectory")

    if time_of_flight > 0:
        # Generate data for the graph
        t = np.linspace(0, time_of_flight, 100)
        x_coords = velocity * math.cos(angle_rad) * t
        y_coords = (velocity * math.sin(angle_rad) * t) - (0.5 * GRAVITY * t**2)
        df = pd.DataFrame({'x': x_coords, 'y': y_coords})

        # Debugging: Check the DataFrame
        st.write(df)

        # Create and display chart
        chart = alt.Chart(df).mark_line(tooltip=True).encode(
            x=alt.X('x', title='Horizontal Distance (m)'),
            y=alt.Y('y', title='Vertical Distance (m)', scale=alt.Scale(zero=True)),
        ).properties(
            title='Projectile Path'
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No trajectory to plot (initial velocity or launch angle is zero).")


# --- Display Selected Simulation ---

if simulation_choice == "🌬️ Wind Turbine Power":
    wind_turbine_power()
elif simulation_choice == "☀️ Solar Panel Energy":
    solar_panel_energy()
elif simulation_choice == "🚗 EV Battery Drain":
    ev_battery_drain()
elif simulation_choice == "🎯 Projectile Motion":
    projectile_motion()

st.sidebar.markdown("---")
st.sidebar.info("App created using Streamlit.")
