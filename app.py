import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

### 📌 Bar Chart Function (Plotly)
def plot_bar_chart(columns, labels, colors, title):
    df_chart = df[["District ID"] + columns].melt(id_vars="District ID", var_name="Category", value_name="Votes")
    fig = px.bar(df_chart, x="District ID", y="Votes", color="Category",
                 color_discrete_map=dict(zip(columns, colors)), barmode="group", title=title)
    st.plotly_chart(fig)

### 📌 Election Charts
if chart_type == "Governor Race":
    plot_bar_chart(
        columns=["G22GovD", "G22GovR"],
        labels=["Democrat", "Republican"],
        colors={"G22GovD": "blue", "G22GovR": "red"},
        title="🗳️ 2022 Governor Race"
    )

elif chart_type == "Senate Race":
    plot_bar_chart(
        columns=["G22SenD", "G22SenR", "G22SenO"],
        labels=["Democrat", "Republican", "Other"],
        colors={"G22SenD": "blue", "G22SenR": "red", "G22SenO": "gray"},
        title="🗳️ 2022 Senate Race"
    )

elif chart_type == "Secretary of State & Attorney General":
    plot_bar_chart(
        columns=["G22SosD", "G22SosR", "G22AgD", "G22AgR"],
        labels=["Sos-Dem", "Sos-Rep", "Ag-Dem", "Ag-Rep"],
        colors={"G22SosD": "blue", "G22SosR": "red", "G22AgD": "lightblue", "G22AgR": "darkred"},
        title="🗳️ Secretary of State & Attorney General Results"
    )

### 📌 Demographic Charts
elif chart_type == "Age Distribution":
    plot_bar_chart(
        columns=["D20Minus", "D20to40", "D40to65", "D65Plus"],
        labels=["<20", "20-40", "40-65", "65+"],
        colors={"D20Minus": "lightblue", "D20to40": "blue", "D40to65": "darkblue", "D65Plus": "gray"},
        title="👥 Age Distribution by District"
    )

elif chart_type == "Income Distribution":
    plot_bar_chart(
        columns=["D0_25k", "D25k_50k", "D50k_100k", "D100k_200k", "D200kPlus"],
        labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
        colors={"D0_25k": "lightgreen", "D25k_50k": "green", "D50k_100k": "darkgreen", "D100k_200k": "blue", "D200kPlus": "darkblue"},
        title="💰 Income Distribution by District"
    )

### 📌 District-Specific Charts
elif chart_type == "District-Specific Analysis":
    district_options = df["District ID"].unique()
    selected_district = st.sidebar.selectbox("🏙️ Select a District", district_options)

    if selected_district:
        district_data = df[df["District ID"] == selected_district].iloc[0]

        # 📌 Pie Chart Function (Plotly)
        def plot_pie_chart(values, labels, colors, title):
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
            fig.update_layout(title=title)
            st.plotly_chart(fig)

        st.subheader(f"📍 {selected_district} Overview")

        # 📊 Age Distribution Pie Chart
        plot_pie_chart(
            values=[district_data["D20Minus"], district_data["D20to40"], district_data["D40to65"], district_data["D65Plus"]],
            labels=["<20", "20-40", "40-65", "65+"],
            colors=["lightblue", "blue", "darkblue", "gray"],
            title="👥 Age Distribution"
        )

        # 💰 Income Distribution Pie Chart
        plot_pie_chart(
            values=[district_data["D0_25k"], district_data["D25k_50k"], district_data["D50k_100k"], district_data["D100k_200k"], district_data["D200kPlus"]],
            labels=["<$25k", "$25k-$50k", "$50k-$100k", "$100k-$200k", "$200k+"],
            colors=["lightgreen", "green", "darkgreen", "blue", "darkblue"],
            title="💰 Income Distribution"
        )

        # 🗳️ Governor Election Pie Chart
        plot_pie_chart(
            values=[district_data["G22GovD"], district_data["G22GovR"]],
            labels=["Democrat", "Republican"],
            colors=["blue", "red"],
            title="🗳️ Governor Election"
        )

        # 🗳️ Senate Election Pie Chart
        plot_pie_chart(
            values=[district_data["G22SenD"], district_data["G22SenR"], district_data["G22SenO"]],
            labels=["Democrat", "Republican", "Other"],
            colors=["blue", "red", "gray"],
            title="🗳️ Senate Election"
        )