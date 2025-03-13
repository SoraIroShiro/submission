import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Judul Dashboard
st.title("📊 Dashboard Penyewaan Sepeda")

# Sidebar untuk Filter Data
st.sidebar.header("🔍 Filter Data")

# Filter berdasarkan Tanggal
start_date = df['dteday'].min()
end_date = df['dteday'].max()
selected_date = st.sidebar.date_input("📅 Pilih Rentang Tanggal", [start_date, end_date], min_value=start_date, max_value=end_date)

# Checkbox untuk Hari Kerja vs Akhir Pekan
show_workingday = st.sidebar.checkbox("🏢 Tampilkan Hari Kerja", value=True)
show_weekend = st.sidebar.checkbox("🌞 Tampilkan Akhir Pekan", value=True)

# Terapkan Filter
df_filtered = df[(df['dteday'] >= pd.to_datetime(selected_date[0])) & 
                 (df['dteday'] <= pd.to_datetime(selected_date[1]))]

if show_workingday and not show_weekend:
    df_filtered = df_filtered[df_filtered['workingday'] == 1]
elif show_weekend and not show_workingday:
    df_filtered = df_filtered[df_filtered['workingday'] == 0]
elif not show_workingday and not show_weekend:
    df_filtered = pd.DataFrame(columns=df.columns)  # Kosongkan data jika tidak ada checkbox yang dipilih

# Jika tidak ada checkbox yang dipilih, tampilkan semua data
total_users = df_filtered['cnt'].sum()
st.metric("🚴 Total Pengguna Setelah Filter:", f"{total_users:,}".replace(",", "."))

# Tampilkan data yang telah difilter
st.write("### Data yang Ditampilkan Setelah Filter")
st.dataframe(df_filtered.head())

# Menentukan Pertanyaan Bisnis
st.header("📌 Menentukan Pertanyaan Bisnis")

st.subheader("1️⃣ Bagaimana pola distribusi penyewaan sepeda?")
st.write("Untuk melihat insight ke depan dalam distribusi.")
if not df_filtered.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_filtered['cnt'], bins=30, kde=True, ax=ax)
    ax.set_title("Distribusi Penyewaan Sepeda")
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang tersedia untuk ditampilkan.")

st.subheader("2️⃣ Bagaimana perbedaan antara menyewa sepeda di hari kerja dan akhir pekan?")
st.write("Pertanyaan ini ditujukan untuk pemerataan kebutuhan suplai sepeda pada suatu persewaan.")
if not df_filtered.empty:
    filtered_data = df_filtered.copy()
    if show_workingday and not show_weekend:
        filtered_data = filtered_data[filtered_data['workingday'] == 1]
    elif show_weekend and not show_workingday:
        filtered_data = filtered_data[filtered_data['workingday'] == 0]
    
    if not filtered_data.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=filtered_data['workingday'].map({0: "Akhir Pekan", 1: "Hari Kerja"}), y=filtered_data['cnt'], estimator=sum, ax=ax)
        ax.set_title("Perbedaan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
        ax.set_xlabel("Jenis Hari")
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data yang tersedia untuk ditampilkan.")
else:
    st.warning("Tidak ada data yang tersedia untuk ditampilkan.")

st.subheader("3️⃣ Bagaimana tren penyewaan sepeda berdasarkan musim di setiap tahun?")
st.write("Bertujuan untuk melihat minat pesepeda pada setiap musim.")
if not df_filtered.empty:
    df_filtered['year_month'] = df_filtered['dteday'].dt.strftime('%Y-%m')
    season_trend = df_filtered.groupby(['year_month', 'season'])['cnt'].mean().unstack()
    fig, ax = plt.subplots(figsize=(10, 5))
    season_trend.plot(kind='line', marker='o', ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Bulan-Tahun")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.legend(title="Musim", labels=["Spring", "Summer", "Fall", "Winter"])
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang tersedia untuk ditampilkan.")
