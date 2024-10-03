import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Analisis Data Bike Sharing")

# Mengupload file (misal dataset CSV)
uploaded_file = st.file_uploader("Upload file dataset", type=["csv"])

if uploaded_file is not None:
    # Membaca dataset
    df = pd.read_csv("day.csv")
    df = pd.read_csv("hour.csv")
    
    # Menampilkan beberapa data
    st.write("Contoh data:")
    st.write(df.head())

    # Tambahkan analisis yang sudah dibuat di sini
    # Contoh analisis (misal: rata-rata pengguna casual dan registered)
    avg_casual = df['casual'].mean()
    avg_registered = df['registered'].mean()
    
    st.write(f"Rata-rata Casual Users: {avg_casual}")
    st.write(f"Rata-rata Registered Users: {avg_registered}")

    # Kamu bisa tambahkan visualisasi menggunakan st.line_chart, st.bar_chart, dsb.
#Mengelompokkan jam menjadi kategori : pagi, siang, sore, dan malem
def categorize_time(hour):
    if 4 <= hour <= 10:
        return 'Pagi'
    elif 10 < hour <= 14:
        return 'Siang'
    elif 14 < hour <= 18:
        return 'Sore'
    else:
        return 'Malam'

hour_df['time_category'] = hour_df['hr'].apply(categorize_time)
hour_df['time_category'].head(30)

hour_df['time_category'] = pd.Categorical(hour_df['time_category'], categories=['Pagi', 'Siang', 'Sore', 'Malam'], ordered=True)
time_trend = hour_df.groupby('time_category')['cnt'].sum().sort_index()

st.bar_chart("time_trend")



