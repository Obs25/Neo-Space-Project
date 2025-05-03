
import streamlit as st
import mysql.connector as db
import pandas as pd
from datetime import datetime, timedelta


st.set_page_config(
    page_title="☄️ NEO Explorer",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("☄️ NEO Explorer: Asteroid Insights")
st.markdown("*Visualizing NASA NEO Data*")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Obuli25052004#", 
    "database": "astero"
}

# Here I have established the connection to the sql
connection = db.connect(**DB_CONFIG)
st.sidebar.success("✅ DB Connected") 

# these are all the key performance indicators which you can see in the demo
kpi_cursor = connection.cursor(dictionary=True) 

kpi_cursor.execute("SELECT COUNT(DISTINCT id) as total FROM asteroids")
total_asteroids = kpi_cursor.fetchone()['total']

kpi_cursor.execute("SELECT COUNT(DISTINCT id) as hazardous FROM asteroids WHERE is_potentially_hazardous_asteroid = TRUE")
hazardous_count = kpi_cursor.fetchone()['hazardous']

kpi_cursor.execute("SELECT MAX(relative_velocity_kmph) as fastest FROM close_approach WHERE relative_velocity_kmph IS NOT NULL")
fastest_speed_result = kpi_cursor.fetchone()
fastest_speed = fastest_speed_result['fastest'] if fastest_speed_result else 0.0 

kpi_cursor.close() 

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric(label="Total Unique NEOs Recorded", value=f"{total_asteroids:,}")
kpi_col2.metric(label="Potentially Hazardous NEOs", value=f"{hazardous_count:,}")
kpi_col3.metric(label="Highest Recorded Speed (km/h)", value=f"{fastest_speed:,.0f}")

