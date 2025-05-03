# ☄️ NASA NEO Insights Dashboard

This project retrieves Near-Earth Object (NEO) data from NASA's public API, stores it in a MySQL database, and presents insights through an interactive web application built with Streamlit.

## ✨ Features

*   **Database Integration:** Fetches data from the NASA NeoWs API and stores it in a structured MySQL database (Note: Data fetching/storage might be in a separate script/notebook).
*   **Key Metrics:** Displays key statistics like the total number of unique NEOs recorded, the count of potentially hazardous ones, and the highest approach speed observed.
*   **Predefined Queries:** Offers a sidebar dropdown with 30+ pre-built SQL queries to explore common questions about the NEO data (e.g., counts, fastest/largest objects, close approaches).
*   **Interactive Filtering:** Allows users to dynamically filter the close approach data based on:
    *   📅 Approach Date Range
    *   💨 Relative Velocity (km/h)
    *   📏 Estimated Diameter (Min & Max in km)
    *   🛰️ Miss Distance (Astronomical Units - AU)
    *   🌙 Miss Distance (Lunar Distances - LD)
    *   ⚠️ Hazardous Status (All, Hazardous Only, Non-Hazardous Only)
*   **Data Visualization:**
    *   Presents query results and filtered data in clear, sortable tables.
    *   Includes basic charts (bar/line) for specific predefined queries (like monthly counts or size distributions).

## 🛠️ Technologies Used

*   **Python:** Core programming language.
*   **Streamlit:** For building the interactive web application.
*   **Pandas:** For data manipulation and handling query results.
*   **MySQL Connector Python:** For connecting Python to the MySQL database.
*   **MySQL:** Relational database used for storing NEO data.
*   **NASA NeoWs API:** The source of the Near-Earth Object data.

## 📋 Prerequisites

*   **Python:** Version 3.8 or higher recommended.
*   **MySQL Server:** Must be installed and running.
*   **pip:** Python package installer (usually comes with Python).
*   **NASA API Key:** You need a free API key from [https://api.nasa.gov/](https://api.nasa.gov/).

## 🚀 Setup & Installation

1.  **Clone Repository (Optional):** If you have this project in a Git repository, clone it:
    ```bash
    git clone https://github.com/Obs25/Project-1-NASA-Near-Earth-Object-NEO-Tracking-Insights-using-Public-API.git
    ```
    Otherwise, just make sure you have the project files in a local directory.

2.  **Install Python Packages:**
    ```bash
    pip install streamlit pandas mysql-connector-python
    ```

3.  **Set up MySQL Database:**
    *   Connect to your MySQL server.
    *   Create the database: `CREATE DATABASE astero;`
    *   Use the database: `USE astero;`
    *   Create the `asteroids` and `close_approach` tables using the SQL `CREATE TABLE` statements provided in the project documentation or relevant script/notebook.

4.  **Configure Database Credentials:**
    *   Open the main Streamlit Python script (e.g., `nasa_neo_app_basic.py`).
    *   Find the `DB_CONFIG` dictionary near the top.
    *   **Crucially, replace `"YOUR_MYSQL_PASSWORD"` with your actual MySQL password.** Verify the host, user, and database name are correct.

5.  **Populate Database:**
    *   Run the separate Python script or Jupyter Notebook responsible for fetching data from the NASA API and inserting it into the `asteroids` and `close_approach` tables in your MySQL database. **This step must be completed before running the Streamlit app.**

## ▶️ How to Run the Application

1.  **Navigate to Directory:** Open your terminal or command prompt and change to the directory where you saved the Streamlit Python script (e.g., `demo1.py`).

2.  **Run Streamlit:**
    ```bash
    streamlit run demo1.py
    ```
    *   *(Optional)* If the browser doesn't open automatically or you see a `FileNotFoundError: [Errno 2] No such file or directory: 'open'` in the terminal, use:
        ```bash
        streamlit demo1.py --server.headless true
        ```
        Then manually open your web browser and go to the "Network URL" provided in the terminal (usually `http://localhost:8501`).

3.  **Interact:** Explore the predefined queries in the sidebar and use the filters on the main page to analyze the NEO data!

## 📊 Data Source

*   All Near-Earth Object data is sourced from the **NASA NeoWs (Near Earth Object Web Service) API**.
*   API Homepage: [https://api.nasa.gov/](https://api.nasa.gov/)

---

*Enjoy exploring the cosmos!* 🌌
