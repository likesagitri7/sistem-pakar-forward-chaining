from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        # --- KOP SURAT (SAMA PERSIS DENGAN FILE UPLOAD) ---
        try:
            self.image('assets/logoRSUD.png', 10, 8, 20) 
        except: pass
        
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0) # Hitam Standar
        self.cell(0, 5, 'RSUD KABUPATEN SOLOK SELATAN', 0, 1, 'C')
        
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Jalan Raya Km. 1, Nagari Koto Baru, Kec. Sungai Pagu, Solok Selatan', 0, 1, 'C')
        self.cell(0, 5, 'Telp: (0755) 70462 | Email: rsud.solsel@yahoo.co.id', 0, 1, 'C')
        
        # Garis Tebal Kop
        self.ln(5)
        self.set_line_width(0.5)
        self.line(10, 32, 200, 32)
        self.set_line_width(0.1)
        self.line(10, 33, 200, 33)
        self.ln(10)

    def footer(self):
        # --- FOOTER (DISCLAIMER SESUAI PERMINTAAN) ---
        self.set_y(-25)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        # Narasi Disclaimer Resmi
        self.multi_cell(0, 4, "Catatan Sistem: Laporan ini merupakan hasil komputasi Sistem Pakar (Metode Forward Chaining) berdasarkan input gejala pengguna. Diagnosa klinis final dan tindakan medis tetap menjadi wewenang Dokter Spesialis.", 0, 'C')
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'R')

def create_pdf(nama_pasien, umur, alamat, hasil_diagnosa, gejala_list, solusi, status_warna="normal"):
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # --- 1. JUDUL LAPORAN ---
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'LAPORAN HASIL DETEKSI DINI KOMPLIKASI MATERNAL', 0, 1, 'C')
    pdf.ln(5)
    
    # --- 2. BIODATA PASIEN ---
    pdf.set_font('Arial', '', 11)
    
    tgl_sekarang = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    tgl_ttd = datetime.datetime.now().strftime("%d-%m-%Y")

    def row_bio(label, val):
        pdf.set_x(10)
        pdf.cell(40, 7, label, 0, 0)
        pdf.cell(5, 7, ':', 0, 0)
        pdf.cell(0, 7, str(val), 0, 1)

    row_bio("Nama Pasien", nama_pasien)
    row_bio("Tanggal Periksa", tgl_sekarang)
    row_bio("Lokasi", "Sistem Pakar Online (Mandiri)")
    
    # Jika umur/alamat ada isinya, tampilkan. Jika strip (-), sembunyikan biar rapi (opsional)
    if umur and umur != "-": row_bio("Umur", f"{umur} Tahun")
    
    pdf.ln(8) 
    
    # --- SETUP WARNA VISUAL ALERT ---
    if status_warna == "danger":
        bg_color = (255, 240, 240)    # Merah Pucat
        border_color = (200, 0, 0)    # Merah
        text_header = (180, 0, 0)
    elif status_warna == "warning":
        bg_color = (255, 252, 235)    # Kuning Pucat
        border_color = (200, 150, 0)  # Emas
        text_header = (150, 100, 0)
    else:
        bg_color = (240, 248, 255)    # Biru Pucat (Normal)
        border_color = (100, 100, 100)
        text_header = (0, 77, 64)

    # --- 3. HASIL ANALISA / DIAGNOSA ---
    pdf.set_fill_color(*bg_color) 
    pdf.set_draw_color(*border_color)
    pdf.set_text_color(*text_header)
    pdf.set_font("Arial", "B", 11)
    
    # Header Kotak 1
    pdf.cell(0, 8, "  HASIL ANALISA / DIAGNOSA SISTEM", 0, 1, 'L', fill=True)
    
    # Isi Kotak 1
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0) # Hitam
    pdf.set_font("Arial", "B", 12)
    
    # Bersihkan simbol medis (≥ jadi >=)
    clean_diagnosa = str(hasil_diagnosa).replace("≥", ">=").replace("≤", "<=")
    pdf.multi_cell(0, 6, clean_diagnosa)
    pdf.ln(5)

    # --- 4. GEJALA TERDETEKSI (BAGIAN INI TETAP ADA SESUAI REQUEST) ---
    if gejala_list and len(gejala_list) > 0:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "Fakta Klinis / Gejala yang Ditemukan:", 0, 1)
        pdf.set_font("Arial", "", 10)
        for g in gejala_list:
            clean_g = str(g).replace("≥", ">=").replace("≤", "<=")
            pdf.cell(5) # Indent
            pdf.cell(0, 5, f"- {clean_g}", 0, 1)
        pdf.ln(5)

    # --- 5. REKOMENDASI (PERBAIKAN DISINI) ---
    pdf.set_fill_color(255, 248, 225)
    pdf.set_text_color(230, 81, 0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "  REKOMENDASI MEDIS / SARAN PENANGANAN", 0, 1, 'L', fill=True)
    
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)
    
    # FIX: HAPUS .replace("\n", " ") AGAR ENTER TETAP JADI BARIS BARU
    # Kita hanya membersihkan simbol medis dan karakter carriage return (\r)
    clean_solusi = str(solusi).replace("≥", ">=").replace("≤", "<=").replace("\r", "")
    
    # Trik: Jika inputnya string panjang tanpa enter, multi_cell akan wrap otomatis.
    # Jika inputnya ada enter (seperti list 1. 2. 3.), multi_cell akan bikin baris baru.
    pdf.multi_cell(0, 6, clean_solusi)
    pdf.ln(8)

    # --- 6. INSTRUKSI (NARASI SESUAI PDF UPLOAD) ---
    pdf.set_font('Arial', 'BI', 9) # Bold Italic
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Instruksi: Dokumen ini harap dibawa dan ditunjukkan kepada Bidan atau Dokter Spesialis Kandungan (Obgyn) sebagai DATA PENUNJANG MEDIS & HASIL SKRINING AWAL.")
    
    # --- 7. TANDA TANGAN (MUARA LABUH) ---
    pdf.ln(10)
    
    # Cek sisa halaman agar tidak kepotong
    if pdf.get_y() > 220: pdf.add_page()
    
    margin_ttd = 120 
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    
    # Lokasi Muara Labuh
    pdf.set_x(margin_ttd)
    pdf.cell(60, 5, f"Muara Labuh, {tgl_ttd}", 0, 1, 'L')
    
    pdf.set_x(margin_ttd)
    pdf.cell(60, 5, "Validasi Dokter / Tenaga Medis,", 0, 1, 'L')
    
    pdf.ln(25) # Ruang TTD Basah
    
    pdf.set_x(margin_ttd)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 5, "( .................................................... )", 0, 1, 'L')
    
    pdf.set_x(margin_ttd)
    pdf.set_font("Arial", "", 9)
    pdf.cell(60, 5, "Nama Lengkap & Stempel RSUD", 0, 1, 'L')

    # --- FINAL RETURN (SAFE ENCODING) ---
    return pdf.output(dest='S').encode('latin-1', 'replace')