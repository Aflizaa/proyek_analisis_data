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
        - Suhu memiliki korelasi positif yang cukup kuat dengan jumlah penyewaan.
        - Kelembaban dan kecepatan angin memiliki korelasi negatif dengan penyewaan dengan pengaruh yang minimal.
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
        
        plt.bar([i - width for i in x], weather_rentals['casual'], width, label='Casual', color='#6C030D')
        plt.bar(x, weather_rentals['registered'], width, label='Registered', color='#9D0106')
        plt.bar([i + width for i in x], weather_rentals['cnt'], width, label='Total', color='#D00000')
    
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
        - Penyewaan tertinggi terjadi saat cuaca cerah.
        - Cuaca berawan mengurangi penyewaan sekitar 20%.
        - Hujan ringan menurunkan penyewaan hingga 50%.
        - Pengguna registered selalu lebih banyak  dibanding pengguna casualdi berbagai cuaca.
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
        st.subheader("1. Rata-Rata Penyewaan Berdasarkan Waktu")
        time_trend = hour_df.groupby('time_category').agg({
            'casual': 'mean',
            'registered': 'mean',
            'cnt': 'mean'
        }).round(0)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        x = range(len(time_trend.index))
        width = 0.25
        
        # Membuat bars
        casual_bars = ax3.bar([i - width for i in x], time_trend['casual'], width, label='Casual', color='#6C030D')
        registered_bars = ax3.bar(x, time_trend['registered'], width, label='Registered', color='#9D0106')
        total_bars = ax3.bar([i + width for i in x], time_trend['cnt'], width, label='Total', color='#D00000')
        
        # Menambahkan nilai di atas setiap bar
        def add_value_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')
        
        add_value_labels(casual_bars)
        add_value_labels(registered_bars)
        add_value_labels(total_bars)
        
        plt.title("Rata-rata Penyewaan Berdasarkan Waktu Hari")
        plt.xlabel("Waktu Hari")
        plt.ylabel("Rata-rata Penyewaan per Jam")
        plt.xticks(x, time_trend.index)
        plt.legend()
        
        st.pyplot(fig3)
        plt.close()
    
    with col2:
        # Hourly trend
        st.subheader("2. Tren Penyewaan Per Jam")
        hourly_trend = hour_df.groupby('hr').agg({
            'casual': 'mean',
            'registered': 'mean',
            'cnt': 'mean'
        }).round(0)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(hourly_trend.index, hourly_trend['casual'], label='Casual', color='#9D0106')
        ax4.plot(hourly_trend.index, hourly_trend['registered'], label='Registered', color='#E85D04')
        ax4.plot(hourly_trend.index, hourly_trend['cnt'], label='Total', color='#D00000')
        
        plt.title("Rata-rata Penyewaan Per Jam")
        plt.xlabel("Jam")
        plt.ylabel("Rata-rata Penyewaan")
        plt.xticks(range(0, 24))
        plt.legend()
        
        st.pyplot(fig4)
        plt.close()

elif analysis_type == "Pola Pengguna":
    st.header("Analisis Pengguna Casual vs Registered")
    
    user_pattern = day_df[['weekday', 'casual', 'registered']].groupby('weekday').mean().reset_index()
    
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=user_pattern, x='weekday', y='casual', marker='o', label='Casual', color='#9D0106')
    sns.lineplot(data=user_pattern, x='weekday', y='registered', marker='o', label='Registered', color='#E85D04' )
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
- Penyewaan tertinggi terjadi saat cuaca cerah dan musim gugur.
- Penyewaan terbanyak terjadi pada saat sore hari.
- Suhu memiliki korelasi positif yang kuat dengan jumlah penyewaan.
- Pengguna registered memiliki pola berbeda dibanding pengguna casual.
""")
