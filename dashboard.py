import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Stairvision Safety Monitor",
    page_icon="🚨",
    layout="wide"
)

# Dashboard Title
st.title("🏭 Industrial Safety Monitoring Dashboard")
st.markdown("Real-time monitoring for **Stairvision Area 1**")

# --- DATA LOADING FUNCTION ---
def get_data():
    try:
        conn = sqlite3.connect("stairvision_logs.db")
        df = pd.read_sql_query("SELECT * FROM incidents", conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

# --- MAIN CONTAINER ---
placeholder = st.empty()

while True:
    df = get_data()

    with placeholder.container():
        # 1. METRICS (KPI)
        kpi1, kpi2, kpi3 = st.columns(3)

        # Calculate Total Incidents
        total_incidents = len(df)
        
        # Calculate Today's Incidents
        if not df.empty:
            today = pd.Timestamp.now().normalize()
            today_incidents = df[df['timestamp'] >= today].shape[0]
            last_incident_time = df['timestamp'].max().strftime("%H:%M:%S")
        else:
            today_incidents = 0
            last_incident_time = "-"

        # Display KPIs
        kpi1.metric(
            label="Total Violations (All Time)",
            value=total_incidents,
            delta=None
        )
        
        kpi2.metric(
            label="Violations Today",
            value=today_incidents,
            delta="Live",
            delta_color="inverse" # Red if it increases (bad for safety)
        )
        
        kpi3.metric(
            label="Last Incident Time",
            value=last_incident_time
        )

        st.markdown("---")

        # 2. CHARTS & DATA
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Violation Trend per Hour")
            if not df.empty:
                # Group data by hour
                df['hour'] = df['timestamp'].dt.hour
                hourly_counts = df.groupby('hour').size()
                
                # Display Bar Chart
                st.bar_chart(hourly_counts)
            else:
                st.info("No data available for visualization.")

        with col2:
            st.subheader("Logs & Visual Evidence")
            if not df.empty:
                # Interactive: Show the last 5 logs
                recent_df = df.sort_values(by='timestamp', ascending=False).head(5)
                
                # Display data table
                st.dataframe(recent_df[['timestamp', 'details']], hide_index=True)

                # Fetch image from the most recent record (Top 1)
                latest_evidence = recent_df.iloc[0]['image_path']
                
                # Check if the photo exists
                if latest_evidence and pd.notna(latest_evidence):
                    st.image(latest_evidence, caption="Latest Violation Evidence", use_container_width=True)
                else:
                    st.info("No photo evidence for this record.")
            else:
                st.write("Waiting for incoming data...")

        time.sleep(1)