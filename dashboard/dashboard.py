import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (pastikan file CSV telah dibersihkan)
@st.cache_data
def load_data():
    return pd.read_csv("main_data.csv")  # Ganti dengan path file yang benar

day_df_clean = load_data()

# Sidebar navigasi
st.sidebar.title("🚴 Dashboard Penyewaan Sepeda")
page = st.sidebar.radio("Pilih Analisis", [
    "📊 Statistik Deskriptif",
    "📉 Distribusi Penyewaan",
    "📅 Perbandingan Hari Kerja vs Akhir Pekan",
    "🌦️ Tren Penyewaan Sepeda per Musim",
    "📈 Korelasi Cuaca & Penyewaan"
])

# 1. Statistik Deskriptif
if page == "📊 Statistik Deskriptif":
    st.title("📊 Statistik Deskriptif")
    st.write("**Ringkasan Statistik Jumlah Penyewaan Sepeda**")
    st.write(day_df_clean['cnt'].describe())

# 2. Distribusi Penyewaan Sepeda
elif page == "📉 Distribusi Penyewaan":
    st.title("📉 Distribusi Penyewaan Sepeda")
    
    # Histogram
    st.subheader("Histogram Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(day_df_clean['cnt'], bins=30, kde=True, color='blue', ax=ax)
    plt.xlabel('Jumlah Penyewaan Sepeda')
    plt.ylabel('Frekuensi')
    st.pyplot(fig)
    
    # Boxplot
    st.subheader("Boxplot Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(y=day_df_clean['cnt'], color='lightblue', ax=ax)
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)

# 3. Perbandingan Hari Kerja vs Akhir Pekan
elif page == "📅 Perbandingan Hari Kerja vs Akhir Pekan":
    st.title("📅 Perbandingan Hari Kerja vs Akhir Pekan")
    
    # Menambahkan kolom kategori hari kerja & akhir pekan
    day_df_clean['is_weekend'] = day_df_clean['weekday'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
    
    # Boxplot
    st.subheader("Boxplot Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=day_df_clean, x='is_weekend', y='cnt', palette='coolwarm', ax=ax)
    plt.xlabel('Kategori Hari')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)

# 4. Tren Penyewaan Sepeda berdasarkan Musim
elif page == "🌦️ Tren Penyewaan Sepeda per Musim":
    st.title("🌦️ Tren Penyewaan Sepeda per Musim")
    
    # Mengelompokkan data berdasarkan tahun dan musim
    seasonal_trend = day_df_clean.groupby(['yr', 'season'])['cnt'].mean().reset_index()
    seasonal_trend['yr'] = seasonal_trend['yr'].map({0: 2011, 1: 2012})
    
    # Lineplot
    st.subheader("Tren Penyewaan Sepeda per Musim dan Tahun")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=seasonal_trend, x='yr', y='cnt', hue='season', marker='o', palette='Set2', ax=ax)
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot(fig)

# 5. Korelasi Cuaca & Penyewaan
elif page == "📈 Korelasi Cuaca & Penyewaan":
    st.title("📈 Korelasi Cuaca & Penyewaan Sepeda")
    
    # Heatmap Korelasi
    st.subheader("Heatmap Korelasi")
    correlation_matrix = day_df_clean[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)
    
    # Scatter plot suhu vs jumlah penyewaan
    st.subheader("Scatter Plot Suhu vs Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=day_df_clean, x='temp', y='cnt', hue='season', palette='viridis', alpha=0.7, ax=ax)
    plt.xlabel('Suhu Normalisasi')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)
