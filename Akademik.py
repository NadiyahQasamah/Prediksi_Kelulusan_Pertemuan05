import pickle
import numpy as np
import streamlit as st

# Load model random forest
with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
# Inisialisasi halaman untuk pertama kali
if 'page' not in st.session_state:
    st.session_state.page = 'beranda'


#sidebar
st.sidebar.title('Menu')
if st.sidebar.button('🏠 Beranda'):
    st.session_state.page = 'beranda'
if st.sidebar.button('📊 Form Prediksi'):
    st.session_state.page = 'prediksi'


# Halaman BERANDA
if st.session_state.page == 'beranda':
    st.title('Selamat Datang di Akademik')
    st.write('Silakan Masukkan Nama dan Tahun Masuk')

    # Input Nama & Tahun
    st.session_state.nama = st.text_input('Nama', st.session_state.get('nama','')) #Nama
    st.session_state.tahun = st.date_input('Tahun Masuk', st.session_state.get('tahun', None)) #Tahun

    # Tombol untuk lanjut ke Form Prediksi
    if st.button('Lanjut ke Form Prediksi'):
        if st.session_state.nama and st.session_state.tahun:
            # ubah page, akan menampilkan form prediksi
            st.session_state.page = 'prediksi'
        else:
            st.error('Silakan isi Nama dan Tahun Masuk terlebih dahulu!')


#Halaman FORM DATA
elif st.session_state.page == 'prediksi':
    st.title('📊 Form Prediksi Kelulusan Mahasiswa')
    
    # mengambil data dari Beranda
    nama = st.session_state.get('nama', '-')
    tahun = st.session_state.get('tahun', '-')
    
    st.write(f'Nama: **{nama}**')
    st.write(f'Tahun Masuk: **{tahun}**')
    
    
    # Form input
    gender = {'Perempuan': 0, 'Laki-laki': 1}[st.selectbox('Jenis Kelamin?', ['Perempuan', 'Laki-laki'])]
    matrial_status = {'Menikah': 0, 'Belum Menikah': 1}[st.selectbox('Status', ['Menikah', 'Belum Menikah'])]
    attendance = st.number_input('Persentase Kehadiran (%)', min_value=0, max_value=100, value=0)
    activity = st.number_input('Keaktifan dalam diskusi', min_value=0, max_value=100, value=0)
    assignment = st.number_input('Rata-rata nilai tugas', min_value=40, max_value=100, value=40)
    elearning = st.number_input('Keaktifan pembelajaran online', min_value=40, max_value=100, value=40)
    GPA = st.number_input('Jumlah IPK?', min_value=2.00, max_value=4.00, value=4.00)
    
    #Fungsi memprediksi
    if st.button('Prediksi Kelulusan Mahasiswa'):
        # array data input sesuai format model
        data_input = np.array([[gender, matrial_status, attendance, activity, assignment, elearning, GPA]])
    
        # Prediksi
        prediction = model.predict(data_input)[0]
    
        # Mapping kolom target
        status_mapp = {0: 'Lulus', 1: 'Tidak Lulus'}
    
        #Jika 0 maka lulus
        if prediction == 0:
            st.success(f'Status Akademik: {status_mapp[prediction]}') #tambahkan parameter prediction
        else:
             st.error(f'Status Akademik: {status_mapp[prediction]}') #selain 0 maka tidak lulus

