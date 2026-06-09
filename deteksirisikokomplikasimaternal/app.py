import streamlit as st
import time
import base64

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Sistem Pakar Maternal - RSUD Solok Selatan",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# [FIX] CSS ANTI-GHOSTING
# ==============================================================================
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none !important; }
            div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

# --- FUNGSI LOAD CSS ---
def inject_custom_css():
    try:
        with open("style.css", "r") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

inject_custom_css()

# --- FUNGSI GAMBAR ---
@st.cache_data(show_spinner=False)
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# --- IMPORT MODULES ---
from modules.db_connection import check_login, get_data, run_query
from modules.admin_crud import page_dashboard_admin, page_penyakit, page_gejala, page_rules, page_users, page_laporan
from streamlit_option_menu import option_menu
from modules.user_consultation import page_consultation
from modules.user_history import page_history
# [BARU] Import modul profil
from modules.user_profile import page_profile 

try:
    from modules.auth import page_register 
except ImportError:
    page_register = None

# ==============================================================================
# 2. STATE MANAGEMENT
# ==============================================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['user_name'] = None
    st.session_state['user_id'] = None

if 'menu_selection' not in st.session_state:
    st.session_state['menu_selection'] = "Beranda"

def navigate_to(page_name):
    st.session_state['menu_selection'] = page_name
    st.rerun()

# Auto Login via URL
params = st.query_params
if not st.session_state['logged_in'] and 'session_uid' in params:
    try:
        st.session_state['logged_in'] = True
        st.session_state['user_id'] = params.get('session_uid')
        st.session_state['user_name'] = params.get('session_name')
        st.session_state['role'] = params.get('session_role')
        st.rerun()
    except: pass

# ==============================================================================
# 3. FUNGSI LOGIN & LOGOUT
# ==============================================================================
def callback_login():
    username = st.session_state.get('input_username', '').strip()
    password = st.session_state.get('input_password', '').strip()
    role = st.session_state.get('input_role')

    if not role or not username or not password:
        st.warning("⚠️ Mohon lengkapi semua data login.")
        return

    user = check_login(username, password, role)
    if user:
        st.session_state['logged_in'] = True
        st.session_state['role'] = role
        if 'nama_lengkap' in user: nama = user['nama_lengkap']
        elif 'nama' in user: nama = user['nama']
        else: nama = user.get('username', 'User')
        
        st.session_state['user_name'] = nama
        st.session_state['user_id'] = str(user.get('id_user', user.get('id', 0)))

        st.query_params["session_uid"] = st.session_state['user_id']
        st.query_params["session_name"] = nama
        st.query_params["session_role"] = role

        if role == "User (Ibu Hamil)":
            st.session_state['menu_selection'] = "Dashboard Pasien"
        else:
            st.session_state['menu_selection'] = "Dashboard Admin"
    else:
        st.error("❌ Username atau Password salah!")

def logout_callback():
    st.session_state.clear() 
    st.query_params.clear()  