# here comes the SQL Queries 
QUERIES = {
    "Select a Query...": "",

    "📊 1. Count Approaches per Asteroid": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, COUNT(c.neo_reference_id) AS Approach_Count
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id
        GROUP BY c.neo_reference_id, a.name ORDER BY Approach_Count DESC LIMIT 100;
    """,
    "💨 2. Average Velocity per Asteroid": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, AVG(c.relative_velocity_kmph) AS Average_Velocity_Kmph
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id
        GROUP BY c.neo_reference_id, a.name ORDER BY Average_Velocity_Kmph DESC LIMIT 100;
    """,
    "⚡ 3. Top 10 Fastest Asteroids (by Max Velocity)": """
       SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, MAX(c.relative_velocity_kmph) AS Max_Velocity_Kmph
       FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.relative_velocity_kmph IS NOT NULL
       GROUP BY c.neo_reference_id, a.name ORDER BY Max_Velocity_Kmph DESC LIMIT 10;
    """,
    "⚠️ 4. Hazardous Asteroids Approaching > 3 Times": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, COUNT(c.neo_reference_id) AS Approach_Count
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id WHERE a.is_potentially_hazardous_asteroid = TRUE
        GROUP BY c.neo_reference_id, a.name HAVING COUNT(c.neo_reference_id) > 3 ORDER BY Approach_Count DESC;
    """,
    "📅 5. Busiest Month for Approaches": """
        SELECT MONTHNAME(close_approach_date) AS Month, COUNT(*) AS Approach_Count
        FROM close_approach WHERE close_approach_date IS NOT NULL GROUP BY Month ORDER BY Approach_Count DESC LIMIT 1;
    """,
    "🏆 6. Single Fastest Approach Recorded": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.relative_velocity_kmph AS Max_Velocity_Kmph, c.close_approach_date
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.relative_velocity_kmph IS NOT NULL
        ORDER BY c.relative_velocity_kmph DESC LIMIT 1;
    """,
    "📏 7. Largest Asteroids (by Max Diameter)": """
        SELECT name AS Asteroid_Name, id AS Asteroid_ID, estimated_diameter_max_km AS Max_Diameter_KM
        FROM asteroids WHERE estimated_diameter_max_km IS NOT NULL ORDER BY Max_Diameter_KM DESC LIMIT 50;
    """,
    "🛰️ 8. Closest Approaches Overall (km)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.miss_distance_km AS Miss_Distance_KM
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.miss_distance_km IS NOT NULL
        ORDER BY c.miss_distance_km ASC, c.close_approach_date ASC LIMIT 50;
    """,
     "🛰️ 9. Closest Approach Details (Name, Date, Distance)": """
        SELECT a.name AS Asteroid_Name, c.close_approach_date AS Closest_Approach_Date, c.miss_distance_km AS Miss_Distance_KM
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.miss_distance_km IS NOT NULL
        ORDER BY c.miss_distance_km ASC LIMIT 50;
    """,
    "💨 10. Approaches Faster than 50,000 km/h": """
        SELECT DISTINCT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, MAX(c.relative_velocity_kmph) AS Max_Velocity_Kmph
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.relative_velocity_kmph > 50000
        GROUP BY a.name, c.neo_reference_id ORDER BY Max_Velocity_Kmph DESC LIMIT 100;
    """,
    "📈 11. Approach Count per Month/Year": """
        SELECT YEAR(close_approach_date) AS Year, MONTHNAME(close_approach_date) AS Month, COUNT(*) AS Approach_Count
        FROM close_approach WHERE close_approach_date IS NOT NULL
        GROUP BY Year, Month ORDER BY Year, MONTH(close_approach_date);
    """,
    "☀️ 12. Brightest Asteroid (Lowest Magnitude)": """
        SELECT name AS Asteroid_Name, id AS Asteroid_ID, absolute_magnitude_h AS Absolute_Magnitude
        FROM asteroids WHERE absolute_magnitude_h IS NOT NULL ORDER BY absolute_magnitude_h ASC LIMIT 1;
    """,
    "📊 13. Hazardous vs Non-Hazardous Count": """
        SELECT CASE WHEN is_potentially_hazardous_asteroid = TRUE THEN 'Hazardous' WHEN is_potentially_hazardous_asteroid = FALSE THEN 'Non-Hazardous' ELSE 'Unknown/Null' END AS Hazard_Status,
               COUNT(DISTINCT id) AS Unique_Asteroid_Count
        FROM asteroids GROUP BY Hazard_Status;
    """,
    "🌙 14. Closer Than The Moon (< 1 LD)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.miss_distance_lunar AS Miss_Distance_Lunar
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.miss_distance_lunar < 1
        ORDER BY c.miss_distance_lunar ASC LIMIT 50;
    """,
    "🤏 15. Very Close Approaches (< 0.05 AU)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.astronomical_au AS Miss_Distance_AU
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id WHERE c.astronomical_au < 0.05
        ORDER BY c.astronomical_au ASC LIMIT 50;
    """,
    # Extra queries
    "🥇 16. Closest Approach per Asteroid (km)": """
        SELECT name, neo_reference_id, close_approach_date, miss_distance_km
        FROM (
            SELECT a.name, c.neo_reference_id, c.close_approach_date, c.miss_distance_km,
                   ROW_NUMBER() OVER(PARTITION BY c.neo_reference_id ORDER BY c.miss_distance_km ASC) as rn
            FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
            WHERE c.miss_distance_km IS NOT NULL
        ) ranked_approaches
        WHERE rn = 1 ORDER BY miss_distance_km ASC LIMIT 100;
    """,
    "🐢 17. Slowest Average Velocity Asteroids": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, AVG(c.relative_velocity_kmph) AS Average_Velocity_Kmph
        FROM close_approach c LEFT JOIN asteroids a ON c.neo_reference_id = a.id
        WHERE c.relative_velocity_kmph IS NOT NULL
        GROUP BY c.neo_reference_id, a.name ORDER BY Average_Velocity_Kmph ASC LIMIT 10;
    """,
    "⚠️ 18. Closest Hazardous Asteroid Approach (km)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.miss_distance_km AS Miss_Distance_KM
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = TRUE AND c.miss_distance_km IS NOT NULL
        ORDER BY c.miss_distance_km ASC LIMIT 1;
    """,
     "⚠️ 19. Fastest Hazardous Asteroid Approach (km/h)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.relative_velocity_kmph AS Max_Velocity_Kmph, c.close_approach_date
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = TRUE AND c.relative_velocity_kmph IS NOT NULL
        ORDER BY c.relative_velocity_kmph DESC LIMIT 1;
    """,
    "📉 20. Size Distribution (Max Diameter Bins)": """
        SELECT CASE
            WHEN estimated_diameter_max_km < 0.1 THEN '< 0.1 km'
            WHEN estimated_diameter_max_km < 0.5 THEN '0.1-0.5 km'
            WHEN estimated_diameter_max_km < 1.0 THEN '0.5-1.0 km'
            WHEN estimated_diameter_max_km < 5.0 THEN '1.0-5.0 km'
            ELSE '>= 5.0 km'
        END AS Size_Bin, COUNT(DISTINCT id) AS Unique_Asteroid_Count
        FROM asteroids WHERE estimated_diameter_max_km IS NOT NULL
        GROUP BY Size_Bin ORDER BY MIN(estimated_diameter_max_km);
    """,
    "💨 21. Velocity Distribution (Bins km/h)": """
        SELECT CASE
            WHEN relative_velocity_kmph < 20000 THEN '< 20k'
            WHEN relative_velocity_kmph < 40000 THEN '20k-40k'
            WHEN relative_velocity_kmph < 60000 THEN '40k-60k'
            WHEN relative_velocity_kmph < 80000 THEN '60k-80k'
            WHEN relative_velocity_kmph < 100000 THEN '80k-100k'
            ELSE '>= 100k'
        END AS Velocity_Bin_Kmph, COUNT(*) AS Approach_Count
        FROM close_approach WHERE relative_velocity_kmph IS NOT NULL
        GROUP BY Velocity_Bin_Kmph ORDER BY MIN(relative_velocity_kmph);
    """,
    "📅 22. Approaches per Year": """
        SELECT YEAR(close_approach_date) AS Year, COUNT(*) AS Approach_Count
        FROM close_approach WHERE close_approach_date IS NOT NULL
        GROUP BY Year ORDER BY Year;
    """,
    "☀️ 23. Magnitude Distribution (Bins)": """
        SELECT CASE
            WHEN absolute_magnitude_h < 15 THEN '< 15 (Very Bright)'
            WHEN absolute_magnitude_h < 20 THEN '15-20 (Bright)'
            WHEN absolute_magnitude_h < 25 THEN '20-25 (Moderate)'
            WHEN absolute_magnitude_h < 30 THEN '25-30 (Dim)'
            ELSE '>= 30 (Very Dim)'
        END AS Magnitude_Bin, COUNT(DISTINCT id) AS Unique_Asteroid_Count
        FROM asteroids WHERE absolute_magnitude_h IS NOT NULL
        GROUP BY Magnitude_Bin ORDER BY MIN(absolute_magnitude_h);
    """,
    "❓ 24. Asteroids with Only One Recorded Approach": """
        SELECT a.name, c.neo_reference_id, COUNT(*) as approach_count
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
        GROUP BY c.neo_reference_id, a.name HAVING approach_count = 1
        LIMIT 100;
    """,
    "🪐 25. Most Frequent Orbiting Body (Besides Earth)": """
        SELECT orbiting_body, COUNT(*) AS Count
        FROM close_approach
        WHERE orbiting_body != 'Earth' AND orbiting_body IS NOT NULL
        GROUP BY orbiting_body ORDER BY Count DESC;
    """,
    "📏 26. Smallest Asteroids (by Min Diameter)": """
        SELECT name AS Asteroid_Name, id AS Asteroid_ID, estimated_diameter_min_km AS Min_Diameter_KM
        FROM asteroids WHERE estimated_diameter_min_km IS NOT NULL
        ORDER BY Min_Diameter_KM ASC LIMIT 50;
    """,
    "🤏 27. Extremely Close Approaches (< 0.01 AU)": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.astronomical_au AS Miss_Distance_AU
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
        WHERE c.astronomical_au < 0.01 ORDER BY c.astronomical_au ASC LIMIT 50;
    """,
     "⚠️ 28. Hazardous Approaches Within 0.1 AU": """
        SELECT a.name AS Asteroid_Name, c.neo_reference_id AS Asteroid_ID, c.close_approach_date AS Approach_Date, c.astronomical_au AS Miss_Distance_AU
        FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = TRUE AND c.astronomical_au < 0.1
        ORDER BY c.astronomical_au ASC LIMIT 50;
    """,
    "📅 29. Approaches by Day of Week": """
        SELECT DAYNAME(close_approach_date) AS DayOfWeek, COUNT(*) AS Approach_Count
        FROM close_approach WHERE close_approach_date IS NOT NULL
        GROUP BY DayOfWeek ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    """,
    "🛰️ 30. Furthest Approach per Asteroid (km)": """
        SELECT name, neo_reference_id, close_approach_date, miss_distance_km
        FROM (
            SELECT a.name, c.neo_reference_id, c.close_approach_date, c.miss_distance_km,
                   ROW_NUMBER() OVER(PARTITION BY c.neo_reference_id ORDER BY c.miss_distance_km DESC) as rn
            FROM close_approach c JOIN asteroids a ON c.neo_reference_id = a.id
            WHERE c.miss_distance_km IS NOT NULL
        ) ranked_approaches
        WHERE rn = 1 ORDER BY miss_distance_km DESC LIMIT 100;
    """
}

# Here i have defined the sidebar
st.sidebar.title("📋 Predefined Queries")
st.sidebar.markdown("Select a query:")
selected_query_name = st.sidebar.selectbox(
    "Select Query:",
    options=list(QUERIES.keys()),
    index=0,
    label_visibility="collapsed" 
)

#Predefined Query Display
if selected_query_name != "Select a Query...":
    st.subheader(f"🔎 {selected_query_name}") 
    query_sql = QUERIES[selected_query_name]
    if query_sql:
        # this will show Streamlit error page if fails
        df = pd.read_sql(query_sql, connection)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"Success! Found {len(df)} rows.")


            if "11. Approach Count per Month/Year" in selected_query_name:
                st.subheader("📈 Approaches Over Time")
                df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B', errors='coerce') # Coerce errors
                df_chart = df.dropna(subset=['Date']).set_index('Date') # Drop rows where date conversion failed
                if not df_chart.empty:
                    st.line_chart(df_chart['Approach_Count'])
            elif "13. Hazardous vs Non-Hazardous Count" in selected_query_name:
                st.subheader("📊 Hazard Status Distribution")
                st.bar_chart(df.set_index('Hazard_Status')['Unique_Asteroid_Count'])
            elif "20. Size Distribution" in selected_query_name:
                 st.subheader("📊 Size Distribution (Max Diameter)")
                 st.bar_chart(df.set_index('Size_Bin')['Unique_Asteroid_Count'])
            elif "21. Velocity Distribution" in selected_query_name:
                 st.subheader("📊 Velocity Distribution")
                 st.bar_chart(df.set_index('Velocity_Bin_Kmph')['Approach_Count'])
            elif "22. Approaches per Year" in selected_query_name:
                st.subheader("📈 Approaches per Year")
                st.bar_chart(df.set_index('Year')['Approach_Count'])
            elif "23. Magnitude Distribution" in selected_query_name:
                 st.subheader("📊 Absolute Magnitude Distribution")
                 st.bar_chart(df.set_index('Magnitude_Bin')['Unique_Asteroid_Count'])
            elif "29. Approaches by Day of Week" in selected_query_name:
                 st.subheader("📅 Approaches by Day of Week")
                 st.bar_chart(df.set_index('DayOfWeek')['Approach_Count'])
        else:
            st.info("Query executed, but no matching data found.")

st.divider()

# Filtering section starts here
st.header("🔍 Interactive NEO Data Explorer")
st.markdown("Adjust the filters and click the button below.")

# the widgets for the filtering section starts here
col1, col2 = st.columns(2)
with col1:
    default_start_date = datetime.now().date() - timedelta(days=730)
    default_end_date = datetime.now().date()
    sel_start_date = st.date_input("📅 Start Date", value=default_start_date)
    sel_end_date = st.date_input("📅 End Date", value=default_end_date, min_value=sel_start_date)
    sel_vel_range = st.slider("💨 Velocity (km/h)", 0.0, 300000.0, (0.0, 150000.0), 1000.0) 
    sel_diam_min_range = st.slider("📏 Min Diameter (km)", 0.0, 10.0, (0.0, 1.0), 0.01) 
    sel_diam_max_range = st.slider("📏 Max Diameter (km)", 0.0, 20.0, (0.0, 5.0), 0.1) 
with col2:
    sel_au_range = st.slider("🛰️ Miss Distance (AU)", 0.0, 1.0, (0.0, 0.2), 0.001) 
    sel_ld_range = st.slider("🌙 Miss Distance (Lunar)", 0.0, 100.0, (0.0, 25.0)) 
    sel_hazardous_option = st.selectbox("⚠️ Hazardous Status", ["All", "Hazardous Only", "Non-Hazardous Only"])

# The filter button named apply
if st.button("📊 Show Filtered Data", type="primary"):
    # construction of filtered query
    filter_query_base = """
        SELECT
            a.id AS ID, a.name AS Name,
            a.is_potentially_hazardous_asteroid AS Hazardous,
            a.estimated_diameter_min_km AS MinDiamKM, a.estimated_diameter_max_km AS MaxDiamKM,
            c.close_approach_date AS Date, c.relative_velocity_kmph AS VelocityKMH,
            c.astronomical_au AS MissAU, c.miss_distance_lunar AS MissLD,
            c.miss_distance_km AS MissKM, c.orbiting_body AS Orbiting
        FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE c.close_approach_date BETWEEN %s AND %s
          AND c.relative_velocity_kmph BETWEEN %s AND %s
          AND a.estimated_diameter_min_km BETWEEN %s AND %s
          AND a.estimated_diameter_max_km BETWEEN %s AND %s
          AND c.astronomical_au BETWEEN %s AND %s
          AND c.miss_distance_lunar BETWEEN %s AND %s
    """
    filter_params = [
        sel_start_date, sel_end_date,
        float(sel_vel_range[0]), float(sel_vel_range[1]),
        float(sel_diam_min_range[0]), float(sel_diam_min_range[1]),
        float(sel_diam_max_range[0]), float(sel_diam_max_range[1]),
        float(sel_au_range[0]), float(sel_au_range[1]),
        float(sel_ld_range[0]), float(sel_ld_range[1])
    ]

    if sel_hazardous_option == "Hazardous Only":
        filter_query_base += " AND a.is_potentially_hazardous_asteroid = TRUE"
    elif sel_hazardous_option == "Non-Hazardous Only":
         filter_query_base += " AND a.is_potentially_hazardous_asteroid = FALSE"

    filter_query_base += " ORDER BY c.close_approach_date ASC LIMIT 500;"

    st.subheader("Filtered Approach Data Results")
    filtered_df = pd.read_sql(filter_query_base, connection, params=tuple(filter_params))

    if not filtered_df.empty:
        filtered_df['Hazardous'] = filtered_df['Hazardous'].map({1: 'Yes', 0: 'No'}).fillna('Unknown')
        filtered_df['MinDiamKM'] = filtered_df['MinDiamKM'].map('{:.4f}'.format)
        filtered_df['MaxDiamKM'] = filtered_df['MaxDiamKM'].map('{:.4f}'.format)
        filtered_df['VelocityKMH'] = filtered_df['VelocityKMH'].map('{:,.2f}'.format)
        filtered_df['MissAU'] = filtered_df['MissAU'].map('{:.4f}'.format)
        filtered_df['MissLD'] = filtered_df['MissLD'].map('{:.2f}'.format)
        filtered_df['MissKM'] = filtered_df['MissKM'].map('{:,.0f}'.format)

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        st.caption(f"Showing up to 500 results.")
    else:
        st.info("🤷 No data found matching the selected filters.")
