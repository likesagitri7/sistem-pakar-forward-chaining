import streamlit as st
import base64
import datetime
import pandas as pd
from modules.db_connection import get_data, run_query

# --- SAFEGUARD PDF (Agar tidak error jika file pdf_generator bermasalah) ---
try:
    from modules.pdf_generator import create_pdf
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ==============================================================================
# 1. FUNGSI LOAD RULES DARI DATABASE (DINAMIS - PENGGANTI HARDCODE)
# ==============================================================================
def get_rules_from_db():
    """
    Mengambil konfigurasi Rules langsung dari tabel tb_aturan.
    Sistem sekarang 100% Database Driven.
    """
    # Query mengambil detail rule dan join ke tb_penyakit untuk nama yg rapi
    query = """
    SELECT 
        a.kode_rule, 
        a.kode_penyakit, 
        p.nama_penyakit, 
        a.detail_kondisi, 
        a.kode_gejala
    FROM tb_aturan a
    JOIN tb_penyakit p ON a.kode_penyakit = p.kode_penyakit
    ORDER BY a.kode_rule ASC
    """
    try:
        df = get_data(query)
        if df.empty:
            return {}
        
        # Transformasi DataFrame ke Dictionary untuk Mesin Inferensi
        rules_dict = {}
        # Grouping data berdasarkan Kode Rule (R1, R2, dst)
        for rule_code, group in df.groupby('kode_rule'):
            first_row = group.iloc[0]
            rules_dict[rule_code] = {
                "kode_p": first_row['kode_penyakit'],
                "nama_p": first_row['nama_penyakit'],
                "detail": first_row['detail_kondisi'],
                "gejala": group['kode_gejala'].tolist() # List gejala diambil dari DB
            }
        return rules_dict
    except Exception as e:
        st.error(f"Gagal memuat Knowledge Base: {e}")
        return {}

# ==============================================================================
# 2. MESIN INFERENSI (FORWARD CHAINING)
# ==============================================================================
def forward_chaining_engine(selected_gejala_codes):
    # LOAD RULES DARI DATABASE
    RULES_BASE = get_rules_from_db()
    
    if not RULES_BASE:
        st.error("Knowledge Base Kosong atau Database Error!")
        return None

    matched_rules = []
    user_facts = set(selected_gejala_codes)
    
    for rule_id, rule_content in RULES_BASE.items():
        premis_rule = set(rule_content['gejala'])
        
        # LOGIKA STRICT (ISSUBSET): Apakah Fakta User memenuhi Rule Database?
        if premis_rule.issubset(user_facts):
            matched_rules.append({
                "rule_code": rule_id,
                "kode_penyakit": rule_content['kode_p'],
                "nama_penyakit": rule_content['nama_p'],
                "detail_spesifik": rule_content['detail'],
                "gejala_rule": rule_content['gejala']
            })
            
    if matched_rules:
        # Prioritas: Rule dengan jumlah gejala (Paling Spesifik)
        matched_rules.sort(key=lambda x: len(x['gejala_rule']), reverse=True)
        return matched_rules[0]
    return None

