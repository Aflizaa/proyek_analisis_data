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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Correlation heatmap
        st.subheader("Korelasi antara Faktor Cuaca dan Penyewaan")
        fig, ax = plt.subplots(figsize=(10, 6))
        correlation = day_df[["temp", "atemp", "hum", "windspeed", "weathersit", "cnt"]].corr()
        sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", square=True)
        plt.title("Korelasi antara Faktor Cuaca dan Jumlah Penyewaan")
        ax.set_xticklabels(['Suhu', 'Suhu Terasa', 'Kelembaban', 'Kec. Angin', 'Cuaca', 'Jumlah'], rotation=45)
        ax.set_yticklabels(['Suhu', 'Suhu Terasa', 'Kelembaban', 'Kec. Angin', 'Cuaca', 'Jumlah'], rotation=45)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("Pengaruh Suhu Terhadap Penyewaan")
        day_df['temp_bins'] = pd.cut(day_df['temp'], 
                                    bins=[0, 0.2, 0.4, 0.6, 0.8, 1], 
                                    labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])
        weather_effect = day_df.groupby('temp_bins')['cnt'].mean()
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        weather_effect.plot(kind='bar', ax=ax2)
        plt.title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
        plt.xlabel("Kategori Suhu")
        plt.ylabel("Rata-rata Jumlah Penyewaan")
        st.pyplot(fig2)
        plt.close()

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
