import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Dashboard Analisis Data Penyewaan Sepeda")

# Membaca dataset dari file lokal
day_df = pd.read_csv('day.csv')  # Pastikan file ini ada di repositori GitHub kamu
hour_df = pd.read_csv('hour.csv')  # Pastikan file ini ada di repositori GitHub kamu

# Tampilkan contoh data
st.subheader("Contoh Data Harian")
st.write(day_df.head())

st.subheader("Contoh Data Jam")
st.write(hour_df.head(30))

# Data Wrangling - Mengubah tipe data
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Descriptive Statistics
st.subheader("Statistik Deskriptif Data Harian")
st.write(day_df.describe())

st.subheader("Statistik Deskriptif Data Jam")
st.write(hour_df.describe())

# Analisis Pertanyaan 1: Penyewaan tertinggi berdasarkan tanggal
busiest_day = day_df.loc[day_df['cnt'].idxmax()]
st.subheader(f"Penyewaan Tertinggi Tanggal: {busiest_day['dteday'].date()} dengan {busiest_day['cnt']} penyewaan")

# Analisis Pertanyaan 2: Penyewaan berdasarkan cuaca
st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
weather_trend = day_df.groupby('weathersit')['cnt'].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x=weather_trend['weathersit'], y=weather_trend['cnt'], palette='coolwarm')
plt.title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

# Analisis Penyewaan Berdasarkan Waktu (Pagi, Siang, Sore, Malam)
hour_df['hour'] = hour_df['dteday'].dt.hour  # Menggunakan .hour, bukan .hr

# Menampilkan nilai jam yang tersedia
st.subheader("Nilai Jam yang Tersedia")
st.write(hour_df['hour'].unique())  # Tampilkan nilai unik dari kolom 'hour'

# Menampilkan statistik dari kolom cnt
st.subheader("Statistik Penyewaan (cnt)")
st.write(hour_df['cnt'].describe())  # Tampilkan statistik dari kolom 'cnt'

# Mengkategorikan waktu menggunakan fungsi
def categorize_time(hour):
    if 0 <= hour < 4:
        return 'Malam'
    elif 4 <= hour < 10:
        return 'Pagi'
    elif 10 <= hour < 14:
        return 'Siang'
    elif 14 <= hour < 18:
        return 'Sore'
    else:
        return 'Malam'

# Menambahkan kolom time_category
hour_df['time_category'] = hour_df['hour'].apply(categorize_time)

# Menghitung jumlah penyewaan berdasarkan kategori waktu
time_trend = hour_df.groupby('time_category')['cnt'].sum().reset_index()

# Menampilkan total penyewaan per kategori waktu
st.subheader("Jumlah Penyewaan per Kategori Waktu")
st.write(time_trend)  # Tampilkan total penyewaan per kategori waktu

# Menampilkan hasil dalam tabel
st.subheader("Tabel Jumlah Penyewaan per Kategori Waktu")
st.write(hour_df[['time_category', 'cnt']].head(30))  # Tampilkan beberapa baris untuk memeriksa kategorinya

# Analisis Pertanyaan 3: Pola pengguna Casual vs Registered
st.subheader("Pola Penyewaan Casual vs Registered")
user_pattern = day_df[['weekday', 'casual', 'registered']].groupby('weekday').mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=user_pattern, x='weekday', y='casual', marker='o', label='Casual')
sns.lineplot(data=user_pattern, x='weekday', y='registered', marker='o', label='Registered')
plt.title('Rata-rata Penyewaan Sepeda Casual vs Registered per Hari')
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
plt.legend()
st.pyplot(plt)

# Kesimpulan
st.subheader("Kesimpulan:")
st.write("""
1. Penyewaan sepeda tertinggi terjadi pada cuaca cerah.
2. Tren penyewaan tertinggi terjadi di sore hari.
3. Pengguna casual lebih banyak menyewa pada hari kerja, sedangkan pengguna registered cenderung lebih banyak di akhir pekan.
""")
