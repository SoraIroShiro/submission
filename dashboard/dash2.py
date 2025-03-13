# saya menggunakan pandas, numpy, matplotlib, dan seaborn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi visualisasi
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)


# diubah dulu tampilan tabel agar terlihat rapi
pd.set_option('display.max_columns', None)  # Menampilkan semua kolom
pd.set_option('display.expand_frame_repr', False)  # Mencegah pemotongan tampilan di terminal


# Data Wrangling - Gathering data
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("dashboard/main_data.csv")

# Menampilkan informasi awal dari dataset
day_info = day_df.info()
hour_info = hour_df.info()

# Menampilkan beberapa baris pertama
day_head = day_df.head()
hour_head = hour_df.head()


day_info, hour_info, day_head, hour_head

# Proses assesing pertama adalah mengecek tipe data

def check_data_types(day_df, hour_df):
    return pd.DataFrame({"Column": day_df.dtypes.index, "Data Type": day_df.dtypes.values}), \
           pd.DataFrame({"Column": hour_df.dtypes.index, "Data Type": hour_df.dtypes.values})

def assess_data_type(day_df, hour_df):
    print("=== Memulai Proses Assessing Data ===\n")
    
    print("1. Mengecek Tipe Data:")
    day_types, hour_types = check_data_types(day_df, hour_df)
    print(day_types, "\n")
    print(hour_types, "\n")

# pemanggilan fungsi
assess_data_type(day_df, hour_df)

def check_invalid_data(day_df, hour_df):
    """
    Mengecek apakah terdapat data yang tidak konsisten atau invalid pada kolom kategori.
    """
    invalid_data = []
    
    # Mengecek unique values di setiap kategori
    category_columns = ["season", "weekday", "weathersit"]
    for col in category_columns:
        unique_day = sorted(day_df[col].unique())
        unique_hour = sorted(hour_df[col].unique())
        
        if unique_day != unique_hour:
            status = "Inconsistent"
        else:
            status = "Consistent"
        
        invalid_data.append({"Column": f"{col} (Day DF)", "Unique Values": unique_day, "Status": status})
        invalid_data.append({"Column": f"{col} (Hour DF)", "Unique Values": unique_hour, "Status": status})
    
    return pd.DataFrame(invalid_data)

def assess_data_invalid(day_df, hour_df):
    print("2. Mengecek Data Invalid atau Tidak Konsisten:")
    print(check_invalid_data(day_df, hour_df).to_string(index=False), "\n")

# Contoh pemanggilan fungsi
assess_data_invalid(day_df, hour_df)

def check_missing_and_duplicates(day_df, hour_df):
    missing_day = day_df.isnull().sum().sum()
    missing_hour = hour_df.isnull().sum().sum()
    duplicate_day = day_df.duplicated().sum()
    duplicate_hour = hour_df.duplicated().sum()
    
    missing_df = pd.DataFrame({
        'Dataset': ['Day DF', 'Hour DF'],
        'Missing Values': [missing_day, missing_hour],
        'Duplicated Rows': [duplicate_day, duplicate_hour]
    })
    return missing_df

def assess_data_miss(day_df, hour_df):

    print("3. Mengecek Missing Values dan Duplikasi:")
    print(check_missing_and_duplicates(day_df, hour_df).to_string(index=False), "\n")

# pemanggilan fungsi
assess_data_miss(day_df, hour_df)

def detect_outliers_iqr(df, columns):
    outlier_info = {}
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_info[col] = outliers.shape[0]
    return outlier_info

