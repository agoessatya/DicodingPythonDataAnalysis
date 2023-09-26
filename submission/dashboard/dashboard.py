import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from millify import millify
from babel.numbers import format_currency
sns.set(style='white')

def data_process(data):
    bikebyseason = data.groupby('season')['cnt'].sum().reset_index()
    bikebyseason = bikebyseason.rename(columns={'cnt': 'total count'})

    bikebyweather = data.groupby('weathersit')['cnt'].sum().reset_index()
    bikebyweather = bikebyweather.rename(columns={'cnt': 'total count'})
    return bikebyseason, bikebyweather

def make_df(data, date_parameter):
    main_df = data[(data[date_parameter] >= str(start_date)) & (data[date_parameter] <= str(end_date))]
    return main_df

day_data = pd.read_csv('D:/tes_nc/Dicoding/AnalisisDataPython/submission/dashboard/bike_day_data.csv')
hour_data = pd.read_csv('D:/tes_nc/Dicoding/AnalisisDataPython/submission/dashboard/bike_hour_data.csv')

datetime_columns = ["dteday"]
day_data.sort_values(by="dteday", inplace=True)
day_data.reset_index(inplace=True)
for column in datetime_columns:
    day_data[column] = pd.to_datetime(day_data[column])
hour_data.sort_values(by="dteday", inplace=True)
hour_data.reset_index(inplace=True)
for column in datetime_columns:
    hour_data[column] = pd.to_datetime(hour_data[column])


min_date = hour_data["dteday"].min()
max_date = hour_data["dteday"].max()

with st.sidebar:
    st.image("D:/tes_nc/Dicoding/AnalisisDataPython/submission/dashboard/Logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

day_main_df = make_df(day_data, "dteday")
hour_main_df = make_df(hour_data, "dteday")
day_bikebyseason, day_bikeweather = data_process(day_main_df)
hour_bikebyseason, hour_bikeweather = data_process(hour_main_df)

st.header('Dicoding Rental Bike :bike:')
st.subheader('Daily Orders')
col1, col2, col3 = st.columns(3)
with col1:
    total_orders = day_main_df.cnt.sum()
    st.metric("Total Orders", millify(total_orders, precision=2))
with col2:
    mean_orders = day_main_df.cnt.mean()
    st.metric("Daily Orders Averange", millify(mean_orders, precision=2))
with col3:
    mean_orders = hour_main_df.cnt.mean()
    last_orders = int((hour_main_df['cnt'].iloc[-2]) - (hour_main_df['cnt'].iloc[-1]))
    st.metric("Order per Hour", millify(mean_orders), delta=last_orders)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_main_df["dteday"],
    day_main_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader('The Most Time of Biggest Amount of Bike Rental')
colors = ['#b45c64','#7c8cb4','#7c8cb4','#7c8cb4','#7c8cb4']
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
sns.barplot(x="season", y="total count", data=day_bikebyseason, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Season", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)
ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
sns.barplot(x="weathersit", y="total count", data=hour_bikeweather, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("By Weather", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
st.pyplot(fig)


st.subheader('The Time Series Correlation Between Temp and Bike Rental')
fig, ax1 = plt.subplots(figsize=(15, 5))
ax2 = ax1.twinx()
ax1.plot(day_main_df["instant"],
         day_main_df["atemp"],
         color='r',
         linewidth=0.5,
         label='temp')
ax2.plot(day_main_df["instant"],
         day_main_df["cnt"],
         color='b',
         linewidth=0.5,
         label='total count')
ax1.set_xlabel('X data')
ax1.set_ylabel('Temp', color='r')
ax2.set_ylabel('Total Bike Count', color='b')
ax1.legend(loc=1)
ax2.legend(loc=2)
plt.title('Temp Against Total Count', loc="center", fontsize=20)
st.pyplot(fig)
corr_score = day_main_df["atemp"].corr(day_main_df["cnt"])
st.caption('Correlation Score = '+ str(corr_score))


st.subheader('The Time Series Correlation Between Humidity and Bike Rental')
fig, ax1 = plt.subplots(figsize=(15, 5))
ax2 = ax1.twinx()
ax1.plot(day_main_df["instant"],
         day_main_df["hum"],
         color='g',
         linewidth=0.5,
         label='hum')
ax2.plot(day_main_df["instant"],
         day_main_df["cnt"],
         color='r',
         linewidth=0.5,
         label='total count')
ax1.set_xlabel('X data')
ax1.set_ylabel('Temp', color='r')
ax2.set_ylabel('Total Bike Count', color='b')
ax1.legend(loc=1)
ax2.legend(loc=2)
plt.title('Humidity Against Total Count', loc="center", fontsize=20)
st.pyplot(fig)
corr_score = day_main_df["hum"].corr(day_main_df["cnt"])
st.caption('Correlation Score = '+ str(corr_score))

st.subheader('Total Average of Rental Bike Each Hour and Holiday')
bike_hour_byhour = hour_main_df.groupby('hr')['cnt'].sum().reset_index()
bike_hour_byhour = bike_hour_byhour.rename(columns={'cnt': 'total count'})
bike_hour_byholiday = hour_main_df.groupby('holiday')['cnt'].sum().reset_index()
bike_hour_byholiday = bike_hour_byholiday.rename(columns={'cnt': 'total count'})
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
sns.barplot(x="hr", y="total count", data=bike_hour_byhour, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Count of Total Rental Bike by Season Hourly", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)
ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
sns.barplot(x="holiday", y="total count", data=bike_hour_byholiday, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Count of Total Rental Bike by Holiday or Not", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
st.pyplot(fig)


st.subheader('How do time parameters influence the number of bicycle rentals?')
st.caption('Diketahui bahwa parameter cuaca berpengaruh terhadap jumlah penyewaan sepeda. Dapat diketahui dari tabel dan grafik yang diperoleh bahwa cuaca cerah merupakan favorit untuk orang menggunakan sepeda dan enggan untuk menyewa ketika hujan atau salju turun. Kemudian orang lebih memilih untuk menggunakan sepeda di musim autumn atau gugur dan kurang menyukai bersepeda di musim spring atau semi. Hal ini kemudian dianalisis lebih lanjut dengan melihat kesesuaian time-series dari suhu udara rata-rata dan kelembapan terhadap jumlah penyewaan sepeda. Di mana pada musim gugur cuaca lebih sejuk, dan musim semi cuaca lebih lembab. Diketahui bahwa suhu memiliki korelasi 0.6 atau 60% terhadap jumlah penyewaan sepeda dan berkorelasi negatif terhadap kelembapan dengan nilai -0.1 atau 10%')

st.subheader('How do time parameters influence the number of bicycle rentals?')
st.caption('Diketahui bahwa parameter waktu mempengaruhi orang untuk menyewa sepeda. Di mana pada hari kerja, jumlah penyewaan sepeda jauh lebih tinggi dibandingkan dengan akhir pekan atau libur. Ini dikarenakan mobilitas orang yang lebih tinggi pada saat hari kerja. Kemudian pola yang mendukung terlihat apabila dianalisis parameter jam terhadap penyewaan sepeda. Tingkat penyewaan tertinggi terjadi pada saat rush hour ketika orang berangkat kerja ataupun sekolah yaitu pukul 8 untuk berangkat dan 17 untuk kepulangan.')