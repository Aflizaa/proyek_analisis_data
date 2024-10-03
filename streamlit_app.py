import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Convert dteday to datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

     # Mapping kondisi cuaca
    weather_mapping = {
        1: "Cerah",
        2: "Berawan",
        3: "Hujan Ringan",
        4: "Hujan Lebat"
    }
    
    # Tambahkan kolom baru dengan label cuaca dalam bahasa Indonesia
    day_df['kondisi_cuaca'] = day_df['weathersit'].map(weather_mapping)
    hour_df['kondisi_cuaca'] = hour_df['weathersit'].map(weather_mapping)
    
    # Add time category to hour_df
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
    
    return day_df, hour_df

# Load data
try:
    day_df, hour_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Header
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.write("oleh Afliza Husniyar Anggraini")

# Sidebar
st.sidebar.header("Opsi Dashboard")
analysis_type = st.sidebar.selectbox(
    "Pilih Analisis",
    ["Dampak Cuaca", "Tren Waktu", "Pola Pengguna"]
)

# Main content based on selection
if analysis_type == "Dampak Cuaca":
    st.header("Analisis Dampak Cuaca")
    
    # Subheader untuk korelasi
    st.subheader("1. Korelasi antara Faktor Cuaca dan Penyewaan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Correlation heatmap
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        correlation = day_df[["temp", "atemp", "hum", "windspeed", "weathersit", "cnt"]].corr()
        sns.heatmap(correlation, annot=True, cmap="Reds", fmt=".2f", square=True)
        ax_corr.set_xticklabels(['Suhu', 'Suhu Terasa', 'Kelembaban', 'Kec. Angin', 'Cuaca', 'Jumlah'], rotation=45)
        ax_corr.set_yticklabels(['Suhu', 'Suhu Terasa', 'Kelembaban', 'Kec. Angin', 'Cuaca', 'Jumlah'], rotation=45)
        st.pyplot(fig_corr)
        plt.close()
    
    with col2:
        st.write("""
        **Insight Korelasi:**
        - Suhu memiliki korelasi positif kuat dengan jumlah penyewaan
        - Kelembaban memiliki korelasi negatif dengan penyewaan
        - Kecepatan angin memiliki pengaruh minimal
        """)
    # Subheader untuk analisis kondisi cuaca
    st.subheader("2. Dampak Kondisi Cuaca Terhadap Penyewaan")
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        # Visualisasi pengaruh kondisi cuaca
        weather_rentals = day_df.groupby('kondisi_cuaca').agg({
            'casual': 'mean',
            'registered': 'mean',
            'cnt': 'mean'
        }).reset_index()
        
        fig_weather = plt.figure(figsize=(10, 6))
        x = range(len(weather_rentals['kondisi_cuaca']))
        width = 0.25
        
        plt.bar([i - width for i in x], weather_rentals['casual'], width, label='Casual', color=''#FFA07A'')
        plt.bar(x, weather_rentals['registered'], width, label='Registered', color='#FF8C00'')
        plt.bar([i + width for i in x], weather_rentals['cnt'], width, label='Total', color='#FF4500')
        
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Jumlah Penyewaan')
        plt.title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
        plt.xticks(x, weather_rentals['kondisi_cuaca'])
        plt.legend()
        
        st.pyplot(fig_weather)
        plt.close()
    
    with col4:
        st.write("""
        **Insight Kondisi Cuaca:**
        - Penyewaan tertinggi terjadi saat cuaca cerah
        - Cuaca berawan mengurangi penyewaan sekitar 20%
        - Hujan ringan menurunkan penyewaan hingga 50%
        - Pengguna registered lebih konsisten di berbagai cuaca
        """)
        
        # Tabel ringkasan
        st.write("**Tabel Ringkasan:**")
        weather_summary = weather_rentals.round(2)
        weather_summary.columns = ['Kondisi Cuaca', 'Rata-rata Casual', 'Rata-rata Registered', 'Rata-rata Total']
        st.dataframe(weather_summary)

elif analysis_type == "Tren Waktu":
    st.header("Pola Penyewaan Berdasarkan Waktu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Time category analysis
        st.subheader("Penyewaan Berdasarkan Waktu Hari")
        time_trend = hour_df.groupby('time_category')['cnt'].sum()
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        time_trend.plot(kind='bar', ax=ax3)
        plt.title("Total Penyewaan Berdasarkan Waktu Hari")
        plt.xlabel("Waktu Hari")
        plt.ylabel("Total Penyewaan")
        st.pyplot(fig3)
        plt.close()
    
    with col2:
        # Hourly trend
        st.subheader("Pola Penyewaan Per Jam")
        hourly_trend = hour_df.groupby('hr')['cnt'].mean()
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        hourly_trend.plot(ax=ax4)
        plt.title("Rata-rata Penyewaan Per Jam")
        plt.xlabel("Jam")
        plt.ylabel("Rata-rata Penyewaan")
        st.pyplot(fig4)
        plt.close()

elif analysis_type == "Pola Pengguna":
    st.header("Analisis Pengguna Casual vs Registered")
    
    user_pattern = day_df[['weekday', 'casual', 'registered']].groupby('weekday').mean().reset_index()
    
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=user_pattern, x='weekday', y='casual', marker='o', label='Casual')
    sns.lineplot(data=user_pattern, x='weekday', y='registered', marker='o', label='Registered')
    plt.title('Rata-rata Penyewaan: Pengguna Casual vs Registered')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Rata-rata Penyewaan')
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], 
               labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    st.pyplot(fig5)
    plt.close()

# Display key insights
st.sidebar.markdown("## Insight Utama")
st.sidebar.markdown("""
- Penyewaan tertinggi terjadi saat cuaca cerah dan musim gugur
- Jam puncak penyewaan adalah saat sore hari
- Suhu memiliki korelasi positif yang kuat dengan jumlah penyewaan
- Pengguna registered memiliki pola berbeda dibanding pengguna casual
""")
