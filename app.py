import streamlit as st
import subprocess
import sys

# Ensure plotly is installed
try:
    import plotly.express as px
except ModuleNotFoundError:
    subprocess.run([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.express as px

import plotly
print(plotly.__version__)  # Should output something like 5.15.0+

import pandas as pd


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("AZ Post-2024.csv")  
    df.dropna(subset=["District ID"], inplace=True)  # Drop rows with missing District ID
    df["District ID"] = df["District ID"].astype(str).str.strip()  
    return df

df = load_data()

# 🔹 Sidebar for chart selection
st.sidebar.header("📌 Select Visualization")
chart_type = st.sidebar.selectbox("Choose a Chart Type", [
    "Governor Race", "Senate Race", "Secretary of State & Attorney General",
    "Age Distribution", "Income Distribution", "District-Specific Analysis"
])

# ✅ Debug: Ensure correct selection
st.sidebar.write(f"**DEBUG:** Selected Chart - {chart_type}")  # Can remove later

### 📌 Generic Bar Chart Function (Plotly)
def plot_bar_chart(columns, labels, title):
    df_melted = df.melt(id_vars=["District ID"], value_vars=columns, var_name="Category", value_name="Votes")
    fig = px.bar(df_melted, x="District ID", y="Votes", color="Category", 
                 title=title, labels={"District ID": "District", "Votes": "Number of Votes"},
                 color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

### 📌 Election Charts (Bar Plots)
if chart_type == "Governor Race":
    plot_bar_chart(["G22GovD", "G22GovR"], ["Democrat", "Republican"], "🗳️ 2022 Governor Race")


elif chart_type == "Senate Race":
    plot_bar_chart(
        columns=["G22SenD", "G22SenR", "G22SenO"],
        labels=["Democrat", "Republican", "Other"],
        title="🗳️ 2022 Senate Race"
    )

elif chart_type == "Secretary of State & Attorney General":
    plot_bar_chart(
        columns=["G22SosD", "G22SosR", "G22AgD", "G22AgR"],
        labels=["Sos-Dem", "Sos-Rep", "Ag-Dem", "Ag-Rep"],
        title="🗳️ Secretary of State & Attorney General Results"
    )

### 📌 Demographic Charts (Bar Plots)
elif chart_type == "Age Distribution":
    plot_bar_chart(
        columns=["D20Minus", "D20to40", "D40to65", "D65Plus"],
        labels=["<20", "20-40", "40-65", "65+"],
        title="👥 Age Distribution by District"
    )

elif chart_type == "Income Distribution":
    plot_bar_chart(
        columns=["D0_25k", "D25k_50k", "D50k_100k", "D100k_200k", "D200kPlus"],
        labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
        title="💰 Income Distribution by District"
    )

### 📌 District-Specific Charts
elif chart_type == "District-Specific Analysis":
    district_options = df["District ID"].unique()
    selected_district = st.sidebar.selectbox("🏙️ Select a District", district_options)

    if selected_district:
        district_data = df[df["District ID"] == selected_district].iloc[0]  # Get data for selected district

        # 📌 Generic Pie Chart Function (Plotly)
        def plot_pie_chart(values, labels, title):
            fig = px.pie(names=labels, values=values, title=title, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig)

        # 🏙️ District Overview
        st.subheader(f"📍 {selected_district} Overview")

        # 📊 Pie Chart: Age Distribution
        plot_pie_chart(
            values=[district_data["D20Minus"], district_data["D20to40"], district_data["D40to65"], district_data["D65Plus"]],
            labels=["<20", "20-40", "40-65", "65+"],
            title="👥 Age Distribution"
        )

        # 💰 Pie Chart: Income Distribution
        plot_pie_chart(
            values=[district_data["D0_25k"], district_data["D25k_50k"], district_data["D50k_100k"], district_data["D100k_200k"], district_data["D200kPlus"]],
            labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
            title="💰 Income Distribution"
        )

        # 🗳️ Pie Chart: Governor Election
        plot_pie_chart(
            values=[district_data["G22GovD"], district_data["G22GovR"]],
            labels=["Democrat", "Republican"],
            title="🗳️ Governor Election"
        )

        # 🗳️ Pie Chart: Senate Election
        plot_pie_chart(
            values=[district_data["G22SenD"], district_data["G22SenR"], district_data["G22SenO"]],
            labels=["Democrat", "Republican", "Other"],
            title="🗳️ Senate Election"
        )
