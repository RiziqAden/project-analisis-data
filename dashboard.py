import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# membuat fungsi Tren Penyewaan Sepeda dari tahun 2011-2012
def create_trend_bike(df):
    trend_bike_df = df.groupby(df['dteday'].dt.to_period("M"))['cnt'].sum()
    trend_bike_df = trend_bike_df.sort_index()
    return trend_bike_df

# membuat fungsi Perbandingan Tahunan Penyewaan Sepeda (2011-2012)
def create_year_bike_df(df):
    year_df = df.groupby('yr')['cnt'].mean()
    return year_df

# membuat fungsi rata-rata pengguna dari setiap musim
def create_season_bike_mean(df):
    musim_bike_df = df.groupby('season')['cnt'].mean()
    return musim_bike_df

# membuat fungsi rata-rata pengguna dari setiap hours(jam)
def create_avg_jam_users(df):
    jam_average = df.groupby('hr')['cnt'].mean()
    return jam_average

# membuat fungsi Korelasi antara 'temp', 'atemp', 'hum', 'windspeed' dengan jumlah sepeda yang disewa?
def create_korelasi_bike_df(df):
    korelasi_df = df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    return korelasi_df

# membaca file
bike_df = pd.read_csv("bike_df.csv")

datetime_columns = ["dteday"]
bike_df.sort_values(by="dteday", inplace=True)
bike_df.reset_index(inplace=True)

for column in datetime_columns:
    bike_df[column] = pd.to_datetime(bike_df[column])
    
min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("https://github.com/RiziqAden/project-analisis-data/raw/main/Gambar-2.png")
    
    # Mengambil start_date & end_date dari date yang di input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                (bike_df["dteday"] <= str(end_date))]


season_bike_mean = create_season_bike_mean(main_df)
year_bike_df = create_year_bike_df(main_df)
avg_jam_users = create_avg_jam_users(main_df)
korelasi_bike_df = create_korelasi_bike_df(main_df)
trend_bike_df = create_trend_bike(main_df)


st.header('Bike-sharing rental Dashboard 🚲')

st.subheader('Tren penyewaan sepeda tahun 2011-2012')
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(
    trend_bike_df.index.astype(str),
    trend_bike_df.values,
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_xlabel(None)
ax.set_ylabel('Jumlah Sepeda Disewa')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)


st.subheader("Perbandingan Tahunan Penyewaan Sepeda (2011-2012)")
fig, ax = plt.subplots(figsize=(8, 5))
year_bike_df.plot(kind='bar', color="#72BCD4", ax=ax)
ax.set_xlabel('Tahun')
ax.set_ylabel('Rata-rata Sepeda Disewa')
ax.set_xticks([0, 1])
ax.set_xticklabels(['2011', '2012'], rotation=0)
st.pyplot(fig)


st.subheader("Persebaran Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
season_bike_mean.plot(kind='bar', color="#72BCD4", ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Sepeda Disewa')
ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], rotation=0, ha='center')
st.pyplot(fig)

st.subheader("melihat Korelasi antara data dengan jumlah sepeda yang disewa")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(korelasi_bike_df, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
ax.set_title('Korelasi antara Faktor Lingkungan dan Jumlah Sepeda Disewa')
st.pyplot(fig)

st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
fig, ax = plt.subplots(figsize=(10, 5))
avg_jam_users.plot(kind='bar', ax=ax, color="#72BCD4")
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Sepeda Disewa')
ax.tick_params(axis='x', labelrotation=0, labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)


st.caption('Copyright (c) M. Riziq Sirfatullah Alfarizi 2023')
