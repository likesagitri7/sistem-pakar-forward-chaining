import streamlit as st
import pandas as pd
import base64
from modules.db_connection import get_data

# IMPORT MODUL PDF
try:
    from modules.pdf_generator import create_pdf
except ImportError:
    pass

def page_history():
    st.markdown("<h2 style='color: #2C3E50;'>Riwayat Pemeriksaan</h2>", unsafe_allow_html=True)
    
    if 'user_id' not in st.session_state:
        st.warning("⚠️ Sesi habis. Silakan Login kembali.")
        return

    user_id = st.session_state['user_id']
    user_name = st.session_state.get('user_name', 'Pasien')

    # ==========================================================================
    # 1. PERSIAPAN KAMUS PENERJEMAH (KODE -> NAMA)
    # Kita ambil dulu master gejala agar bisa mengubah "G01" jadi "Darah Tinggi"
    # ==========================================================================
    try:
        df_master_gejala = get_data("SELECT kode_gejala, nama_gejala FROM tb_gejala")
        # Buat Dictionary: {'G01': 'Tekanan Darah Tinggi...', 'G02': 'Protein...'}
        # Ini teknik lookup tercepat di Python
        map_gejala = dict(zip(df_master_gejala['kode_gejala'], df_master_gejala['nama_gejala']))
    except:
        map_gejala = {}

    # ==========================================================================
    # 2. QUERY DATABASE RIWAYAT
    # ==========================================================================
    query = f"""
        SELECT 
            id_riwayat,
            tanggal_konsultasi,
            hasil_diagnosa,
            gejala_terpilih,
            saran_penanganan
        FROM tb_riwayat 
        WHERE id_user = {user_id}
        ORDER BY tanggal_konsultasi DESC
    """
    
    try:
        df_riwayat = get_data(query)
        
        if df_riwayat.empty:
            st.info("📂 Belum ada data riwayat pemeriksaan.")
        else:
            for index, row in df_riwayat.iterrows():
                tgl = row['tanggal_konsultasi']
                diagnosa = row['hasil_diagnosa']
                saran = row['saran_penanganan'] 
                if not saran or str(saran) == 'None':
                    saran = "Tidak ada saran spesifik tersimpan."
                
                # Gejala Raw (Masih Kode: "G01, G02, G03")
                gejala_raw = row['gejala_terpilih']
                
                # ==============================================================
                # 3. LOGIKA PENERJEMAHAN KODE -> NAMA (FIX DISINI)
                # ==============================================================
                list_nama_gejala = []
                if gejala_raw and str(gejala_raw) != 'None':
                    # Pecah string "G01, G02" menjadi list ['G01', 'G02']
                    list_kode = str(gejala_raw).split(", ")
                    
                    # Loop setiap kode, cari namanya di Kamus (map_gejala)
                    for kode in list_kode:
                        # Ambil nama gejala, jika tidak ada kembalikan kodenya saja
                        nama = map_gejala.get(kode, kode) 
                        list_nama_gejala.append(nama)
                
                # Gabungkan kembali untuk tampilan UI (Opsional, biar rapi di expander)
                tampilan_gejala_ui = "\n".join([f"- {x}" for x in list_nama_gejala])

                # ==============================================================
                # 4. TAMPILAN KARTU
                # ==============================================================
                with st.container(border=True):
                    c1, c2 = st.columns([5, 2])
                    
                    with c1:
                        st.markdown(f"##### 🗓️ {tgl}")
                        
                        if "Berat" in str(diagnosa) or "Eklamsia" in str(diagnosa):
                            st.error(f"**Diagnosa:** {diagnosa}")
                        elif "Indikasi" in str(diagnosa) or "Observasi" in str(diagnosa):
                            st.warning(f"**Diagnosa:** {diagnosa}")
                        else:
                            st.success(f"**Diagnosa:** {diagnosa}")
                            
                        with st.expander("📝 Lihat Detail & Saran"):
                            st.markdown("**Fakta Gejala:**")
                            # Tampilkan Nama Gejala (Bukan Kode Lagi)
                            st.text(tampilan_gejala_ui) 
                            st.divider()
                            st.markdown(f"**Saran Medis:**\n{saran}")
                    
                    with c2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # ======================================================
                        # 5. GENERATE PDF DENGAN NAMA LENGKAP
                        # ======================================================
                        try:
                            if "Berat" in str(diagnosa) or "Eklamsia" in str(diagnosa):
                                status_warna = "danger"
                            elif "Indikasi" in str(diagnosa) or "Observasi" in str(diagnosa):
                                status_warna = "warning"
                            else:
                                status_warna = "normal"
                            
                            # PENTING: Kirim list_nama_gejala (Darah Tinggi), BUKAN list_kode (G01)
                            pdf_bytes = create_pdf(
                                nama_pasien=user_name,
                                umur="-", 
                                alamat="-",
                                hasil_diagnosa=diagnosa,
                                gejala_list=list_nama_gejala, # <-- SUDAH DIPERBAIKI
                                solusi=saran,
                                status_warna=status_warna
                            )
                            
                            b64 = base64.b64encode(pdf_bytes).decode()
                            href = f'''
                            <a href="data:application/octet-stream;base64,{b64}" download="Riwayat_{tgl}.pdf" style="text-decoration:none;">
                                <div style="
                                    background: linear-gradient(90deg, #006064 0%, #004D40 100%); 
                                    color: white; 
                                    padding: 8px; 
                                    border-radius: 5px; 
                                    text-align: center; 
                                    font-size: 13px;
                                    font-weight: bold;
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                                ">
                                    📄 CETAK ULANG
                                </div>
                            </a>
                            '''
                            st.markdown(href, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.caption("PDF Error")

            st.caption(f"Menampilkan {len(df_riwayat)} riwayat pemeriksaan.")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan koneksi database: {e}")