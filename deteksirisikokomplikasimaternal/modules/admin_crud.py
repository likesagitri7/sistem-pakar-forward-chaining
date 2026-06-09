import streamlit as st
import pandas as pd
import time
import altair as alt
from fpdf import FPDF
from datetime import datetime
from modules.db_connection import run_query, get_data

# ==============================================================================
# HELPER: PDF GENERATOR (FIX UNICODE SYMBOLS)
# ==============================================================================
class MedicalReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16); self.set_text_color(0, 0, 0); self.cell(0, 8, 'RSUD KABUPATEN SOLOK SELATAN', 0, 1, 'C')
        self.set_font('Arial', '', 10); self.set_text_color(0, 0, 0); self.cell(0, 5, 'Jalan Raya Km. 1, Nagari Koto Baru, Kec. Sungai Pagu, Solok Selatan', 0, 1, 'C'); self.cell(0, 5, 'Telp: (0755) 70462 | Email: rsud.solsel@yahoo.co.id', 0, 1, 'C')
        self.ln(5); self.set_draw_color(0, 0, 0); self.set_line_width(0.5); self.line(10, self.get_y(), 285, self.get_y()); self.set_line_width(0.1); self.line(10, self.get_y()+1, 285, self.get_y()+1); self.ln(8)
        self.set_font('Arial', 'B', 12); self.cell(0, 6, 'LAPORAN RIWAYAT KONSULTASI & DIAGNOSA', 0, 1, 'C'); self.ln(5)
    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8); self.set_text_color(128); self.cell(0, 10, f'Dicetak pada: {datetime.now().strftime("%d/%m/%Y %H:%M")} | Halaman {self.page_no()}', 0, 0, 'R')

def header_section(emoji, title, subtitle):
    st.markdown(f"""<div style="background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #006064; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;"><h3 style="margin: 0; color: #006064; display: flex; align-items: center;"><span style="margin-right: 10px;">{emoji}</span> {title}</h3><p style="margin: 5px 0 0 0; color: #78909C; font-size: 14px;">{subtitle}</p></div>""", unsafe_allow_html=True)

