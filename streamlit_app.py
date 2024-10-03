import streamlit as st
import pandas as pd

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

