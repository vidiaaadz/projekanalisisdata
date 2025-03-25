import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("E-commerce Data Dashboard")

# Membaca Dataset
order_items = pd.read_csv("order_items_dataset.csv")
products = pd.read_csv("products_dataset.csv")
payments = pd.read_csv("order_payments_dataset.csv")

# Filter Kategori Produk
st.sidebar.header("Filter Data")
selected_category = st.sidebar.multiselect("Pilih Kategori Produk", products['product_category_name'].unique())

# Menampilkan Data Order Items
st.subheader("Data Order Items")
st.dataframe(order_items.head())

# Menampilkan Data Produk
st.subheader("Data Produk")
st.dataframe(products.head())

# Menampilkan Data Pembayaran
st.subheader("Data Pembayaran")
st.dataframe(payments.head())

# Visualisasi Jumlah Pesanan per Produk
st.subheader("Jumlah Pesanan per Produk")
product_sales = order_items.groupby('product_id').size().reset_index(name='total_orders')
product_sales = product_sales.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
product_sales = product_sales.groupby('product_category_name')['total_orders'].sum().reset_index()
product_sales = product_sales.sort_values(by='total_orders', ascending=False).head(10)

# Filter berdasarkan kategori produk yang dipilih
if selected_category:
    product_sales = product_sales[product_sales['product_category_name'].isin(selected_category)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='total_orders', y='product_category_name', data=product_sales, palette='coolwarm', ax=ax)
ax.set_xlabel('Jumlah Pesanan')
ax.set_ylabel('Kategori Produk')
ax.set_title('Jumlah Pesanan per Kategori Produk (Top 10)')
st.pyplot(fig)

# Visualisasi Tipe Pembayaran
st.subheader("Tipe Pembayaran yang Paling Sering Digunakan")
payment_counts = payments['payment_type'].value_counts().reset_index()
payment_counts.columns = ['payment_type', 'count']

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='count', y='payment_type', data=payment_counts, palette='viridis', ax=ax2)
ax2.set_xlabel('Frekuensi')
ax2.set_ylabel('Tipe Pembayaran')
ax2.set_title('Distribusi Tipe Pembayaran')
st.pyplot(fig2)
