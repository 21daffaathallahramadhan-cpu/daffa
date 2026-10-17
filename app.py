import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi Halaman Streamlit agar menjadi Wide Mode
st.set_page_config(
    page_title="Dashboard Data Fiskal Daerah",
    page_icon="📊",
    layout="wide",
)

# URL Dataset
DATA_URL = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/refs/heads/main/dataset_fiskal_97_hipoFull.csv"


# Fungsi untuk memuat data dengan caching agar lebih cepat
@st.cache_data
def load_data(url):
  df = pd.read_csv(url)
  return df


# Load data
df = load_data(DATA_URL)

# ================= SIDEBAR (FILTER) =================
st.sidebar.markdown("### 🔍 Filter Data")

# Cek nama kolom yang tersedia untuk menyesuaikan (biasanya 'Kota' dan 'Tahun')
# Pastikan nama kolom sesuai dengan dataset Anda
col_kota = (
    "Kota" if "Kota" in df.columns else df.columns[0]
)  # Sesuaikan jika berbeda
col_tahun = (
    "Tahun" if "Tahun" in df.columns else df.columns[1]
)  # Sesuaikan jika berbeda

# Filter Kota
list_kota = sorted(df[col_kota].unique().tolist())
selected_kota = st.sidebar.multiselect(
    "Pilih Kota", list_kota, default=list_kota[:5]
)

# Filter Rentang Tahun
min_tahun = int(df[col_tahun].min())
max_tahun = int(df[col_tahun].max())
selected_tahun = st.sidebar.slider(
    "Rentang Tahun", min_tahun, max_tahun, (min_tahun, max_tahun)
)

# Filter Menu Navigasi Sederhana
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Fiskal")
menu = st.sidebar.selectbox(
    "Pilih Menu", ["Ringkasan", "Visualisasi Grafik"]
)

# Terapkan Filter ke DataFrame
df_filtered = df[
    (df[col_kota].isin(selected_kota))
    & (df[col_tahun] >= selected_tahun[0])
    & (df[col_tahun] <= selected_tahun[1])
]

# ================= HALAMAN UTAMA =================
st.title("💖 Dashboard Data Fiskal Daerah")
st.markdown(
    "Visualisasi data penerimaan fiskal, belanja pemerintah, dan indikator"
    " sosial ekonomi berdasarkan kota dan tahun."
)
st.markdown("")

# Metrik / Angka Ringkasan di Bagian Atas
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(label="Jumlah Observasi", value=len(df_filtered))
with col2:
  st.metric(
      label="Jumlah Kota", value=df_filtered[col_kota].nunique()
  )
with col3:
  st.metric(
      label="Jumlah Tahun",
      value=df_filtered[col_tahun].nunique(),
  )
with col4:
  st.metric(label="Jumlah Variabel", value=len(df_filtered.columns))

st.markdown("---")

# ================= KONTEN BERDASARKAN MENU =================
if menu == "Ringkasan":
  st.subheader("Ringkasan Data")
  # Menampilkan tabel data yang sudah difilter
  st.dataframe(df_filtered, use_container_width=True)

elif menu == "Visualisasi Grafik":
  st.subheader("Grafik Analisis Data Fiskal")

  if not df_filtered.empty:
    # Contoh Plot sederhana: Rata-rata variabel berdasarkan Tahun atau Kota
    numeric_cols = df_filtered.select_dtypes(
        include=["float64", "int64"]
    ).columns.tolist()
    if col_tahun in numeric_cols:
      numeric_cols.remove(col_tahun)

    selected_var = st.selectbox("Pilih Variabel untuk Dilihat:", numeric_cols)

    # Buat Bar Chart / Line Chart menggunakan Plotly
    fig = px.line(
        df_filtered,
        x=col_tahun,
        y=selected_var,
        color=col_kota,
        markers=True,
        title=f"Tren {selected_var} Berdasarkan Tahun",
    )
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.warning("Data kosong, silakan sesuaikan filter Anda.")
