import streamlit as st
import time
import pandas as pd
from modules.db_connection import run_query, get_data

def page_profile():
    # Header
    st.markdown("""
    <div style="background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #E91E63; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <h3 style="margin: 0; color: #E91E63;">👤 Profil Saya</h3>
        <p style="margin: 5px 0 0 0; color: #78909C; font-size: 14px;">Kelola data pribadi dan keamanan akun Bunda.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Ambil Data User Saat Ini
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("Sesi tidak valid. Silakan login ulang.")
        return

    try:
        # Ambil data terbaru dari database
        df = get_data(f"SELECT * FROM tb_user WHERE id_user='{user_id}'")
        if df.empty:
            st.error("Data pengguna tidak ditemukan.")
            return
        
        user_data = df.iloc[0]
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return

    # 2. Form Edit Profil
    with st.container(border=True):
        st.markdown("#### 📝 Edit Data Diri")
        
        with st.form("form_update_profile"):
            # Username (Disabled/Tidak bisa diubah agar ID konsisten)
            st.text_input("Username", value=user_data['username'], disabled=True, help="Username tidak dapat diubah.")
            
            c1, c2 = st.columns(2)
            with c1:
                nama_baru = st.text_input("Nama Lengkap", value=user_data['nama_lengkap'])
                hp_baru = st.text_input("No. Handphone", value=str(user_data.get('hp', '')))
            with c2:
                pass_baru = st.text_input("Password Baru", type="password", placeholder="Isi hanya jika ingin mengganti password")
                alamat_baru = st.text_area("Alamat Lengkap", value=user_data.get('alamat', ''), height=100)

            st.markdown("---")
            btn_save = st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True)

            if btn_save:
                if not nama_baru:
                    st.warning("Nama Lengkap wajib diisi!")
                else:
                    try:
                        # Cek apakah password diubah
                        if pass_baru:
                            q = "UPDATE tb_user SET nama_lengkap=%s, password=%s, hp=%s, alamat=%s WHERE id_user=%s"
                            p = (nama_baru, pass_baru, hp_baru, alamat_baru, user_id)
                        else:
                            q = "UPDATE tb_user SET nama_lengkap=%s, hp=%s, alamat=%s WHERE id_user=%s"
                            p = (nama_baru, hp_baru, alamat_baru, user_id)
                        
                        run_query(q, p)
                        
                        # Update nama di sesi aplikasi agar header langsung berubah
                        st.session_state['user_name'] = nama_baru
                        
                        st.toast("Profil berhasil diperbarui!", icon="✅")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Gagal update profil: {e}")