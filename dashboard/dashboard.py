import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Load dataset
df = pd.read_csv("all_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

# Helper function untuk filter data berdasarkan tanggal
def filter_data(df, start_date, end_date):
    return df[(df["dteday"] >= pd.Timestamp(start_date)) & (df["dteday"] <= pd.Timestamp(end_date))]

# Helper function untuk agregasi data harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.groupby("dteday")["cnt"].sum().reset_index()
    return daily_rentals_df

# Sidebar - Filter Data
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df["dteday"].min())
end_date = st.sidebar.date_input("End Date", df["dteday"].max())

df_filtered = filter_data(df, start_date, end_date)
daily_rentals_df = create_daily_rentals_df(df_filtered)

# Konten utama
st.title("\U0001F4CA Dashboard Peminjaman Sepeda")

st.write("### \U0001F50D Data yang Ditampilkan")
st.dataframe(df_filtered)

# Metric Summary
col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df["cnt"].sum()
    st.metric("\U0001F4C8 Total Peminjaman", value=total_rentals)

with col2:
    avg_rentals = round(daily_rentals_df["cnt"].mean(), 2)
    st.metric("\U0001F4CA Rata-rata Peminjaman per Hari", value=avg_rentals)

# Visualisasi Tren Peminjaman
st.write("### \U0001F4C5 Grafik Tren Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_rentals_df["dteday"], daily_rentals_df["cnt"], marker='o', linestyle='-', color='#007acc', linewidth=2)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
ax.set_title("Tren Peminjaman Sepeda", fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# Analisis Penyewaan Sepeda Berdasarkan Hari Kerja vs Akhir Pekan
st.write("### \U0001F6B4 Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
df_filtered["is_weekend"] = df_filtered["weekday"].isin(["Saturday", "Sunday"])

weekend_rentals = df_filtered[df_filtered["is_weekend"]]["cnt"].sum()
weekday_rentals = df_filtered[~df_filtered["is_weekend"]]["cnt"].sum()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=["Hari Kerja", "Akhir Pekan"], y=[weekday_rentals, weekend_rentals], palette=["blue", "orange"], ax=ax)
ax.set_ylabel("Total Penyewaan")
ax.set_title("Perbandingan Penyewaan Sepeda")
st.pyplot(fig)

# Analisis Penyewaan Sepeda Berdasarkan Musim
st.write("### 🌦 Penyewaan Sepeda Berdasarkan Musim")

if 'season' in df_filtered.columns:
    season_summary = df_filtered.groupby("season").agg(
        Total_Penyewaan=("cnt", "sum"),
        Rata_rata=("cnt", "mean"),
        Min_Penyewaan=("cnt", "min"),
        Max_Penyewaan=("cnt", "max")
    ).reset_index()

    # Tabel dengan warna gradien
    st.write("📊 **Ringkasan Penyewaan per Musim**")
    st.dataframe(season_summary.style.background_gradient(cmap="Blues", subset=["Total_Penyewaan", "Rata_rata"]))

    # Visualisasi Data
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x="season", y="Total_Penyewaan", data=season_summary, palette="coolwarm", ax=ax)
    ax.set_title("Total Penyewaan Sepeda per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

st.write("### \U0001F3AF Kesimpulan:")
st.markdown("""
- **Penyewaan lebih tinggi di hari kerja dibandingkan akhir pekan.**
- **Musim gugur dan musim panas memiliki penyewaan tertinggi, sementara musim dingin cenderung sedikit lebih rendah.**
- **Penyewaan terendah berada pada musim semi.**
- **Cuaca mempengaruhi jumlah penyewaan tidak secara signifikan.**
""")

st.success("Dashboard ini membantu memahami pola penyewaan sepeda untuk optimasi bisnis.")
