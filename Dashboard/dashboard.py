import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Menonaktifkan peringatan PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)

with st.sidebar:
    st.image("https://www.bing.com/images/blob?bcid=r3Qdj4DiK3cGPnKpInsJR1EtlE7s.....0U")
    st.title("PROJEK DATA ANALISIS")

def plot_top_categories(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(data)))

    ax.bar(data['product_category_name_english'], data['order_id'], color=colors)
    ax.set_xlabel('Kategori Produk')
    ax.set_xticklabels(data['product_category_name_english'], rotation=45)
    ax.set_ylabel('Jumlah Pesanan')
    ax.set_title('Top 10 Kategori Produk Berdasarkan Jumlah Pesanan')
    return fig

def plot_total_sales(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(data)))

    ax.bar(data['product_category_name_english'], data['price'], color=colors)
    ax.set_xlabel('Kategori Produk')
    ax.set_xticklabels(data['product_category_name_english'], rotation=45)
    ax.set_ylabel('Total Sales')
    ax.set_title('Top 10 Kategori Produk Berdasarkan Total Sales Paling Tinggi')
    return fig

def plot_review_score(data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='review_score', y='product_category_name_english', data=data, palette='viridis')
    plt.xlabel('Review Score')
    plt.ylabel('Kategori Produk')
    plt.title('Review Score of Best Reviewed Categories')
    st.pyplot()

def plot_growth_order(data):
    sns.set(rc={'figure.figsize': (14, 8)})
    fig = plt.figure(facecolor='cyan')
    custom_palette = ['#FF5733', '#FFC300', '#C70039', '#900C3F', '#581845'] 

    ax = sns.lineplot(data=data, x='month', y='order_id',
                      hue='product_category_name_english', palette=custom_palette,
                      legend='full', lw=3)

    plt.title("Pertumbuhan order bulanan dari 5 produk yang paling laris")
    plt.ylabel('Total Sales')
    plt.xlabel('Bulan ke-')
    st.pyplot(fig)

# Read data
df_clean = pd.read_csv('./Dashboard/data.csv')

# 10 produk apa yang paling banyak dibeli?
st.title("TOP 10 Produk yang Paling Banyak Dibeli")

top_10_order = df_clean.groupby(['product_category_name_english']).agg({'order_id':'count'}).sort_values(by='order_id', ascending=False).head(10)
top_10_order = top_10_order.reset_index()

# Menampilkan tabel data
st.dataframe(top_10_order)

# Menampilkan visualisasi
fig_order = plot_top_categories(top_10_order)
st.pyplot(fig_order)

st.write("Didapatkan hasil bahwa produk yang paling banyak di-order oleh customer adalah bed_bath_table dengan kuantitas order sebanyak 9298. Lalu, diikuti oleh product category health_beauty sebanyak 8791 dan produk sports_leisure sebanyak 7717. Sementara itu, product category yang menduduki posisi ke-10 adalah toyssebesar 3853 order.")

# 10 produk yang menghasilkan total sales paling tinggi?
st.title("TOP 10 Produk dengan Total Sales Paling Tinggi")

# Menghitung total penjualan untuk top 10 kategori
total_sales = df_clean.groupby(['product_category_name_english']).agg({'price':'sum'}).sort_values(by='price', ascending=False).head(10)
total_sales = total_sales.reset_index()

# Menampilkan tabel total penjualan
st.dataframe(total_sales)
# Menampilkan visualisasi 
fig_sales = plot_total_sales(total_sales)
st.pyplot(fig_sales)

st.write("Didapatkan bahwa produk yang memberikan total sales paling tinggi adalah health_beauty, watches_gifts dan sports_leisure. Cukup menarik bed_bath_table dengan penjualan terbanyak namun untuk total sales berada pada posisi empat tertinggi.")


# 10 Produk yang mendapat review paling baik dari pelanggan?
st.title("TOP 10 Produk dengan Review paling Baik dari Pelanggan")
# Menghitung rata-rata review score untuk top 10 kategori
rata_review = df_clean.groupby(['product_category_name_english']).agg({'review_score':'mean'}).sort_values(by='review_score', ascending=False).head(10)
rata_review = rata_review.reset_index()

# Menampilkan tabel rata-rata review score
st.dataframe(rata_review)

# Menampilkan visualisasi rata-rata review score
plot_review_score(rata_review)
st.write("Review score rata-rata tertinggi adalah barang dengan kategori cds_dvds_musicals, la_cuisine, dan flowers.")


# Bagaimana pertumbuhan pemesanan produk dari 5 produk yang paling tinggi?
st.title("Pertumbuhan Pemesanan 5 Produk Terlaris")

# Menghitung pertumbuhan pemesanan produk dari 5 produk yang paling tinggi
top_5_order = df_clean[['product_category_name_english','order_id']].groupby(['product_category_name_english']).count().sort_values(by = ['order_id'], ascending = False).head(5)
grow_products = df_clean.query('product_category_name_english in @top_5_order.index')
grow_order = pd.DataFrame(data = grow_products.groupby(['month', 'product_category_name_english'])['order_id'].count()).sort_values(by = ['order_id'], ascending = False)

# Menampilkan tabel pertumbuhan pemesanan produk
st.dataframe(grow_order)
# Menampilkan visualisasi pertumbuhan pemesanan produk
plot_growth_order(grow_order)
st.write("Saat memasuki bulan ke-8 terjadi puncak lonjakan penurunan order, pemesanan produk mengalami penurunan sampai bulan Desember. Meskipun sempat terjadi kenaikan order pada bulan ke-11 tetapi pemesanan produk perlahan-lahan kembali menurun sampai bulan ke-12.")

st.title("Conclution:")
st.write('Produk dengan tingkat penjualan tertinggi cenderung menghasilkan penjualan total sales yang tinggi juga. Namun, mulai dari bulan kedelapan, terjadi penurunan pesanan dan penjualan hingga bulan terakhir. Oleh karena itu, perusahaan perlu merancang strategi yang dapat segera diimplementasikan pada bulan ke-8 untuk mempertahankan peningkatan pesanan dan penjualan produk. Beberapa langkah yang dapat diambil adalah memberikan prioritas pada pemasangan iklan untuk produk yang paling laris, memberikan diskon khusus, atau menawarkan potongan harga ongkos kirim kepada pelanggan yang sering melakukan pemesanan.')
