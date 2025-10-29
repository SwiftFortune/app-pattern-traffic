import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set Streamlit page config
st.set_page_config(page_title="App Ads Traffic IVT Analysis", layout="wide")

# === File Paths ===
folder = r"C:\sachin\Python\Daily Project\App_Ads_Analysis"
total_path = os.path.join(folder, "combined_total_data.csv")
daily_path = os.path.join(folder, "combined_daily_data.csv")
hourly_path = os.path.join(folder, "combined_hourly_data.csv")

# === Load Data ===
@st.cache_data
def load_data():
    Total_data = pd.read_csv(total_path)
    daily_data = pd.read_csv(daily_path)
    hourly_data = pd.read_csv(hourly_path)

    # Label each app as IVT or Non-IVT
    ivt_map = {'valid': 'Non-IVT', 'invalid': 'IVT'}
    for df in [Total_data, daily_data, hourly_data]:
        df['ivt_status'] = df['app'].map(ivt_map)
    return Total_data, daily_data, hourly_data

Total_data, daily_data, hourly_data = load_data()

# === Sidebar Navigation ===
st.sidebar.title("📊 IVT Traffic Analysis")
page = st.sidebar.radio("Select Section:", 
                        ["Overview", "Total Analysis", "Daily Trends", "Hourly Behavior", 
                         "Traffic Ratio & Volatility", "Correlation Analysis", "Summary Insights"])

# === Page 1: Overview ===
if page == "Overview":
    st.title("📈 App Traffic Analysis: IVT vs Non-IVT")
    st.markdown("""
    This dashboard analyzes traffic behavior across multiple apps to understand **why some were flagged as IVT (Invalid Traffic) earlier** than others.
    The analysis covers:
    - Total traffic and unique identifiers
    - Daily and hourly activity trends
    - Ratio and volatility patterns
    - Correlation differences
    """)
    st.info("Use the sidebar to explore each analysis section interactively.")

# === Page 2: Total Analysis ===
elif page == "Total Analysis":
    st.header("🔍 Total Traffic Analysis (IVT vs Non-IVT)")
    total_summary = Total_data.groupby(['app', 'ivt_status'])[['unique_idfas', 'unique_ips']].sum().reset_index()

    # --- Plot 1 ---
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=total_summary, x='app', y='unique_idfas', hue='ivt_status', ax=ax)
    ax.set_title("Total Unique IDFAs by App (IVT vs Non-IVT)")
    st.pyplot(fig)

    # --- Plot 2 ---
    fig2 = sns.lmplot(data=total_summary, x='unique_idfas', y='unique_ips', hue='ivt_status', height=5, aspect=1.3)
    plt.title("Correlation of Unique IPs vs IDFAs (Total Level)")
    st.pyplot(fig2.fig)

# === Page 3: Daily Trends ===
elif page == "Daily Trends":
    st.header("📆 Daily Traffic Trends")
    daily_data['date'] = pd.to_datetime(daily_data['date'], errors='coerce')

    # Total Requests
    daily_trend = daily_data.groupby(['date', 'ivt_status'])['total_requests'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=daily_trend, x='date', y='total_requests', hue='ivt_status', marker='o', ax=ax)
    ax.set_title('Daily Total Requests Trend (IVT vs Non-IVT)')
    st.pyplot(fig)

    # Unique IDFAs
    idfa_trend = daily_data.groupby(['date', 'ivt_status'])['unique_idfas'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=idfa_trend, x='date', y='unique_idfas', hue='ivt_status', marker='o', ax=ax2)
    ax2.set_title('Daily Unique IDFAs Trend (IVT vs Non-IVT)')
    st.pyplot(fig2)