def show_pdf_preview(pdf_bytes):
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# ==============================================================================
# 3. UI HALAMAN KONSULTASI
# ==============================================================================
def page_consultation():
    st.markdown("<h2 style='color: #2C3E50;'>Konsultasi & Deteksi Dini</h2>", unsafe_allow_html=True)
    st.write("Silakan isi formulir pemeriksaan di bawah ini sesuai kondisi terkini.")

    # --- AMBIL DATA GEJALA DARI DB ---
    try:
        df_gejala = get_data("SELECT * FROM tb_gejala ORDER BY kategori DESC, kode_gejala ASC")
    except:
        st.error("Error Database: Pastikan tabel tb_gejala tersedia.")
        return
    
    if df_gejala.empty:
        st.warning("Data Gejala kosong.")
        return

    selected_gejala = []

    with st.form("form_konsultasi"):
        # --- A. ANAMNESIS ---
        with st.container(border=True):
            st.markdown("### 🗣️ A. Keluhan Fisik (Anamnesis)")
            st.caption("Centang apa yang Bunda rasakan saat ini:")
            
            anamnesis_data = df_gejala[df_gejala['kategori'] == 'Anamnesis']
            if not anamnesis_data.empty:
                cols = st.columns(2) 
                for index, row in anamnesis_data.iterrows():
                    # Handle teks pertanyaan user
                    teks = row.get('pertanyaan_user', row['nama_gejala'])
                    if not teks: teks = row['nama_gejala']
                    
                    with cols[index % 2]:
                        if st.checkbox(teks, key=f"chk_{row['kode_gejala']}"):
                            selected_gejala.append(row['kode_gejala'])
            else:
                st.info("Data Anamnesis kosong.")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- B. KLINIS ---
        with st.container(border=True):
            st.markdown("### 🩺 B. Tanda Klinis & Hasil Lab")
            st.caption("Isi berdasarkan hasil pemeriksaan Bidan/Dokter (Jika ada):")
            
            klinis_data = df_gejala[df_gejala['kategori'] == 'Klinis']
            if not klinis_data.empty:
                cols2 = st.columns(2)
                for index, row in klinis_data.iterrows():
                    label = f"{row['nama_gejala']} ({row['kode_gejala']})"
                    with cols2[index % 2]:
                        if st.checkbox(label, key=f"chk_{row['kode_gejala']}"):
                            selected_gejala.append(row['kode_gejala'])

        st.markdown("---")
        submit_diag = st.form_submit_button("🔍 PROSES DIAGNOSA", type="primary", use_container_width=True)

    if submit_diag:
        if not selected_gejala:
            st.error("Harap pilih minimal satu gejala.")
        else:
            # 1. SIAPKAN DATA USER (Untuk PDF)
            user_id = st.session_state.get('user_id')
            user_name = st.session_state.get('user_name', 'Pasien Umum')
            user_umur = "-"
            user_alamat = "-"
            
            if user_id:
                try:
                    df_user = get_data(f"SELECT usia, alamat FROM tb_user WHERE id_user = '{user_id}'")
                    if not df_user.empty:
                        user_umur = str(df_user.iloc[0]['usia'])
                        user_alamat = str(df_user.iloc[0]['alamat'])
                except: pass

            # 2. LIST NAMA GEJALA
            nama_gejala_user = df_gejala[df_gejala['kode_gejala'].isin(selected_gejala)]['nama_gejala'].tolist()

            # 3. JALANKAN INFERENCE ENGINE
            with st.spinner("Mengambil Rule dari Database & Menganalisa..."):
                hasil = forward_chaining_engine(selected_gejala)
                st.markdown("<br>", unsafe_allow_html=True)

                # --- SKENARIO 1: TERDETEKSI (MATCH RULE) ---
                if hasil:
                    kd_penyakit = hasil['kode_penyakit']
                    nm_penyakit = hasil['nama_penyakit']
                    detail_ket = hasil['detail_spesifik']
                    
                    # Ambil Solusi & Definisi
                    df_sol = get_data(f"SELECT solusi, definisi FROM tb_penyakit WHERE kode_penyakit='{kd_penyakit}'")
                    solusi = df_sol['solusi'].iloc[0] if not df_sol.empty else "Segera hubungi dokter."
                    definisi = df_sol['definisi'].iloc[0] if not df_sol.empty else "-"

                    # UI CARD
                    st.markdown(f"""
                    <div style="background-color: #FFEBEE; padding: 25px; border-radius: 15px; border-left: 8px solid #D32F2F; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <div style="margin-bottom: 5px;">
                            <span style="background-color: #D32F2F; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                                RULE TERDETEKSI: {hasil['rule_code']}
                            </span>
                        </div>
                        <h1 style="color: #B71C1C; margin: 0; font-size: 28px; font-weight: 800;">{nm_penyakit}</h1>
                        <p style="font-size: 16px; color: #424242; margin-top: 5px;"><em>"Kondisi: {detail_ket}"</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container(border=True):
                        st.markdown(f"**Apa itu {nm_penyakit}?**\n{definisi}")
                        st.divider()
                        st.markdown(f"**💡 Saran Penanganan:**\n{solusi}")

                    # [REVISI BAGIAN INI] SIMPAN RIWAYAT (MENYIMPAN KODE PENYAKIT)
                    try:
                        tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        diag_str = f"{nm_penyakit} ({detail_ket})" # Hanya simpan nama untuk display history
                        gejala_str = ", ".join(selected_gejala)
                        
                        # Simpan ID User, Kode Penyakit (FK), dll
                        q = """
                            INSERT INTO tb_riwayat 
                            (id_user, kode_penyakit, tanggal_konsultasi, hasil_diagnosa, gejala_terpilih, saran_penanganan) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        run_query(q, (user_id, kd_penyakit, tgl, diag_str, gejala_str, solusi))
                    except Exception as e:
                        print(f"Error Save: {e}")

                    # PDF GENERATOR
                    if PDF_AVAILABLE:
                        status_warna = "danger" if "Berat" in nm_penyakit or "Eklamsia" in nm_penyakit else "warning"
                        hasil_full_pdf = f"{nm_penyakit} ({detail_ket})"

                        try:
                            pdf_data = create_pdf(
                                nama_pasien=user_name,
                                umur=user_umur,
                                alamat=user_alamat,
                                hasil_diagnosa=hasil_full_pdf,
                                gejala_list=nama_gejala_user,
                                solusi=solusi,
                                status_warna=status_warna
                            )
                            
                            with st.expander("👁️ Klik untuk Preview Surat Rujukan", expanded=False):
                                show_pdf_preview(pdf_data)
                                
                            st.download_button("📄 Download Laporan PDF (Resmi)", data=pdf_data, file_name=f"Hasil_{user_name}.pdf", mime="application/pdf")
                        except Exception as e:
                            st.error(f"Gagal PDF: {e}")

                # --- SKENARIO 2: OBSERVASI (TIDAK MATCH RULE) ---
                else:
                    st.warning("⚠️ HASIL ANALISA: INDIKASI GEJALA (BELUM SPESIFIK)")
                    st.write("**Gejala Terdeteksi:**")
                    for n in nama_gejala_user:
                        st.markdown(f"- 🔴 {n}")
                    
                    st.info("**Diagnosa spesifik tidak tegak** karena kombinasi gejala belum memenuhi aturan medis lengkap. Sistem mencatat ini sebagai keluhan/observasi.")
                    
                    saran_umum = "1. Istirahat yang cukup dan kurangi aktivitas berat.\n2. Pantau terus jika muncul gejala baru dalam 24 jam.\n3. Konsultasikan keluhan ini ke Bidan/Dokter untuk pemeriksaan fisik."
                    
                    with st.container(border=True):
                        st.markdown(f"**💡 Saran:**\n{saran_umum}")
                    
                    # [REVISI BAGIAN INI] Simpan Riwayat Observasi (Kode Penyakit = NULL)
                    try:
                        tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        gejala_str = ", ".join(selected_gejala)
                        q = """
                            INSERT INTO tb_riwayat 
                            (id_user, kode_penyakit, tanggal_konsultasi, hasil_diagnosa, gejala_terpilih, saran_penanganan) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        # Parameter ke-2 adalah None agar masuk sebagai NULL di database
                        run_query(q, (user_id, None, tgl, "Indikasi Gejala (Observasi)", gejala_str, saran_umum))
                    except: pass

                    if PDF_AVAILABLE:
                        try:
                            pdf_data_warning = create_pdf(
                                nama_pasien=user_name,
                                umur=user_umur,
                                alamat=user_alamat,
                                hasil_diagnosa="INDIKASI GEJALA (Perlu Observasi)",
                                gejala_list=nama_gejala_user,
                                solusi=saran_umum,
                                status_warna="warning"
                            )
                            st.download_button("📄 Download Laporan Keluhan", data=pdf_data_warning, file_name="Keluhan.pdf", mime="application/pdf")
                        except: pass