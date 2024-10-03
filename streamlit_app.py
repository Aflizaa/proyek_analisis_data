import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Analisis Data Penyewaan Sepeda")

# Mengupload file dataset day dan hour
uploaded_day_file = st.file_uploader("Upload file dataset harian (day.csv)", type=["csv"])
uploaded_hour_file = st.file_uploader("Upload file dataset jam (hour.csv)", type=["csv"])

# Jika file diupload, tampilkan beberapa data
if uploaded_day_file is not None and uploaded_hour_file is not None:
    day_df = pd.read_csv(uploaded_day_file)
    hour_df = pd.read_csv(uploaded_hour_file)

    st.write("Contoh data harian:")
    st.write(day_df.head())
    
    st.write("Contoh data jam:")
    st.write(hour_df.head(30))

    # Data Wrangling - Mengubah tipe data
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Descriptive Statistics
    st.subheader("Statistik Deskriptif Data Harian:")
    st.write(day_df.describe())

    st.subheader("Statistik Deskriptif Data Jam:")
    st.write(hour_df.describe())
    
    # Analisis Pertanyaan 1: Penyewaan tertinggi berdasarkan tanggal
    busiest_day = day_df.loc[day_df['cnt'].idxmax()]
    st.write(f"Tanggal dengan penyewaan terbanyak: {busiest_day['dteday'].date()} dengan jumlah penyewaan {busiest_day['cnt']}")

    # Analisis Pertanyaan 2: Penyewaan berdasarkan cuaca
    st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
    weather_trend = day_df.groupby('weathersit')['cnt'].mean().reset_index()
    st.write(weather_trend)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=weather_trend['weathersit'], y=weather_trend['cnt'], palette='coolwarm')
    plt.title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

    # Analisis Penyewaan Berdasarkan Waktu (Pagi, Siang, Sore, Malam)
    st.write(hour_df['hour'].describe())  # Untuk memeriksa rentang nilai hour
if hour_df['hour'].min() < 0 or hour_df['hour'].max() > 23:
    st.error("Nilai jam di luar rentang 0-23!")

    hour_df['hour'] = pd.to_datetime(hour_df['dteday']).dt.hour
    hour_df['time_category'] = pd.cut(hour_df['hour'], bins=[0, 4, 10, 14, 18, 24],
                                  labels=['Malam', 'Pagi', 'Siang', 'Sore', 'Malam'], right=False)
    time_trend = hour_df.groupby('time_category')['cnt'].sum().reset_index()
    
    st.subheader("Jumlah Penyewaan Berdasarkan Waktu")
    st.write(time_trend)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='time_category', y='cnt', data=time_trend, palette='viridis')
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Waktu')
    plt.xlabel('Waktu')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

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

else:
    st.write("Silakan upload file dataset untuk melakukan analisis.")
    