# === Page 4: Hourly Behavior ===
elif page == "Hourly Behavior":
    st.header("⏰ Hourly Traffic Behavior")
    hourly_data['date'] = pd.to_datetime(hourly_data['date'], errors='coerce')
    hourly_data['hour'] = hourly_data['date'].dt.hour

    hourly_trend = hourly_data.groupby(['hour', 'ivt_status'])['total_requests'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_trend, x='hour', y='total_requests', hue='ivt_status', marker='o', linewidth=2.5, ax=ax)
    ax.set_title('Hourly Total Requests (IVT vs Non-IVT)')
    st.pyplot(fig)

    hourly_avg = hourly_data.groupby(['hour', 'ivt_status'])['total_requests'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_avg, x='hour', y='total_requests', hue='ivt_status', marker='o', ax=ax2)
    ax2.set_title('Average Hourly Requests (IVT vs Non-IVT)')
    st.pyplot(fig2)

# === Page 5: Traffic Ratio & Volatility ===
elif page == "Traffic Ratio & Volatility":
    st.header("📊 Traffic Ratio & Volatility")

    # Ratio
    ratio_summary = Total_data.groupby('ivt_status')[['idfa_ip_ratio', 'idfa_ua_ratio']].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=ratio_summary.melt(id_vars='ivt_status'), x='ivt_status', y='value', hue='variable', ax=ax)
    ax.set_title('Average Traffic Ratios (IDFA–IP / IDFA–UA)')
    st.pyplot(fig)

    # Variability
    metrics = ['unique_idfas', 'unique_ips', 'total_requests', 'requests_per_idfa', 'impressions']
    variability = Total_data.groupby('ivt_status')[metrics].std().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=variability.melt(id_vars='ivt_status'), x='ivt_status', y='value', hue='variable', ax=ax2)
    ax2.set_title('Volatility of Key Traffic Metrics (IVT vs Non-IVT)')
    st.pyplot(fig2)

# === Page 6: Correlation Analysis ===
elif page == "Correlation Analysis":
    st.header("🔗 Correlation Differences (IVT vs Non-IVT)")
    num_cols = ['unique_idfas', 'unique_ips', 'unique_uas', 'total_requests',
                'requests_per_idfa', 'impressions', 'impressions_per_idfa',
                'idfa_ip_ratio', 'idfa_ua_ratio']

    ivt_df = Total_data[Total_data['ivt_status'] == 'IVT'][num_cols]
    non_ivt_df = Total_data[Total_data['ivt_status'] == 'Non-IVT'][num_cols]

    corr_ivt = ivt_df.corr()
    corr_non_ivt = non_ivt_df.corr()
    corr_diff = corr_ivt - corr_non_ivt

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("IVT Correlation Matrix")
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(corr_ivt, annot=True, cmap='Reds', vmin=-1, vmax=1, ax=ax)
        st.pyplot(fig)
    with col2:
        st.subheader("Non-IVT Correlation Matrix")
        fig2, ax2 = plt.subplots(figsize=(7, 6))
        sns.heatmap(corr_non_ivt, annot=True, cmap='Blues', vmin=-1, vmax=1, ax=ax2)
        st.pyplot(fig2)

    st.subheader("Difference Heatmap (IVT - Non-IVT)")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_diff, annot=True, cmap='coolwarm', center=0, ax=ax3)
    st.pyplot(fig3)

# === Page 7: Summary Insights ===
elif page == "Summary Insights":
    st.header("🧠 Why Some Apps Were Marked IVT Earlier Than Others")
    st.markdown("""
    - **Traffic Pattern:** IVT apps showed abnormally high counts of unique IDFAs and IPs, indicating synthetic traffic where fake devices connect through many IPs.  
    - **Temporal Activity:** IVT apps displayed sharp, inconsistent spikes in hourly and daily requests. Non-IVT apps maintained steady, organic activity.  
    - **Volatility:** Metrics like requests, impressions, and IDFAs had very high fluctuations in IVT apps.  
    - **Correlation Behavior:** IVT traffic metrics were artificially correlated (impressions, requests, IDFAs move together), unlike real user traffic.  
      
    **✅ Conclusion:**  
    IVT apps were flagged earlier because of their inflated ratios, unstable activity, and mechanical correlations, while Non-IVT apps remained consistent, suggesting genuine engagement.
    """)
