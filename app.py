import streamlit as st
import pandas as pd
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    subprocess.check_call(["pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
import pkg_resources

installed_packages = [pkg.key for pkg in pkg_resources.working_set]
print("Installed packages:", installed_packages)

import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess

# Ensure matplotlib is installed




# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("AZ Post-2024.csv")  # Ensure correct file path
    df.dropna(subset=["District ID"], inplace=True)  # Drop missing District IDs
    df["District ID"] = df["District ID"].astype(str).str.strip()
    return df

df = load_data()

# Sidebar for navigation
st.sidebar.header("📌 Select Visualization")
chart_type = st.sidebar.radio("Choose a Chart", [
    "Governor Race", "Senate Race", "Secretary of State & Attorney General",
    "Age Distribution", "Income Distribution", "District-Specific Analysis"
])

### 📌 Bar Chart Function
def plot_bar_chart(columns, labels, colors, title):
    x = np.arange(len(df))
    width = 0.2 if len(columns) > 3 else 0.3  # Adjust bar width dynamically

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, col in enumerate(columns):
        ax.bar(x + (i * width) - (width * (len(columns) / 2)), df[col], width=width, label=labels[i], color=colors[i])

    ax.set_xlabel("Districts")
    ax.set_ylabel("Votes")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(df["District ID"], rotation=90, fontsize=8)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    st.pyplot(fig)

### 📌 Election Charts
if chart_type == "Governor Race":
    plot_bar_chart(
        columns=["G22GovD", "G22GovR"],
        labels=["Democrat", "Republican"],
        colors=["blue", "red"],
        title="🗳️ 2022 Governor Race"
    )

elif chart_type == "Senate Race":
    plot_bar_chart(
        columns=["G22SenD", "G22SenR", "G22SenO"],
        labels=["Democrat", "Republican", "Other"],
        colors=["blue", "red", "gray"],
        title="🗳️ 2022 Senate Race"
    )

elif chart_type == "Secretary of State & Attorney General":
    plot_bar_chart(
        columns=["G22SosD", "G22SosR", "G22AgD", "G22AgR"],
        labels=["Sos-Dem", "Sos-Rep", "Ag-Dem", "Ag-Rep"],
        colors=["blue", "red", "lightblue", "darkred"],
        title="🗳️ Secretary of State & Attorney General Results"
    )

### 📌 Demographic Charts
elif chart_type == "Age Distribution":
    plot_bar_chart(
        columns=["D20Minus", "D20to40", "D40to65", "D65Plus"],
        labels=["<20", "20-40", "40-65", "65+"],
        colors=["lightblue", "blue", "darkblue", "gray"],
        title="👥 Age Distribution by District"
    )

elif chart_type == "Income Distribution":
    plot_bar_chart(
        columns=["D0_25k", "D25k_50k", "D50k_100k", "D100k_200k", "D200kPlus"],
        labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
        colors=["lightgreen", "green", "darkgreen", "blue", "darkblue"],
        title="💰 Income Distribution by District"
    )

### 📌 District-Specific Charts
elif chart_type == "District-Specific Analysis":
    district_options = df["District ID"].unique()
    selected_district = st.sidebar.selectbox("🏙️ Select a District", district_options)

    if selected_district:
        district_data = df[df["District ID"] == selected_district].iloc[0]  # Get data for selected district

        # Pie Chart Function
        def plot_pie_chart(values, labels, colors, title):
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
            ax.set_title(title)
            st.pyplot(fig)

        # 🏙️ District Overview
        st.subheader(f"📍 {selected_district} Overview")

        # 📊 Pie Chart: Age Distribution
        plot_pie_chart(
            values=[district_data["D20Minus"], district_data["D20to40"], district_data["D40to65"], district_data["D65Plus"]],
            labels=["<20", "20-40", "40-65", "65+"],
            colors=["lightblue", "blue", "darkblue", "gray"],
            title="👥 Age Distribution"
        )

        # 💰 Pie Chart: Income Distribution
        plot_pie_chart(
            values=[district_data["D0_25k"], district_data["D25k_50k"], district_data["D50k_100k"], district_data["D100k_200k"], district_data["D200kPlus"]],
            labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
            colors=["lightgreen", "green", "darkgreen", "blue", "darkblue"],
            title="💰 Income Distribution"
        )

        # 🗳️ Pie Chart: Governor Election
        plot_pie_chart(
            values=[district_data["G22GovD"], district_data["G22GovR"]],
            labels=["Democrat", "Republican"],
            colors=["blue", "red"],
            title="🗳️ Governor Election"
        )

        # 🗳️ Pie Chart: Senate Election
        plot_pie_chart(
            values=[district_data["G22SenD"], district_data["G22SenR"], district_data["G22SenO"]],
            labels=["Democrat", "Republican", "Other"],
            colors=["blue", "red", "gray"],
            title="🗳️ Senate Election"
        )
