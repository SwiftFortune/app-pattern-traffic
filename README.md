# 🧠 App Ads IVT Analysis — Detecting Invalid Traffic Behavior

This project investigates traffic data across multiple mobile apps to understand **why some apps were marked as IVT (Invalid Traffic)** earlier, while others remained **Non-IVT (Valid)**.  
Through data cleaning, aggregation, and analysis at **total**, **daily**, and **hourly** levels, this study identifies behavioral and statistical differences between the two groups.

---

## 📂 Project Overview

We analyzed **six apps**:
- **3 Valid (Non-IVT)** apps  
- **3 Invalid (IVT)** apps, flagged at different points in time  

Each app provided:
- **Total data**
- **Daily data**
- **Hourly data**

The goal is to **analyze traffic patterns**, detect anomalies, and uncover key metrics that signal invalid traffic.

---

## 🧹 Data Preparation

1. All CSV files were combined automatically using Python’s `glob` and `pandas`.
2. Each record was tagged with:
   - App name (`Valid-1`, `Invalid-3`, etc.)
   - IVT status (`IVT` or `Non-IVT`)
3. Missing and empty rows/columns were cleaned before merging.

Generated combined datasets:
- `combined_total_data.csv`
- `combined_daily_data.csv`
- `combined_hourly_data.csv`

---

## 🧭 Key Analyses

### 1. Traffic Volume Comparison
- Compared **unique IDFAs**, **unique IPs**, and **total requests**.
- IVT apps showed **unusually high volumes** across all metrics.

### 2. Behavioral Ratios
- Computed ratios such as:
  - `idfa_ip_ratio` → multiple IPs per device
  - `idfa_ua_ratio` → multiple user agents per device
- IVT apps displayed **inflated ratios**, suggesting **bot or emulator activity**.

### 3. Temporal Patterns
- **Daily Trends:** IVT apps showed sharp spikes and irregular traffic.
- **Hourly Trends:** IVT apps had concentrated traffic bursts at specific hours.
- Non-IVT apps exhibited **smooth, organic activity patterns**.

### 4. Volatility & Correlation
- IVT apps had **higher standard deviation** across metrics like requests and impressions.
- Correlation matrices revealed **mechanical dependencies** among IVT metrics.
- Non-IVT apps displayed **natural, loosely correlated behavior**.

### 5. Correlation Difference Heatmaps
- Compared feature correlations between IVT and Non-IVT groups.
- Highlighted distinct interaction patterns — a key indicator of artificial traffic.

---

## 📊 Visualizations

| Visualization | Description |
|----------------|-------------|
| Barplots | Total Unique IDFAs & IPs (IVT vs Non-IVT) |
| Lineplots | Daily & Hourly traffic trends |
| Boxplots | Requests & Impressions per IDFA |
| Heatmaps | Correlation and difference between IVT and Non-IVT metrics |
| Ratio Analysis | Average IDFA–IP and IDFA–UA ratios |

All visualizations are generated using **Seaborn** and **Matplotlib**.

---

## 🔍 Insights Summary

| Aspect | IVT Apps | Non-IVT Apps |
|--------|-----------|---------------|
| **Traffic Volume** | Abnormally high | Consistent and realistic |
| **Temporal Pattern** | Irregular spikes | Smooth daily/hourly flow |
| **Volatility** | Very high | Stable |
| **Ratios** | Inflated IDFA–IP / UA | Balanced |
| **Correlations** | Mechanically strong | Natural |

### 🧩 Conclusion
IVT apps were flagged earlier because of:
- Inflated **traffic ratios**
- **Erratic and unstable** activity
- **High volatility** in metrics
- **Strong artificial correlations**

In contrast, Non-IVT apps demonstrated **steady, user-driven** engagement patterns.

---

## ⚙️ Tech Stack

- **Python Libraries:**
  - `pandas`, `numpy`
  - `seaborn`, `matplotlib`
  - `glob`, `os`
- **Data Processing:** CSV-based, multi-level aggregation
- **Visualization:** Interactive and comparative plots

---

## 📁 Outputs

- `combined_total_data.csv`
- `combined_daily_data.csv`
- `combined_hourly_data.csv`
- Analytical visualizations (barplots, lineplots, boxplots, heatmaps)

---

## 🧠 Key Takeaway

This project demonstrates how **data analytics and visualization** can effectively reveal **fraudulent traffic behavior** by studying traffic volume, volatility, and correlation patterns over time.


**Sachin Hembram**  
Data Analyst | Machine Learning Enthusiast  
📧 *sachincmf@gmail.com* 