# ==============================================================================
# 4. HALAMAN PUBLIK
# ==============================================================================
def page_login():
    st.markdown("""
        <style>
        button[kind="secondary"] {
            border-radius: 50px !important;
            border: 1px solid #006064 !important;
            color: #006064 !important;
            transition: all 0.3s ease !important;
        }
        button[kind="secondary"]:hover {
            background-color: #E0F2F1 !important;
            transform: scale(1.02);
            border-color: #004D40 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    c_back, c_space = st.columns([1, 5]) 
    with c_back:
        if st.button("⬅ Back", type="secondary", use_container_width=True):
            navigate_to("Beranda")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        with st.container(border=True):
            st.markdown("""
                <div style='text-align: center; margin-bottom: 25px;'>
                    <h2 style='color: #006064; margin-bottom: 10px;'>Selamat Datang Kembali 👋</h2>
                    <p style='color: #546E7A; font-size: 15px; line-height: 1.5;'>
                        Silakan masuk untuk melanjutkan pemantauan kesehatan Bunda dan Buah Hati.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.selectbox("Masuk Sebagai:", ["User (Ibu Hamil)", "Admin (Pakar/Medis)"], index=None, placeholder="Pilih Role Pengguna...", key="input_role")
            st.text_input("Username", placeholder="Masukkan username Anda", key="input_username") 
            st.text_input("Password", type="password", placeholder="Masukkan kata sandi", key="input_password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Masuk ke Aplikasi", type="primary", use_container_width=True):
                callback_login() 
            
            st.markdown("---")
            
            if st.button("Belum punya akun? Daftar disini", type="secondary", use_container_width=True):
                navigate_to("Registrasi")

def page_home_website():
    with st.container():
        col_logo, col_space, col_b1, col_b2, col_b3 = st.columns([3.5, 2, 1.3, 1.3, 1.6], vertical_alignment="center")
        
        with col_logo:
            img_path = "assets/logoRSUD.png"
            img_base64 = get_img_as_base64(img_path)
            img_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3004/3004458.png"

            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="{img_src}" width="70" style="filter: drop-shadow(0 2px 2px rgba(0,0,0,0.1));">
                <div style="line-height: 1.2; display: flex; flex-direction: column; justify-content: center;">
                    <h3 style="margin: 0; color: #006064; font-size: 1.4rem; font-weight: 800; white-space: nowrap;">SISTEM PAKAR MATERNAL</h3>
                    <small style="margin: 0; color: #546E7A; font-size: 0.9rem; font-weight: 600; white-space: nowrap;">RSUD Solok Selatan</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b1:
            if st.button("Beranda", use_container_width=True): navigate_to("Beranda")
    
        with col_b2:
            if st.button("Login", use_container_width=True): navigate_to("Login")
    
        with col_b3:
            if st.button("Registrasi", type="primary", use_container_width=True): navigate_to("Registrasi")

    st.markdown("""
        <div style="
            height: 2px; 
            background: linear-gradient(to right, transparent, #006064, transparent); 
            margin-top: 15px; 
            margin-bottom: 30px; 
            opacity: 0.3;">
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    
    col_text, col_img = st.columns([1, 1], gap="large", vertical_alignment="center")

    with col_text:
        st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Tenang Menanti Buah Hati,<br>Sehat Bersama Kami.</h1>', unsafe_allow_html=True)
        st.markdown("""
        <p class="hero-subtitle">
        <b>Setiap detak jantung si Kecil adalah harapan.</b><br>
        Pantau kondisi Bunda dan Janin dari rumah dengan rasa aman. Kami hadir mendampingi Bunda dengan standar medis terpercaya RSUD.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Mulai Sesi Konsultasi", type="primary"):
            navigate_to("Login")

    with col_img:
        hero_path = "assets/hero_maternal.png"
        hero_base64 = get_img_as_base64(hero_path)
        if hero_base64:
            hero_src = f"data:image/png;base64,{hero_base64}"
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <img src="{hero_src}" style="width: 100%; height: auto; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); animation: fadeInUp 1.5s ease-out;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.image("https://img.freepik.com/free-vector/pregnant-woman-concept-illustration_114360-1659.jpg", width=400)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #006064; margin-bottom: 10px;'>Sahabat Perjalanan Bunda</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; color: #78909C; margin-bottom: 40px; max-width: 700px; margin-left: auto; margin-right: auto;'>
    Kami mengerti kekhawatiran Bunda. Sistem ini hadir untuk memastikan kesehatan Bunda dan si Kecil terpantau dengan baik, kapan saja dan di mana saja.
    </p>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="modern-card"><h1>🩺</h1><h4>Analisa Medis Cerdas</h4><p>Cukup jawab pertanyaan gejala, sistem akan menganalisa kondisi Bunda layaknya sedang berkonsultasi dengan Dokter Spesialis</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="modern-card"><h1>❤️</h1><h4>Hasil Langsung & Tenang</h4><p>Hilangkan rasa cemas menunggu. Dapatkan info potensi kesehatan Bunda saat ini juga, lengkap dengan saran perawatan yang penuh kasih</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="modern-card"><h1>📄</h1><h4>Surat Rujukan Resmi</h4><p>Jika butuh penanganan lanjut, Bunda bisa langsung unduh hasil diagnosa resmi (PDF) untuk dibawa ke Bidan atau Dokter RSUD</p></div>""", unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("@2026 RSUD Solok Selatan.")

# ==============================================================================
# 5. MAIN PROGRAM (CONTROLLER)
# ==============================================================================
def main():
    if st.session_state['logged_in']:
        with st.sidebar:
            img_base64 = get_img_as_base64("assets/logoRSUD.png")
            img_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3004/3004458.png"
            
            st.markdown(f"""
                <div class="sidebar-header-container">
                    <img src="{img_src}" class="sidebar-logo-img">
                    <div style="display: flex; flex-direction: column; justify-content: center; line-height: 1.2;">
                        <span style="font-weight: 700; font-size: 16px; color: #006064; text-transform: uppercase;">Sistem Pakar Maternal</span>
                        <span style="font-size: 11px; color: #546E7A; font-weight: 500;">RSUD Solok Selatan</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)

            if st.session_state['role'] == "Admin (Pakar/Medis)":
                # [FIXED URUTAN ADMIN]
                selected = option_menu(
                    menu_title=None,
                    options=["Dashboard", "Data Pengguna", "Data Gejala", "Data Penyakit", "Basis Aturan", "Laporan Riwayat Konsultasi"],
                    icons=["speedometer2", "people", "thermometer-half", "virus", "diagram-3", "file-earmark-text"],
                    default_index=0,
                    styles={
                        "container": {"padding": "0!important", "background-color": "transparent"},
                        "icon": {"color": "#006064", "font-size": "16px"}, 
                        "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#E0F2F1", "color": "#455A64"},
                        "nav-link-selected": {"background-color": "#006064", "color": "white", "font-weight": "600"},
                    }
                )
                map_menu = {
                    "Dashboard": "Dashboard Admin",
                    "Data Pengguna": "Kelola Pengguna",
                    "Data Gejala": "Manajemen Gejala",
                    "Data Penyakit": "Manajemen Penyakit",
                    "Basis Aturan": "Basis Aturan",
                    "Laporan Riwayat Konsultasi": "Laporan Konsultasi"
                }
                menu = map_menu[selected]

            else:
                # [UPDATE: MENU USER DENGAN PROFIL]
                selected = option_menu(
                    menu_title=None,
                    options=["Beranda", "Konsultasi", "Riwayat", "Profil"], # <--- MENU BARU
                    icons=["house-heart", "heart-pulse", "clock-history", "person"], # <--- ICON BARU
                    default_index=0,
                    styles={
                        "container": {"padding": "0!important", "background-color": "transparent"},
                        "icon": {"color": "#E91E63", "font-size": "16px"},
                        "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#FCE4EC"},
                        "nav-link-selected": {"background-color": "#E91E63", "color": "white", "font-weight": "600"},
                    }
                )
                map_menu = {
                    "Beranda": "Dashboard Pasien",
                    "Konsultasi": "Konsultasi",
                    "Riwayat": "Riwayat",
                    "Profil": "Profil" # <--- MAPPING BARU
                }
                menu = map_menu[selected]

            if menu != st.session_state.get('sidebar_selection_temp'):
                st.session_state['menu_selection'] = menu
                st.session_state['sidebar_selection_temp'] = menu

            st.markdown("---")
            st.button("🚪 Logout", on_click=logout_callback, use_container_width=True)

    page = st.session_state.get('menu_selection', 'Beranda')

    if not st.session_state['logged_in']:
        if page == "Beranda": page_home_website()
        elif page == "Login": page_login()
        elif page == "Registrasi" and page_register: page_register()
        else: page_home_website()

    elif st.session_state['role'] == "Admin (Pakar/Medis)":
        if page == "Dashboard Admin":
            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
            page_dashboard_admin()
        elif page == "Kelola Pengguna": page_users()
        elif page == "Manajemen Gejala": page_gejala()
        elif page == "Manajemen Penyakit": page_penyakit()
        elif page == "Basis Aturan": page_rules()
        elif page == "Laporan Konsultasi": page_laporan()
        else: page_dashboard_admin()

    elif st.session_state['role'] == "User (Ibu Hamil)":
        if page == "Dashboard Pasien":
            try:
                user_id = st.session_state['user_id']
                q_last = f"SELECT tanggal_konsultasi, hasil_diagnosa FROM tb_riwayat WHERE id_user='{user_id}' ORDER BY tanggal_konsultasi DESC LIMIT 1"
                df_last = get_data(q_last)
                
                if not df_last.empty:
                    last_date = df_last['tanggal_konsultasi'].iloc[0]
                    last_result = df_last['hasil_diagnosa'].iloc[0]
                    status_msg = f"Terakhir cek: {last_date}"
                    status_result = last_result
                else:
                    status_msg = "Belum ada riwayat"
                    status_result = "Yuk, cek kesehatan Bunda sekarang!"
            except:
                status_msg = "-"
                status_result = "-"

            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #006064 0%, #00838F 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h2 style="margin:0; font-size: 26px;">Halo, Bunda {st.session_state['user_name']}! 👋</h2>
                <p style="margin:5px 0 0 0; color: #E0F2F1; font-size: 15px;">
                    Selamat datang di ruang pantau kesehatan mandiri RSUD Solok Selatan.
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_main, col_info = st.columns([1.8, 1.2])

            with col_main:
                with st.container(border=True):
                    st.markdown("#### 🩺 Status Terakhir")
                    st.markdown(f"""
                    <div style="background-color: #F5F7F8; padding: 15px; border-radius: 10px; border-left: 5px solid #006064; margin-bottom: 15px;">
                        <p style="margin:0; font-size: 13px; color: #546E7A; font-weight: 600; text-transform: uppercase;">{status_msg}</p>
                        <h3 style="margin: 5px 0 0 0; color: #006064; font-size: 20px;">{status_result}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("Ada keluhan baru yang dirasakan hari ini?")
                    if st.button("Mulai Konsultasi Baru ➡️", type="primary", use_container_width=True):
                        st.session_state['menu_selection'] = "Konsultasi"
                        st.rerun()

                st.write("")
                with st.container(border=True):
                    st.markdown("#### 💡 Tips Sehat Hari Ini")
                    st.info("Minum air putih minimal 8 gelas sehari.", icon="💧")

            with col_info:
                with st.container(border=True):
                    st.markdown("#### 🚨 Tanda Bahaya")
                    st.markdown("<p style='font-size: 13px; color: grey;'>Segera ke IGD RSUD jika Bunda mengalami:</p>", unsafe_allow_html=True)
                    st.error("Pendarahan Hebat", icon="🩸")
                    st.warning("Nyeri Kepala Hebat", icon="⚡")
                    st.warning("Bayi Kurang Aktif", icon="👶")
                    st.error("Ketuban Pecah Dini", icon="💧")
                    st.markdown("---")
                    st.caption("Jika kondisi darurat, segera cari pertolongan medis terdekat.")

        elif page == "Konsultasi":
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            page_consultation()

        elif page == "Riwayat":
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            page_history()
        
        # [BARU] HALAMAN PROFIL
        elif page == "Profil":
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            page_profile()

if __name__ == "__main__":
    main()