def visualize_outliers(day_df, hour_df, numerical_cols):
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    
    sns.boxplot(data=day_df[numerical_cols], ax=axes[0])
    axes[0].set_title("Boxplot of Numerical Columns - Day DF")
    axes[0].set_xticklabels(numerical_cols, rotation=45, ha='right')
    
    sns.boxplot(data=hour_df[numerical_cols], ax=axes[1])
    axes[1].set_title("Boxplot of Numerical Columns - Hour DF")
    axes[1].set_xticklabels(numerical_cols, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


def assess_data_outlier(day_df, hour_df):

    numerical_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
    outliers_day = detect_outliers_iqr(day_df, numerical_cols)
    outliers_hour = detect_outliers_iqr(hour_df, numerical_cols)
    
    print("4. Mengecek Outliers:")
    print("=== Outliers in Day DF ===")
    print(pd.DataFrame(list(outliers_day.items()), columns=['Column', 'Outliers']).to_string(index=False), "\n")
    print("=== Outliers in Hour DF ===")
    print(pd.DataFrame(list(outliers_hour.items()), columns=['Column', 'Outliers']).to_string(index=False), "\n")
    
    visualize_outliers(day_df, hour_df, numerical_cols)
    
    print("=== Assessing Data Selesai ===\n")

# Contoh pemanggilan fungsi
assess_data_outlier(day_df, hour_df)

# Data Wrangling - Cleaning Data


def clean_data(day_df, hour_df):
    """
    Membersihkan data dengan:
    1. Mengonversi kolom 'dteday' ke format datetime
    2. Memetakan nilai kategori
    3. Menghapus outlier menggunakan metode IQR
    """
    print("=== Memulai Proses Cleaning Data ===\n")
    
    # === 1. Konversi Tipe Data ===
    print("[1/3] Mengonversi kolom 'dteday' ke format datetime...")
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    
    # === 2. Mapping Nilai Kategori ===
    print("[2/3] Memetakan kategori season dan weekday...")
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    
    day_df["season"] = day_df["season"].map(season_mapping)
    day_df["weekday"] = day_df["weekday"].map(weekday_mapping)
    hour_df["season"] = hour_df["season"].map(season_mapping)
    hour_df["weekday"] = hour_df["weekday"].map(weekday_mapping)
    
    # === 3. Menghapus Outlier ===
    print("[3/3] Menghapus outlier dari data menggunakan metode IQR...")
    def remove_outliers(df, columns):
        """Menghapus outlier dari kolom numerik menggunakan metode IQR."""
        initial_rows = df.shape[0]
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        final_rows = df.shape[0]
        print(f"   - Menghapus {initial_rows - final_rows} baris outlier dari {columns}.")
        return df
    
    numerical_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
    day_df = remove_outliers(day_df, numerical_cols)
    hour_df = remove_outliers(hour_df, numerical_cols)
    
    print("\n=== Cleaning Data Selesai! ===")
    print(f"Total baris setelah cleaning: Day DF = {day_df.shape[0]}, Hour DF = {hour_df.shape[0]}\n")
    
    return day_df, hour_df

# Membersihkan data
day_df_clean, hour_df_clean = clean_data(day_df, hour_df)

# Menampilkan hasil setelah cleaning
print("=== Contoh Data Setelah Cleaning (Day DF) ===")
print(day_df_clean.head())
print("\n=== Contoh Data Setelah Cleaning (Hour DF) ===")
print(hour_df_clean.head())

def plot_cleaned_boxplots(day_df_clean, hour_df_clean):
    """Menampilkan boxplot untuk data setelah cleaning."""
    numerical_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
    
    fig, axes = plt.subplots(2, len(numerical_cols), figsize=(20, 10))
    fig.suptitle("Boxplot Setelah Cleaning Outlier", fontsize=16, fontweight="bold")

    # Plot boxplot untuk Day DF
    for i, col in enumerate(numerical_cols):
        sns.boxplot(y=day_df_clean[col], ax=axes[0, i], color="lightgreen")
        axes[0, i].set_title(f"Day DF - {col}")

    # Plot boxplot untuk Hour DF
    for i, col in enumerate(numerical_cols):
        sns.boxplot(y=hour_df_clean[col], ax=axes[1, i], color="lightblue")
        axes[1, i].set_title(f"Hour DF - {col}")

    # Tambahkan label
    axes[0, 0].set_ylabel("Day DF")
    axes[1, 0].set_ylabel("Hour DF")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

# Panggil fungsi untuk menampilkan boxplot setelah cleaning
plot_cleaned_boxplots(day_df_clean, hour_df_clean)

# Pastikan day_df_clean telah dibersihkan sebelumnya
df = day_df_clean.copy()

# Statistik Deskriptif
print("Statistik Deskriptif Jumlah Penyewaan Sepeda:")
print(day_df_clean["cnt"].describe())

# Plot Histogram dengan informasi hari
plt.figure(figsize=(10, 5))
sns.histplot(data=day_df_clean, x='cnt', hue='weekday', multiple='stack', palette='viridis', bins=30)
plt.xlabel('Jumlah Penyewaan Sepeda')
plt.ylabel('Frekuensi')
plt.title('Distribusi Jumlah Penyewaan Sepeda berdasarkan Hari')
plt.legend(title='Day', labels=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
plt.show()

# Visualisasi Boxplot
plt.figure(figsize=(6, 4))
sns.boxplot(y=day_df_clean["cnt"], color="lightblue")
plt.title("Boxplot Jumlah Penyewaan Sepeda")
plt.ylabel("Jumlah Penyewaan")
plt.show()


# Menambahkan kolom baru untuk kategori hari kerja dan akhir pekan
day_df_clean['is_weekend'] = day_df_clean['weekday'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')

# Boxplot jumlah penyewaan sepeda berdasarkan hari kerja vs akhir pekan
plt.figure(figsize=(8, 5))
sns.boxplot(data=day_df_clean, x='is_weekend', y='cnt', palette='coolwarm')
plt.xlabel('Kategori Hari')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Perbedaan Jumlah Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan')
plt.show()

# Barplot rata-rata jumlah penyewaan sepeda
plt.figure(figsize=(8, 5))
sns.barplot(data=day_df_clean, x='is_weekend', y='cnt', palette='coolwarm', estimator=sum)
plt.xlabel('Kategori Hari')
plt.ylabel('Total Penyewaan Sepeda')
plt.title('Total Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan')
plt.show()

# EDA Multivariate - Tren Penyewaan Sepeda per Musim & Tahun

# Mengelompokkan data berdasarkan tahun dan musim
seasonal_trend = day_df_clean.groupby(['yr', 'season'])['cnt'].mean().reset_index()

# Mengubah nilai tahun agar lebih mudah dibaca
seasonal_trend['yr'] = seasonal_trend['yr'].map({0: 2011, 1: 2012})

# Plot tren penyewaan sepeda berdasarkan musim dan tahun
plt.figure(figsize=(10, 6))
sns.lineplot(data=seasonal_trend, x='yr', y='cnt', hue='season', marker='o', palette='Set2')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.title('Tren Penyewaan Sepeda per Musim dan Tahun')
plt.legend(title='Musim')
plt.xticks([2011, 2012])
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

### EDA Korelasi - Hubungan antara Variabel Cuaca, Musim, dan Jumlah Penyewaan Sepeda

# Mengonversi variabel kategori menjadi numerik
season_mapping = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
day_df_clean['season'] = day_df_clean['season'].map(season_mapping)

# Menghitung matriks korelasi
correlation_matrix = day_df_clean[['cnt', 'season', 'temp', 'atemp', 'hum', 'windspeed']].corr()

# Plot heatmap korelasi
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Heatmap Korelasi antara Variabel Cuaca, Musim, dan Penyewaan Sepeda')
plt.show()

# Scatter plot antara suhu dan jumlah penyewaan sepeda
plt.figure(figsize=(8, 5))
sns.scatterplot(data=day_df_clean, x='temp', y='cnt', hue='season', palette='viridis', alpha=0.7)
plt.xlabel('Suhu Normalisasi')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Musim')
plt.legend(title='Musim', labels=['Spring', 'Summer', 'Fall', 'Winter'])
plt.show()

# Visualisasi dan Explanatory Analysis

# Heatmap Korelasi
plt.figure(figsize=(10, 6))
sns.heatmap(day_df_clean[['temp', 'hum', 'cnt']].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Korelasi antara Suhu, Kelembaban, dan Jumlah Pengguna Sepeda')
plt.show()

# Scatter plot antara suhu dan jumlah penyewaan sepeda dengan kurva regresi per musim
plt.figure(figsize=(8, 5))
sns.scatterplot(data=day_df_clean, x='temp', y='cnt', hue='season', palette='viridis', alpha=0.7)

# Menyesuaikan kurva regresi polynomial untuk setiap musim
seasons = [1, 2, 3, 4]
colors = ['blue', 'green', 'orange', 'red']
labels = ['Spring', 'Summer', 'Fall', 'Winter']

for season, color, label in zip(seasons, colors, labels):
    season_data = day_df_clean[day_df_clean['season'] == season]
    if not season_data.empty:
        x = season_data['temp']
        y = season_data['cnt']
        coeffs = np.polyfit(x, y, deg=3)
        poly_eq = np.poly1d(coeffs)
        x_range = np.linspace(x.min(), x.max(), 100)
        plt.plot(x_range, poly_eq(x_range), color=color, linestyle='dashed', label=label)

plt.xlabel('Suhu Normalisasi')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Musim')
plt.legend(title='Musim')
plt.show()

# 1. Distribusi jumlah penyewaan sepeda secara keseluruhan
plt.figure(figsize=(8, 5))
sns.histplot(day_df_clean['cnt'], bins=30, kde=True, color='blue')
mean_value = day_df_clean['cnt'].mean()
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Rata-rata: {mean_value:.1f}')
plt.text(mean_value, plt.ylim()[1] * 0.9, f'{mean_value:.1f}', color='red', fontsize=12, ha='center')
plt.xlabel('Jumlah Penyewaan Sepeda')
plt.ylabel('Frekuensi')
plt.title('Distribusi Jumlah Penyewaan Sepeda Secara Keseluruhan')
plt.legend()
plt.show()

# 2. Perbedaan penyewaan sepeda antara hari kerja dan akhir pekan menggunakan bar chart
plt.figure(figsize=(8, 5))
workingday_counts = day_df_clean.groupby('workingday')['cnt'].mean()
bars = plt.bar(['0', '1'], workingday_counts, color=['red', 'green'])
plt.xlabel('Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)')
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
plt.title('Perbandingan Rata-rata Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan')

# Menambahkan garis dan angka pada bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 100, round(yval, 1), ha='center', va='bottom', fontsize=12, color='black')
    plt.axhline(yval, color='gray', linestyle='dashed', alpha=0.7)

plt.show()

# 3. Tren penyewaan sepeda berdasarkan musim di setiap tahun
plt.figure(figsize=(8, 8))
season_counts = day_df_clean.groupby('season')['cnt'].sum()
labels = ['Spring', 'Summer', 'Fall', 'Winter']
colors = ['blue', 'green', 'orange', 'red']
plt.pie(season_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title('Distribusi Penyewaan Sepeda berdasarkan Musim')
plt.show()