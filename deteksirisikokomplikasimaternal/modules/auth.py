import streamlit as st
import time
from modules.db_connection import run_query, get_data

def page_register():
    # --- [BAGIAN BARU 1] CSS UNTUK TOMBOL MODERN ---
    st.markdown("""
        <style>
        /* Mengubah tombol Secondary jadi Lonjong (Pill) & Teal */
        button[kind="secondary"] {
            border-radius: 50px !important;
            border: 1px solid #006064 !important;
            color: #006064 !important;
            transition: all 0.3s ease !important;
        }
        button[kind="secondary"]:hover {
            background-color: #E0F2F1 !important;
            transform: scale(1.02);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- [BAGIAN BARU 2] LAYOUT TOMBOL KEMBALI (AGAR RAPI DI KIRI) ---
    c_back, c_space = st.columns([1, 5]) 
    with c_back:
        if st.button("⬅ Back", type="secondary", use_container_width=True):
            st.session_state['menu_selection'] = "Beranda"
            st.rerun()

    # Inisialisasi ID Reset Form
    if 'form_reset_id' not in st.session_state:
        st.session_state['form_reset_id'] = 0

    # Layout Centering (Agar form tidak terlalu lebar)
    c1, c2, c3 = st.columns([1, 3, 1]) # Kolom tengah (c2) lebih lebar (skala 3)

    with c2:
        # Header Modern
        st.markdown("""
            <div style='text-align: center; margin-bottom: 30px;'>
                <h2 style='color: #006064; margin-bottom: 10px;'>Selamat Datang, Bunda! ✨</h2>
                    <p style='color: #546E7A; font-size: 15px; line-height: 1.6;'>
                    Bergabunglah dengan layanan RSUD Solok Selatan untuk pemantauan kehamilan yang lebih baik.
                </p>
                <p style='color: #546E7A; font-size: 15px; line-height: 0.4;'>
                    Mari lengkapi data diri di bawah ini untuk mulai memantau kesehatan Bunda dan calon Buah Hati tercinta bersama kami.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Notifikasi Sukses
        if st.session_state.get('registrasi_sukses'):
            st.success("✅ Akun berhasil dibuat! Silakan Login melalui menu di Sidebar.")
            st.session_state['registrasi_sukses'] = False

        reset_id = st.session_state['form_reset_id']

        # Form dalam Card Style
        with st.form("form_register"):
            st.markdown("### 📝 Data Akun")
            # Baris 1: Username & Password
            col_a, col_b = st.columns(2)
            with col_a:
                username = st.text_input("Username", placeholder="Contoh: bunda_siti", key=f"reg_user_{reset_id}").strip()
            with col_b:
                password = st.text_input("Password", type="password", placeholder="Minimal 6 karakter", key=f"reg_pass_{reset_id}").strip()
            
            st.markdown("---")
            st.markdown("### 🤰 Data Pribadi")
            
            # Nama Lengkap (Full Width)
            nama = st.text_input("Nama Lengkap", placeholder="Sesuai KTP", key=f"reg_nama_{reset_id}").strip()
            
            # Baris 2: Usia & HP
            col_c, col_d = st.columns(2)
            with col_c:
                usia = st.number_input("Usia (Tahun)", min_value=15, max_value=60, value=25, key=f"reg_usia_{reset_id}")
            with col_d:
                # Ingat: Kolom database kamu 'hp'
                hp = st.text_input("Nomor HP / WhatsApp", placeholder="0812xxxx", key=f"reg_hp_{reset_id}").strip()
                
            # Alamat
            alamat = st.text_area("Alamat Domisili", placeholder="Nama Jalan, Jorong, Nagari...", height=100, key=f"reg_alamat_{reset_id}").strip()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tombol Submit (Full Width & Besar)
            submit = st.form_submit_button("Daftar Sekarang", type="primary", use_container_width=True)

        # LOGIKA PROSES (REVISI: CEK KE DUA TABEL)
        if submit:
            # 1. Validasi Input Kosong & Spasi
            if not nama or not username or not password or not alamat:
                st.warning("⚠️ Mohon lengkapi semua kolom isian.")
                return
            
            if " " in username:
                st.warning("⚠️ Username tidak boleh mengandung spasi!")
                return

            # 2. Cek Username (DIREVISI: Cek di tb_user DAN tb_admin)
            try:
                cek_user = get_data(f"SELECT username FROM tb_user WHERE username = '{username}'")
                cek_admin = get_data(f"SELECT username FROM tb_admin WHERE username = '{username}'")
                
                if not cek_user.empty or not cek_admin.empty:
                    st.error(f"❌ Username '{username}' sudah digunakan. Silakan pilih yang lain.")
                    return
                
                # 3. Simpan ke Database
                # Pastikan urutan kolom sesuai tabel database kamu: (username, password, nama, usia, alamat, hp)
                
                query = """
                INSERT INTO tb_user (username, password, nama_lengkap, usia, alamat, hp)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (username, password, nama, usia, alamat, hp)
                
                run_query(query, values)
                
                # Reset Form & Notifikasi
                st.session_state['registrasi_sukses'] = True
                st.session_state['form_reset_id'] += 1 
                st.success("✅ Registrasi Berhasil! Silakan Login.") # Kotak hijau statis
                st.toast("Akun telah dibuat!", icon='🎉')          # Notifikasi melayang di pojok kanan (mirip HP)
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"Terjadi kesalahan sistem: {e}")
                st.info("Tips: Periksa apakah ada kolom database yang tidak sesuai (misal: 'hp' vs 'hp').")