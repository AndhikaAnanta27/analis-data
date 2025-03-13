import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setel konfigurasi halaman di bagian paling atas
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load dataset
@st.cache
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Mengubah kolom 'dteday' menjadi datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    return day_df, hour_df

day_df, hour_df = load_data()

# Streamlit setup
# Sidebar Navigation
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih menu", ["Overview", "Analisis Musim", "Perbandingan Pengguna", "Ekspor Data"])

st.title("🚴‍♂️ Dashboard Analisis Data Bike Sharing")
st.markdown("---")

# Seksi Overview
if menu == "Overview":
    st.header("📊 Overview Data Bike Sharing")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Hari", day_df.shape[0])
    col2.metric("Jumlah Jam Data", hour_df.shape[0])
    col3.metric("Total Penyewa", day_df['cnt'].sum())
    
    st.subheader("Ringkasan Data")
    st.write(day_df.describe())

# Seksi Analisis Musim
elif menu == "Analisis Musim":
    st.header("📈 Analisis Musim")
    
    # Menambahkan fitur filter untuk memilih musim (season)
    season_filter = st.selectbox("Pilih Musim", ['All', 'Spring', 'Summer', 'Fall', 'Winter'])

    # Pemetaan kode musim ke label
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season'] = day_df['season'].map(season_labels)

    # Filter data berdasarkan musim yang dipilih
    if season_filter != 'All':
        day_df = day_df[day_df['season'] == season_filter]

    # Mengelompokkan data berdasarkan musim untuk menghitung jumlah penyewa
    season_counts = day_df.groupby('season')['cnt'].sum()

    # Membuat grafik batang yang menunjukkan total penyewa per musim
    fig, ax = plt.subplots(figsize=(8, 6))
    season_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Total Penyewa per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewa')
    ax.set_xticklabels(season_counts.index, rotation=45)

    st.pyplot(fig)

# Seksi Perbandingan Pengguna
elif menu == "Perbandingan Pengguna":
    st.header("💼 Pengguna Terdaftar vs Kasual")
    
    # Menambahkan fitur filter untuk memilih rentang tanggal
    start_date = st.date_input("Pilih Tanggal Mulai", min_value=day_df['dteday'].min(), max_value=day_df['dteday'].max())
    end_date = st.date_input("Pilih Tanggal Selesai", min_value=day_df['dteday'].min(), max_value=day_df['dteday'].max())

    # Filter data berdasarkan rentang tanggal
    filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

    # Mengelompokkan data berdasarkan bulan untuk menghitung total pengguna kasual dan terdaftar
    monthly_data = filtered_day_df.groupby('mnth').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()

    # Membuat plot garis untuk membandingkan pengguna kasual dan terdaftar
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_data['mnth'], monthly_data['casual'], label='Pengguna Kasual', color='blue', marker='o')
    ax.plot(monthly_data['mnth'], monthly_data['registered'], label='Pengguna Terdaftar', color='orange', marker='o')

    ax.set_title('Perbandingan Bulanan: Pengguna Kasual vs Terdaftar')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewa')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# Seksi Ekspor Data
elif menu == "Ekspor Data":
    st.header("📤 Ekspor Data ke CSV")
    if st.button("Ekspor Data ke CSV"):
        all_df = pd.concat([day_df, hour_df], ignore_index=True)
        all_df.to_csv("all_bike_data.csv", index=False)
        st.success("Data berhasil diekspor sebagai all_bike_data.csv.")

st.sidebar.info("Dikembangkan oleh Andhika Putra Ananta")
