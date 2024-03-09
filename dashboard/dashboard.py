import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from PIL import Image

sns.set(style='dark')

day = pd.read_csv("https://raw.githubusercontent.com/fildzahkhls/ProjekAnalisisData/main/data/day.csv")
hour = pd.read_csv("https://raw.githubusercontent.com/fildzahkhls/ProjekAnalisisData/main/data/hour.csv")

hour.drop(columns=['instant', 'workingday'], inplace=True)
day.drop(columns=['instant', 'workingday'], inplace=True)

hour['dteday'] = pd.to_datetime(hour['dteday'])
day['dteday'] = pd.to_datetime(day['dteday'])

columns = ['season', 'mnth', 'holiday', 'weekday', 'weathersit']

for column in columns:
    hour[column] = hour[column].astype("category")
    day[column] = day[column].astype("category")

day.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
hour.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)

day.mnth.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), inplace=True)
hour.mnth.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), inplace=True)

day.weathersit.replace((1, 2, 3, 4), ('Bright', 'Misty', 'Lightsnow', 'Heavysnow'), inplace=True)
hour.weathersit.replace((1, 2, 3, 4), ('Bright', 'Misty', 'Lightsnow', 'Heavysnow'), inplace=True)

day.weekday.replace((0, 1, 2, 3, 4, 5, 6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)
hour.weekday.replace((0, 1, 2, 3, 4, 5, 6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)

day.yr.replace((0, 1), ('2011', '2012'), inplace=True)
hour.yr.replace((0, 1), ('2011', '2012'), inplace=True)


def get_monthly_total_rentals(hour):
    monthly_total_rentals = hour.groupby(pd.Grouper(key='dteday', freq='M'))['cnt'].sum()
    return monthly_total_rentals


def get_hourly_rentals(hour):
    hourly_rentals = hour.groupby('hr')['cnt'].mean()
    return hourly_rentals


def seasonal_rentals(hour):
    seasonal_rentals = hour.groupby('season')['cnt'].mean()
    return seasonal_rentals


def daily_rent(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df


def daily_casual_rent(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df


def daily_registered_rent(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df


st.image("bg.jpeg")
st.header('Bike Rentals 🚲')

min_date = pd.to_datetime(day['dteday']).dt.date.min()
max_date = pd.to_datetime(day['dteday']).dt.date.max()

start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = day[(day['dteday'] >= str(start_date)) &
              (day['dteday'] <= str(end_date))]

daily_rent_df = daily_rent(main_df)
daily_casual_rent_df = daily_casual_rent(main_df)
daily_registered_rent_df = daily_registered_rent(main_df)

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total User', value=daily_rent_total)

# Masuk ke visualisasi
st.subheader("Bagaimana pola jumlah peminjaman sepeda pada setiap jam dalam satu hari?")

plt.figure(figsize=(10, 6))
bars = plt.bar(get_hourly_rentals(hour).index, get_hourly_rentals(hour).values, color='skyblue')


top_3_hours = get_hourly_rentals(hour).nlargest(3).index
bottom_3_hours = get_hourly_rentals(hour).nsmallest(3).index

for hours in top_3_hours:
    bars[hours].set_color('navy')

for hours in bottom_3_hours:
    bars[hours].set_color('lightcoral')

plt.title('Pola Jumlah Peminjaman Sepeda pada Setiap Jam dalam Satu Hari')
plt.xlabel('Jam (0-23)')
plt.ylabel('Jumlah Peminjaman Sepeda (Rata-rata)')
plt.xticks(range(24), labels=[f'{hours}:00' for hours in range(24)], rotation=45)  # Mengatur label sumbu x
plt.grid(axis='y')

st.pyplot(plt.gcf())

st.write("Dari hasil visualisasi diatas, dapat diketahui bahwa peminjaman sepeda paling tinggi pada pagi hari yaitu jam 8 dan sore hari dijam 5 dan jam 6 dan paling rendah itu disubuh hari jam 3, 4 dan 5")

st.subheader("Apakah terdapat tren jangka panjang dalam jumlah total peminjaman sepeda dari waktu ke waktu?")

plt.figure(figsize=(10, 6))
plt.plot(get_monthly_total_rentals(hour).index, get_monthly_total_rentals(hour).values, marker='o', linestyle='-')
plt.title('Total Peminjaman Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Total Peminjaman Sepeda')
plt.grid(True)
st.pyplot(plt.gcf())
st.write("Dari hasil visualisasi di atas, terlihat bahwa peminjaman sepeda mencapai puncaknya antara bulan 7 dan 10 2012. Sedangkan peningkatan tertinggi terjadi antara bulan 3 dan 4 2012, dan penurunan tertinggi terjadi antara bulan 10 dan bulan 11 2012.")

st.subheader("Bagaimana korelasi antara musim dan jumlah penyewaan sepeda harian, pada musim apakah peminjam terbanyak?")

plt.figure(figsize=(8, 6))
seasonal_rentals(hour).plot(kind='bar', color='skyblue')
plt.title('Korelasi antara Musim dan Jumlah Penyewaan Sepeda Harian')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan Sepeda Harian (Rata-rata)')
plt.xticks(range(4), rotation=45)
plt.grid(axis='y')
st.pyplot(plt.gcf())
st.write("Dari hasil visualisasi diatas, dapat diketahui bahwa peminjaman sepeda paling tinggi terjadi pada musim gugur, diikuti dengan musim panas, musim dingin, dan musim semi.")

st.subheader("Bagaimana perbandingan jumlah peminjaman sepeda antara registered (pelanggan terdaftar) dan casual (pelanggan tidak terdaftar) pada hari libur?")

weekend_data = hour.loc[(hour['weekday'] == 'Saturday') | (hour['weekday'] == 'Sunday')]
registered_rentals = weekend_data['registered'].sum()
casual_rentals = weekend_data['casual'].sum()
labels = ['Registered', 'Casual']
colors = ['lightpink', 'lightskyblue']

plt.figure(figsize=(8, 6))
plt.pie([registered_rentals,casual_rentals], labels=[f'{label}: {count}' for label, count in zip(labels, [registered_rentals,casual_rentals])], colors=colors, autopct='%1.1f%%', startangle=100)
plt.title('Perbandingan Jumlah Peminjaman Sepeda pada Hari Libur (Sabtu dan Minggu)')
plt.axis('equal')
st.pyplot(plt.gcf())
st.write("Dari hasil visualisasi diatas, dapat diketahui bahwa peminjaman sepeda pada hari libur kebanyakan adalah dari peminjam terdaftar (registered) dengan besaran 68.1% sedangkan casual hanya 31.9%")

st.subheader("Conclusion")
st.write("Kesimpulan dari pertanyaan 1 yaitu, pola peminjaman sepeda menunjukkan adanya tren yang konsisten sepanjang hari. Puncak peminjaman terjadi pada sore hari sekitar jam 5 dan 6 dan paling rendah itu disubuh hari jam 3, 4 dan 5, yang kemungkinan disebabkan oleh pulangnya orang-orang dari tempat kerja atau sekolah dan menggunakan sepeda untuk rekreasi atau kegiatan lainnya. Sedangkan peminjaman tertinggi selanjutnya terjadi pada pagi hari sekitar jam 8, yang mungkin karena banyaknya orang yang menggunakan sepeda sebagai sarana transportasi untuk berangkat ke tempat kerja atau sekolah. Selain itu, terdapat penurunan jumlah peminjaman pada jam 12 malam hingga sekitar jam 7 pagi, serta pada malam hari. Pola ini berulang setiap hari, menunjukkan bahwa pola peminjaman sepeda pada setiap jam dalam satu hari relatif konsisten dan dapat diandalkan.")
st.write("Kesimpulan pertanyaan 2 yaitu, terdapat tren jangka panjang dalam jumlah total peminjaman sepeda dari waktu ke waktu. Peminjaman sepeda mencapai puncaknya antara bulan Juli dan Oktober 2012. Peningkatan tertinggi dalam jumlah peminjaman terjadi antara bulan Maret dan April 2012, menunjukkan adanya peningkatan signifikan dalam minat masyarakat untuk menggunakan layanan peminjaman sepeda pada periode tersebut. Namun, terdapat penurunan tertinggi dalam jumlah peminjaman antara bulan Oktober dan November 2012, yang mungkin disebabkan oleh faktor-faktor musiman atau perubahan tren dalam preferensi transportasi. Ini menunjukkan bahwa meskipun terdapat fluktuasi dalam jumlah peminjaman sepeda dari waktu ke waktu, tren jangka panjang menunjukkan adanya periode tertentu di mana minat masyarakat dalam menggunakan layanan peminjaman sepeda lebih tinggi daripada periode lainnya.")
st.write("Kesimpulan pertanyaan 3 yaitu, Peminjaman sepeda paling tinggi terjadi pada musim gugur, yang kemungkinan disebabkan oleh cuaca yang lebih sejuk dan kondisi yang lebih nyaman untuk bersepeda. Diikuti oleh musim panas, dimana cuaca yang cerah dan hangat membuat orang lebih cenderung untuk beraktivitas di luar ruangan, termasuk bersepeda. Selanjutnya, jumlah penyewaan sepeda pada musim dingin menunjukkan penurunan, mungkin karena cuaca yang lebih dingin dan kurangnya preferensi untuk bersepeda di musim tersebut. Sedangkan pada musim semi, jumlah penyewaan sepeda berada di antara musim gugur dan musim panas. Oleh karena itu, dapat disimpulkan bahwa peminjaman sepeda cenderung tertinggi pada musim gugur, diikuti oleh musim panas, musim semi, dan musim dingin.")
st.write("Kesimpulan pertanyaan 4 yaitu, Pada hari libur, sebagian besar peminjaman sepeda berasal dari pelanggan terdaftar (registered), dengan proporsi sebesar 68.1%. Ini menunjukkan bahwa pada hari libur, pelanggan terdaftar cenderung lebih aktif dalam menggunakan layanan penyewaan sepeda dibandingkan dengan pelanggan tidak terdaftar (casual). Kemungkinan besar, pelanggan terdaftar memiliki keanggotaan atau komitmen jangka panjang dengan penyedia layanan, sehingga mereka cenderung menggunakan layanan tersebut secara rutin bahkan pada hari libur.Di sisi lain, pelanggan tidak terdaftar (casual) hanya menyumbang sekitar 31.9%' dari total peminjaman sepeda pada hari libur. Ini bisa menunjukkan bahwa pelanggan casual mungkin menggunakan layanan penyewaan sepeda secara sporadis atau hanya pada kesempatan tertentu, seperti liburan atau acara khusus.")