# 1. DASHBOARD
def page_dashboard_admin():
    try: total_pasien = get_data("SELECT COUNT(*) as total FROM tb_user").iloc[0]['total']
    except: total_pasien = 0
    try: total_konsul = get_data("SELECT COUNT(*) as total FROM tb_riwayat").iloc[0]['total']
    except: total_konsul = 0
    try: total_penyakit = get_data("SELECT COUNT(*) as total FROM tb_penyakit").iloc[0]['total']
    except: total_penyakit = 0
    try: total_gejala = get_data("SELECT COUNT(*) as total FROM tb_gejala").iloc[0]['total']
    except: total_gejala = 0

    st.markdown("""<div style="background: linear-gradient(90deg, #006064 0%, #00838F 100%); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"><div><h2 style="margin:0; color:white; font-size: 24px;">Hallo, Administrator! 👋</h2><p style="margin:5px 0 0 0; color:#E0F2F1;">Selamat datang di Panel Sistem Pakar Maternal.</p></div><div style="font-size: 3rem;">📊</div></div>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card" style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; text-align: center;"><div style="font-size: 2rem; color: #006064; font-weight: 800;">{total_pasien}</div><div style="font-size: 0.9rem; color: #666; font-weight: 600;">PASIEN</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card" style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; text-align: center;"><div style="font-size: 2rem; color: #006064; font-weight: 800;">{total_konsul}</div><div style="font-size: 0.9rem; color: #666; font-weight: 600;">KONSULTASI</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card" style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; text-align: center;"><div style="font-size: 2rem; color: #006064; font-weight: 800;">{total_penyakit}</div><div style="font-size: 0.9rem; color: #666; font-weight: 600;">PENYAKIT</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card" style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; text-align: center;"><div style="font-size: 2rem; color: #006064; font-weight: 800;">{total_gejala}</div><div style="font-size: 0.9rem; color: #666; font-weight: 600;">GEJALA</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📊 Tren Partisipasi")
        g1, g2 = st.columns([2, 1])
        with g1:
            try:
                query_trend = "SELECT DATE(tanggal_konsultasi) as tanggal, COUNT(*) as jumlah FROM tb_riwayat GROUP BY DATE(tanggal_konsultasi) ORDER BY tanggal ASC LIMIT 14"
                df_trend = get_data(query_trend)
                if not df_trend.empty:
                    # 1. Format tanggal langsung di DataFrame menjadi Teks/String ('01 Feb', '02 Feb', dll)
                    df_trend['tanggal_str'] = pd.to_datetime(df_trend['tanggal']).dt.strftime('%d %b')
                    
                    # 2. Buat grafik menggunakan kolom yang sudah diformat
                    chart = alt.Chart(df_trend).mark_bar(
                        cornerRadiusTopLeft=10, cornerRadiusTopRight=10, color="#006064"
                    ).encode(
                        # Hapus format='%d %b' karena datanya sudah berwujud string
                        x=alt.X('tanggal_str:O', axis=alt.Axis(title='Tanggal', labelAngle=0)), 
                        y=alt.Y('jumlah:Q', axis=alt.Axis(title='Jumlah Pasien', tickMinStep=1)), 
                        tooltip=[alt.Tooltip('tanggal_str:O', title='Tanggal'), alt.Tooltip('jumlah:Q', title='Total')]
                    ).properties(height=320).configure_axis(grid=False).configure_view(strokeWidth=0)
                    
                    st.altair_chart(chart, use_container_width=True)
                else: st.info("Belum ada data grafik.")
            except: st.warning("Grafik belum tersedia.")
        with g2:
            try:
                query_pie = "SELECT hasil_diagnosa, COUNT(*) as jumlah FROM tb_riwayat GROUP BY hasil_diagnosa ORDER BY jumlah DESC LIMIT 5"
                df_pie = get_data(query_pie)
                if not df_pie.empty: st.dataframe(df_pie, hide_index=True, use_container_width=True, column_config={"hasil_diagnosa": st.column_config.TextColumn("Top Diagnosa"), "jumlah": st.column_config.ProgressColumn("Total", format="%d", min_value=0, max_value=int(df_pie['jumlah'].max()))})
                else: st.info("Belum ada data.")
            except: st.warning("Statistik belum siap.")

# 2. PENGGUNA (TAB USER & ADMIN - SESUAI GAMBAR)
def page_users():
    header_section("👥", "Manajemen Pengguna", "Kelola akun Admin dan User (Ibu Hamil).")
    # Inisialisasi State (Defensive Coding)
    if 'reset_user_add' not in st.session_state: st.session_state['reset_user_add'] = 0
    if 'reset_admin_add' not in st.session_state: st.session_state['reset_admin_add'] = 0
    
    # TAB UTAMA
    tab_pasien, tab_admin = st.tabs(["User (Ibu Hamil)", "Admin"])

    # --- TAB 1: USER ---
    with tab_pasien:
        try: df_user = get_data("SELECT * FROM tb_user ORDER BY id_user DESC")
        except: df_user = pd.DataFrame()
        with st.container(border=True):
            st.markdown("##### 📋 Daftar User Terdaftar")
            if not df_user.empty: st.dataframe(df_user.drop(columns=['password'], errors='ignore'), use_container_width=True, hide_index=True)
            else: st.info("Belum ada data user.")
        
        c1, c2, c3 = st.columns(3)
        
        # ADD USER [UPDATE: Ada Input Usia]
        with st.expander("➕ Tambah User"):
            with st.form("add_u"):
                # Gunakan key dinamis (rid) agar bisa di-reset
                rid = st.session_state['reset_user_add']
                
                col_a, col_b = st.columns(2)
                with col_a:
                    un = st.text_input("Nama Lengkap", key=f"u_nm_{rid}")
                    uu = st.text_input("Username", key=f"u_us_{rid}")
                    up = st.text_input("Password", type="password", key=f"u_pw_{rid}")
                with col_b:
                    u_usia = st.number_input("Usia (Tahun)", min_value=15, max_value=60, value=25, key=f"u_ag_{rid}")
                    uh = st.text_input("No HP", key=f"u_hp_{rid}")
                    ua = st.text_area("Alamat", key=f"u_al_{rid}")
                
                if st.form_submit_button("Simpan", type="primary"):
                    try: 
                        # Query Insert
                        run_query("INSERT INTO tb_user (nama_lengkap, username, password, hp, alamat, usia) VALUES (%s, %s, %s, %s, %s, %s)", (un, uu, up, uh, ua, u_usia))
                        
                        # Increment ID Reset agar form bersih
                        st.session_state['reset_user_add'] += 1
                        
                        st.toast("Sukses Menyimpan Data!", icon='✅')
                        time.sleep(1)
                        st.rerun() # Refresh halaman
                    except Exception as e: st.error(f"Gagal: {e}")
        # EDIT USER [UPDATE: Ada Edit Usia]
        with st.expander("✏️ Edit User"):
            if not df_user.empty:
                su = st.selectbox("Pilih User:", df_user['username'].tolist(), key="ed_u_sel")
                du = df_user[df_user['username']==su].iloc[0]
                with st.form("ed_u"):
                    st.text_input("ID", value=du['id_user'], disabled=True)
                    
                    c_edit1, c_edit2 = st.columns(2)
                    with c_edit1:
                        en = st.text_input("Nama", value=du['nama_lengkap'])
                        eu = st.text_input("Username", value=du['username'])
                        ep = st.text_input("Pass Baru", type="password", placeholder="Isi jika ingin ubah")
                    with c_edit2:
                        usia_val = int(du['usia']) if pd.notna(du['usia']) else 25
                        e_usia = st.number_input("Usia", value=usia_val, min_value=15, max_value=60)
                        eh = st.text_input("HP", value=du.get('hp','')) 
                        ea = st.text_area("Alamat", value=du.get('alamat',''))
                    
                    if st.form_submit_button("Update"):
                        # FIX: Konversi numpy.int64 ke int Python biasa
                        uid = int(du['id_user']) 
                        
                        if ep: run_query("UPDATE tb_user SET nama_lengkap=%s, username=%s, password=%s, hp=%s, alamat=%s, usia=%s WHERE id_user=%s", (en, eu, ep, eh, ea, e_usia, uid))
                        else: run_query("UPDATE tb_user SET nama_lengkap=%s, username=%s, hp=%s, alamat=%s, usia=%s WHERE id_user=%s", (en, eu, eh, ea, e_usia, uid))
                        st.toast("Updated", icon='✅'); time.sleep(1); st.rerun()
        with st.expander("🗑️ Hapus User"):
            if not df_user.empty:
                del_u = st.selectbox("Hapus User:", df_user['username'].tolist(), key="del_u_sel")
                if st.button("Hapus Permanen", type="primary", key="btn_del_u"):
                    uid = df_user[df_user['username']==del_u]['id_user'].iloc[0]
                    run_query("DELETE FROM tb_riwayat WHERE id_user=%s", (str(uid),)); run_query("DELETE FROM tb_user WHERE id_user=%s", (str(uid),)); st.toast("Terhapus", icon='🗑️'); time.sleep(1); st.rerun()

    # --- TAB 2: ADMIN ---
    with tab_admin:
        try: df_admin = get_data("SELECT * FROM tb_admin ORDER BY id_admin ASC")
        except: df_admin = pd.DataFrame()
        with st.container(border=True):
            st.markdown("##### 🛡️ Daftar Admin")
            if not df_admin.empty: st.dataframe(df_admin.drop(columns=['password'], errors='ignore'), use_container_width=True, hide_index=True)
            else: st.info("Belum ada data.")
        # ADD ADMIN - [FIX: Auto Reset & Error Message]
        with st.expander("➕ Tambah Admin"):
            with st.form("add_a"):
                rid_a = st.session_state['reset_admin_add']
                
                an = st.text_input("Nama", key=f"a_nm_{rid_a}")
                au = st.text_input("Username", key=f"a_us_{rid_a}")
                ap = st.text_input("Password", type="password", key=f"a_pw_{rid_a}")
                
                if st.form_submit_button("Simpan", type="primary"):
                    if an and au and ap:
                        try: 
                            run_query("INSERT INTO tb_admin (nama_lengkap, username, password) VALUES (%s, %s, %s)", (an, au, ap))
                            st.session_state['reset_admin_add'] += 1
                            st.toast("Sukses Menyimpan Admin!", icon='✅'); time.sleep(1); st.rerun()
                        except Exception as e: st.error(f"Gagal: {e}")
                    else:
                        st.warning("Mohon lengkapi semua data!")
        # EDIT ADMIN - [FIX: Integer Casting]
        with st.expander("✏️ Edit Admin"):
            if not df_admin.empty:
                sa = st.selectbox("Pilih Admin:", df_admin['username'].tolist(), key="ed_a_sel")
                da = df_admin[df_admin['username']==sa].iloc[0]
                with st.form("ed_a"):
                    st.text_input("ID", value=da['id_admin'], disabled=True)
                    en = st.text_input("Nama", value=da['nama_lengkap']); eu = st.text_input("Username", value=da['username']); ep = st.text_input("Pass Baru", type="password")
                    if st.form_submit_button("Update"):
                        try:
                            aid = int(da['id_admin']) # FIX: Int Cast
                            if ep: run_query("UPDATE tb_admin SET nama_lengkap=%s, username=%s, password=%s WHERE id_admin=%s", (en, eu, ep, aid))
                            else: run_query("UPDATE tb_admin SET nama_lengkap=%s, username=%s WHERE id_admin=%s", (en, eu, aid))
                            st.toast("Updated", icon='✅'); time.sleep(1); st.rerun()
                        except Exception as e: st.error(f"Gagal: {e}")
        # DELETE ADMIN - [FIX: Integer Casting]
        with st.expander("🗑️ Hapus Admin"):
            if not df_admin.empty:
                del_a = st.selectbox("Hapus Admin:", df_admin['username'].tolist(), key="del_a_sel")
                if st.button("Hapus Permanen", type="primary", key="btn_del_a"):
                    if del_a == st.session_state.get('username'): st.error("Tidak bisa hapus akun sendiri!")
                    else:
                        aid = int(df_admin[df_admin['username']==del_a]['id_admin'].iloc[0]) # FIX: Int Cast
                        run_query("DELETE FROM tb_admin WHERE id_admin=%s", (aid,))
                        st.toast("Terhapus", icon='🗑️'); time.sleep(1); st.rerun()

# 3. GEJALA
def page_gejala():
    header_section("🌡️", "Manajemen Gejala", "Kelola daftar gejala klinis.")
    if 'reset_gejala' not in st.session_state: st.session_state['reset_gejala'] = 0
    tab1, tab2, tab3 = st.tabs(["📋 Data Tabel", "➕ Tambah Baru", "✏️ Edit / Hapus"])
    with tab1:
        with st.container(border=True):
            df = get_data("SELECT * FROM tb_gejala ORDER BY kode_gejala ASC")
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True); st.caption(f"Total Gejala: {len(df)}")
            else: st.info("Kosong.")
    with tab2:
        with st.container(border=True):
            with st.form("add_gejala"):
                rid = st.session_state['reset_gejala']; c1, c2 = st.columns([1, 4])
                with c1: kode = st.text_input("Kode", placeholder="G01", key=f"gk{rid}")
                with c2: nama = st.text_input("Nama Gejala", placeholder="Contoh: Demam", key=f"gn{rid}")
                c3, c4 = st.columns([2, 1])
                with c3: tanya = st.text_input("Pernyataan User", key=f"gq{rid}")
                with c4: kat = st.selectbox("Kategori", ["Anamnesis", "Klinis"], key=f"gkt{rid}")
                st.markdown("---")
                if st.form_submit_button("Simpan Data", type="primary", use_container_width=True):
                    try:
                        # FIX: Sebutkan nama kolom secara eksplisit agar aman
                        q = "INSERT INTO tb_gejala (kode_gejala, nama_gejala, pertanyaan_user, kategori) VALUES (%s, %s, %s, %s)"
                        run_query(q, (kode, nama, tanya, kat))
                        
                        st.toast("Berhasil!", icon='✅')
                        st.session_state['reset_gejala'] += 1
                        time.sleep(0.5); st.rerun()
                    except Exception as e:
                        # FIX: Tampilkan error asli biar tau (misal Duplicate Entry)
                        st.error(f"Gagal: {e}") 
    with tab3:
        if not df.empty:
            with st.container(border=True):
                pilih = st.selectbox("Pilih Gejala:", df['kode_gejala'].tolist())
                if pilih:
                    dt = df[df['kode_gejala']==pilih].iloc[0]
                    with st.form("edit_g"):
                        nn = st.text_input("Nama Gejala", value=dt['nama_gejala']); nq = st.text_input("Pernyataan User", value=dt['pertanyaan_user']); nk = st.selectbox("Kategori", ["Anamnesis", "Klinis"], index=(0 if dt['kategori']=="Anamnesis" else 1))
                        c_up, c_del = st.columns(2)
                        if c_up.form_submit_button("Update", type="primary"): run_query("UPDATE tb_gejala SET nama_gejala=%s, pertanyaan_user=%s, kategori=%s WHERE kode_gejala=%s", (nn, nq, nk, pilih)); st.toast("Updated!", icon='✅'); time.sleep(0.5); st.rerun()
                        if c_del.form_submit_button("Hapus", type="secondary"): run_query("DELETE FROM tb_aturan WHERE kode_gejala=%s", (pilih,)); run_query("DELETE FROM tb_gejala WHERE kode_gejala=%s", (pilih,)); st.toast("Terhapus!", icon='🗑️'); time.sleep(0.5); st.rerun()

# 4. PENYAKIT
def page_penyakit():
    header_section("🦠", "Manajemen Penyakit", "Kelola data penyakit.")
    if 'reset_penyakit' not in st.session_state: st.session_state['reset_penyakit'] = 0
    
    tab1, tab2, tab3 = st.tabs(["📋 Data Tabel", "➕ Tambah Baru", "✏️ Edit / Hapus"])
    with tab1:
        with st.container(border=True):
            df = get_data("SELECT * FROM tb_penyakit ORDER BY kode_penyakit ASC")
            if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("Kosong.")
    with tab2:
        with st.container(border=True):
            with st.form("add_p"):
                rid = st.session_state['reset_penyakit']
                c1, c2 = st.columns([1, 4])
                kode = c1.text_input("Kode", placeholder="P01", key=f"pk{rid}")
                nama = c2.text_input("Nama Penyakit", key=f"pn{rid}")
                definisi = st.text_area("Definisi", height=80, key=f"pd{rid}")
                solusi = st.text_area("Solusi", height=100, key=f"ps{rid}")
                st.markdown("---")
                if st.form_submit_button("Simpan Data", type="primary"):
                    try: 
                        # FIX: Sebutkan nama kolom secara eksplisit
                        q = "INSERT INTO tb_penyakit (kode_penyakit, nama_penyakit, definisi, solusi) VALUES (%s, %s, %s, %s)"
                        run_query(q, (kode, nama, definisi, solusi))
                        
                        st.session_state['reset_penyakit'] += 1 # Auto reset
                        st.toast("Berhasil!", icon='✅'); time.sleep(0.5); st.rerun()
                    except Exception as e: 
                        st.error(f"Gagal: {e}")
    with tab3:
        if not df.empty:
            with st.container(border=True):
                pilih = st.selectbox("Pilih Penyakit:", df['kode_penyakit'].tolist())
                if pilih:
                    dt = df[df['kode_penyakit']==pilih].iloc[0]
                    with st.form("edit_p"):
                        nn = st.text_input("Nama", value=dt['nama_penyakit']); nd = st.text_area("Definisi", value=dt['definisi']); ns = st.text_area("Solusi", value=dt['solusi']); c1, c2 = st.columns(2)
                        if c1.form_submit_button("Update", type="primary"): run_query("UPDATE tb_penyakit SET nama_penyakit=%s, definisi=%s, solusi=%s WHERE kode_penyakit=%s", (nn, nd, ns, pilih)); st.toast("Updated!", icon='✅'); time.sleep(0.5); st.rerun()
                        # --- UNLOCKED DELETE FOR P00 ---
                        if c2.form_submit_button("Hapus", type="secondary"):
                            # PENGAMAN DIHAPUS.
                            run_query("DELETE FROM tb_aturan WHERE kode_penyakit=%s", (pilih,))
                            run_query("DELETE FROM tb_penyakit WHERE kode_penyakit=%s", (pilih,))
                            st.toast("Dihapus!", icon='🗑️'); time.sleep(0.5); st.rerun()

# 5. RULES (GLOBAL CHECK UNIQUE RULE ID)
def page_rules():
    header_section("🔗", "Basis Aturan (Rules)", "Hubungkan Penyakit dengan Gejala.")
    
    # Ambil Data Master
    try:
        df_p = get_data("SELECT * FROM tb_penyakit")
        df_g = get_data("SELECT * FROM tb_gejala")
        # Ambil semua aturan untuk validasi global
        df_all_rules = get_data("SELECT kode_rule, kode_penyakit FROM tb_aturan GROUP BY kode_rule, kode_penyakit")
    except:
        st.error("Gagal memuat data database."); return

    if df_p.empty or df_g.empty: st.error("Data Master Penyakit/Gejala belum lengkap."); return

    tab1, tab2 = st.tabs(["⚙️ Konfigurasi Aturan", "📊 Matriks Rules"])

    # --- TAB 1: KONFIGURASI ---
    with tab1:
        with st.container(border=True):
            p_dict = dict(zip(df_p['nama_penyakit'], df_p['kode_penyakit']))
            
            # [FIX] Dropdown kosong di awal
            p_name = st.selectbox(
                "Pilih Penyakit:", 
                list(p_dict.keys()), 
                index=None, 
                placeholder="-- Silakan Pilih Penyakit --"
            )
            
            if p_name:
                pid = p_dict[p_name]
                st.info(f"Aturan untuk: **{p_name} ({pid})**")
                
                col_r1, col_r2 = st.columns(2)
                with col_r1: rule_code_input = st.text_input("Kode Rule (Unik)", placeholder="Contoh: R11")
                with col_r2: detail_input = st.text_input("Detail Kondisi", placeholder="Contoh: Anemia Ringan / Berat")
                
                old_gejala_list = []
                is_duplicate_other_disease = False
                owner_disease = ""

                if rule_code_input:
                    if not df_all_rules.empty:
                        check_global = df_all_rules[df_all_rules['kode_rule'] == rule_code_input]
                        if not check_global.empty:
                            existing_pid = check_global.iloc[0]['kode_penyakit']
                            if existing_pid != pid:
                                is_duplicate_other_disease = True
                                owner_disease = existing_pid

                    cek_rule_local = get_data(f"SELECT detail_kondisi, kode_gejala FROM tb_aturan WHERE kode_rule='{rule_code_input}' AND kode_penyakit='{pid}'")
                    
                    if is_duplicate_other_disease:
                        st.error(f"⛔ **DILARANG:** Kode **{rule_code_input}** sudah digunakan oleh penyakit **{owner_disease}**. Harap gunakan kode baru (misal: R11).")
                    elif not cek_rule_local.empty: 
                        st.success(f"ℹ️ Rule **{rule_code_input}** ditemukan pada penyakit ini. Mode: **EDIT DATA**")
                        old_gejala_list = cek_rule_local['kode_gejala'].tolist()
                        # Auto-fill detail kondisi jika edit
                        if not detail_input:
                            st.caption(f"Detail saat ini: *{cek_rule_local.iloc[0]['detail_kondisi']}*")
                    else: 
                        st.caption(f"✨ Rule **{rule_code_input}** belum ada. Mode: **BUAT BARU**")

                st.markdown("---")
                st.write(f"**Pilih Gejala:**")
                
                with st.form("rules_form"):
                    # Tampilkan Checkbox Gejala
                    cols = st.columns(2)
                    sel = []
                    for idx, row in df_g.iterrows():
                        gid = row['kode_gejala']
                        checked = gid in old_gejala_list
                        with cols[idx%2]:
                            if st.checkbox(f"**{gid}** - {row['nama_gejala']}", value=checked, key=f"r_{pid}_{gid}_{rule_code_input}"):
                                sel.append(gid)
                    
                    st.markdown("---")
                    # Tombol Simpan (Disable jika duplikat)
                    submit = st.form_submit_button("💾 Simpan Rule Ini", type="primary", use_container_width=True, disabled=is_duplicate_other_disease)
                    
                    if submit:
                        if is_duplicate_other_disease:
                            st.error("Ganti Kode Rule dulu!")
                        elif not rule_code_input or not detail_input or not sel: 
                            st.error("Lengkapi Kode Rule, Detail Kondisi, dan minimal 1 Gejala!")
                        else:
                            # Hapus data lama (overwrite mode edit)
                            run_query(f"DELETE FROM tb_aturan WHERE kode_rule='{rule_code_input}' AND kode_penyakit='{pid}'")
                            # Insert data baru
                            for g in sel: 
                                run_query("INSERT INTO tb_aturan (kode_rule, kode_penyakit, detail_kondisi, kode_gejala) VALUES (%s, %s, %s, %s)", (rule_code_input, pid, detail_input, g))
                            
                            st.toast(f"Rule {rule_code_input} Tersimpan!", icon='✅')
                            time.sleep(1)
                            st.rerun()

                # Hapus Rule
                if rule_code_input and not is_duplicate_other_disease and not cek_rule_local.empty:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander(f"🗑️ Hapus Rule {rule_code_input}?"):
                        if st.button("Ya, Hapus", type="primary"):
                            run_query(f"DELETE FROM tb_aturan WHERE kode_rule='{rule_code_input}' AND kode_penyakit='{pid}'")
                            st.toast("Terhapus!", icon='🗑️')
                            time.sleep(1)
                            st.rerun()

    # --- TAB 2: MATRIKS ---
    with tab2:
        with st.container(border=True):
            st.markdown("#### Daftar Aturan Tersimpan")
            q = """
            SELECT 
                a.kode_rule, 
                p.nama_penyakit, 
                a.detail_kondisi, 
                GROUP_CONCAT(a.kode_gejala ORDER BY a.kode_gejala SEPARATOR ', ') as daftar_gejala 
            FROM tb_aturan a 
            JOIN tb_penyakit p ON a.kode_penyakit=p.kode_penyakit 
            GROUP BY a.kode_rule, p.nama_penyakit, a.detail_kondisi 
            ORDER BY LENGTH(a.kode_rule), a.kode_rule ASC
            """
            try: 
                df_v = get_data(q)
                st.dataframe(df_v, use_container_width=True, hide_index=True)
            except: 
                st.error("Gagal memuat matriks.")

# 6. LAPORAN (FIX: OVERLAPPING TEXT & LAYOUT)
def page_laporan():
    header_section("📄", "Laporan Riwayat Konsultasi", "Rekapitulasi diagnosa dan gejala pasien.")
    
    # Ambil Data Master Gejala untuk mapping kode ke nama
    try: 
        master_gejala = get_data("SELECT kode_gejala, nama_gejala FROM tb_gejala")
        gejala_dict = dict(zip(master_gejala['kode_gejala'], master_gejala['nama_gejala']))
    except: 
        gejala_dict = {}
    
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1: start_date = st.date_input("Dari Tanggal", value=datetime.today())
        with c2: end_date = st.date_input("Sampai Tanggal", value=datetime.today())
        with c3: search_keyword = st.text_input("Cari Pasien / Diagnosa", placeholder="Ketik kata kunci...")
        
        # Query Data
        query_laporan = f"""
            SELECT r.id_riwayat, r.tanggal_konsultasi, u.nama_lengkap, r.hasil_diagnosa, r.gejala_terpilih 
            FROM tb_riwayat r 
            JOIN tb_user u ON r.id_user=u.id_user 
            WHERE (r.tanggal_konsultasi BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59') 
            AND (u.nama_lengkap LIKE '%{search_keyword}%' OR r.hasil_diagnosa LIKE '%{search_keyword}%') 
            ORDER BY r.tanggal_konsultasi ASC
        """
        df = get_data(query_laporan)
        
        st.markdown("---")
        if not df.empty:
            st.info(f"Ditemukan **{len(df)}** data.")
            st.dataframe(df, use_container_width=True, hide_index=True, column_config={"tanggal_konsultasi": st.column_config.DatetimeColumn("Tanggal", format="D MMM YYYY, HH:mm")})
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_pdf, _ = st.columns([1, 3])
            
            with col_pdf:
                if st.button("🖨️ Cetak PDF (Laporan Resmi)", type="primary", use_container_width=True):
                    try:
                        # --- KONFIGURASI PDF ---
                        pdf = MedicalReportPDF('L', 'mm', 'A4') # Landscape
                        pdf.alias_nb_pages()
                        pdf.add_page()
                        
                        # Info Periode
                        pdf.set_font('Arial', '', 10)
                        pdf.cell(0, 6, f'Periode Laporan : {start_date.strftime("%d-%m-%Y")} s/d {end_date.strftime("%d-%m-%Y")}', 0, 1, 'L')
                        pdf.ln(4)

                        # Definisi Lebar Kolom
                        w = [10, 35, 50, 60, 120] 
                        h_cols = ['No', 'Tanggal', 'Nama Pasien', 'Diagnosa', 'Gejala Klinis yang Dialami']
                        
                        # Fungsi Cetak Header Tabel
                        def print_table_header():
                            pdf.set_fill_color(0, 96, 100) # Warna Hijau Tua
                            pdf.set_text_color(255)        # Teks Putih
                            pdf.set_font('Arial', 'B', 9)
                            for i in range(len(h_cols)):
                                pdf.cell(w[i], 8, h_cols[i], 1, 0, 'C', True) # Border 1 agar rapi
                            pdf.ln()
                            pdf.set_text_color(0)          # Reset Hitam
                            pdf.set_font('Arial', '', 9)

                        # Cetak Header Pertama Kali
                        print_table_header()
                        
                        no = 1
                        for index, row in df.iterrows():
                            # 1. SIAPKAN DATA & BERSIHKAN STRING
                            # Parse Gejala
                            raw_codes = str(row['gejala_terpilih']).split(',')
                            decoded_list = []
                            for code in raw_codes:
                                code = code.strip()
                                name = gejala_dict.get(code, code)
                                decoded_list.append(f"- {code} : {name}")
                            gejala_text = "\n".join(decoded_list)
                            
                            # Bersihkan simbol matematika yang bikin error di FPDF
                            diag_text = str(row['hasil_diagnosa']).replace('\u2265', '>=').replace('\u2264', '<=')
                            gejala_text = gejala_text.replace('\u2265', '>=').replace('\u2264', '<=').replace('•', '-')

                            # 2. HITUNG TINGGI BARIS (ROW HEIGHT)
                            pdf.set_font('Arial', '', 9)
                            
                            # Hitung berapa baris yang dibutuhkan kolom Diagnosa
                            # split_only=True mensimulasikan output tanpa mencetak
                            lines_diag = pdf.multi_cell(w[3], 5, diag_text, split_only=True)
                            h_diag = len(lines_diag) * 5
                            
                            # Hitung berapa baris yang dibutuhkan kolom Gejala
                            lines_gej = pdf.multi_cell(w[4], 5, gejala_text, split_only=True)
                            h_gej = len(lines_gej) * 5
                            
                            # Tinggi Nama Pasien (jika nama panjang)
                            lines_nama = pdf.multi_cell(w[2], 5, str(row['nama_lengkap']), split_only=True)
                            h_nama = len(lines_nama) * 5

                            # Ambil Tinggi Maksimal dari ketiga kolom tersebut
                            # Tambahkan padding 4mm agar tidak terlalu mepet
                            row_height = max(h_diag, h_gej, h_nama, 10) 
                            
                            # 3. CEK SISA HALAMAN (PAGE BREAK)
                            # A4 Landscape Height = 210mm. Footer start -15.
                            # Safe limit sekitar 175mm
                            if pdf.get_y() + row_height > 175: 
                                pdf.add_page()
                                print_table_header() # Cetak Header lagi di halaman baru
                            
                            # 4. CETAK BARIS DATA
                            # Simpan posisi Y awal baris ini
                            y_start = pdf.get_y()
                            x_start = pdf.get_x()

                            # Styling Zebra (Selang-seling warna)
                            if no % 2 == 0: pdf.set_fill_color(240, 240, 240)
                            else: pdf.set_fill_color(255, 255, 255)

                            # --- KOLOM 1: NO ---
                            pdf.cell(w[0], row_height, str(no), 1, 0, 'C', True)
                            
                            # --- KOLOM 2: TANGGAL ---
                            pdf.cell(w[1], row_height, str(row['tanggal_konsultasi'])[0:16], 1, 0, 'C', True)
                            
                            # --- KOLOM 3: NAMA (MultiCell Manual Positioning) ---
                            x_nama = pdf.get_x()
                            pdf.cell(w[2], row_height, '', 1, 0, 'L', True) # Background box
                            pdf.set_xy(x_nama, y_start) # Reset posisi untuk isi teks
                            pdf.multi_cell(w[2], 5, str(row['nama_lengkap']), 0, 'L')
                            pdf.set_xy(x_nama + w[2], y_start) # Pindah ke sebelah kanan kolom ini

                            # --- KOLOM 4: DIAGNOSA ---
                            x_diag = pdf.get_x()
                            pdf.cell(w[3], row_height, '', 1, 0, 'L', True) # Background box
                            pdf.set_xy(x_diag, y_start) 
                            pdf.multi_cell(w[3], 5, diag_text, 0, 'L')
                            pdf.set_xy(x_diag + w[3], y_start)

                            # --- KOLOM 5: GEJALA ---
                            x_gej = pdf.get_x()
                            pdf.cell(w[4], row_height, '', 1, 0, 'L', True) # Background box
                            pdf.set_xy(x_gej, y_start)
                            pdf.multi_cell(w[4], 5, gejala_text, 0, 'L')
                            
                            # 5. PINDAH KE BARIS BERIKUTNYA
                            pdf.set_xy(10, y_start + row_height)
                            no += 1

                        pdf.ln(10)
                        
                        # Tanda Tangan
                        if pdf.get_y() > 140: pdf.add_page() # Cek tempat tanda tangan
                        
                        pdf.set_x(200)
                        pdf.cell(60, 6, f'Padang, {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
                        pdf.set_x(200)
                        pdf.cell(60, 6, 'Mengetahui,', 0, 1, 'C')
                        pdf.set_x(200)
                        pdf.cell(60, 6, 'Dokter Penanggung Jawab / Bidan', 0, 1, 'C')
                        pdf.ln(25)
                        pdf.set_x(200)
                        pdf.cell(60, 6, '( ..................................................... )', 0, 1, 'C')
                        pdf.set_x(200)
                        pdf.cell(60, 6, 'NIP. .....................................', 0, 1, 'C')

                        # Output PDF
                        pdf_byte = pdf.output(dest='S').encode('latin-1', 'replace')
                        st.download_button(label="⬇️ Download PDF Resmi", data=pdf_byte, file_name=f"Laporan_Medis_{datetime.now().strftime('%Y%m%d')}.pdf", mime='application/pdf', type="secondary")
                        st.success("PDF Siap Cetak!")
                        
                    except Exception as e: st.error(f"Gagal generate PDF: {e}")
        else: st.warning("Data tidak ditemukan.")