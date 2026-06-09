import mysql.connector
import pandas as pd
import streamlit as st

# --- KONFIGURASI DATABASE ---
# Pastikan nama database sesuai dengan yang ada di phpMyAdmin kamu (db_maternal)
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_maternal" 
    )

# --- FUNGSI 1: EKSEKUSI QUERY (INSERT/UPDATE/DELETE) ---
def run_query(query, values=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        st.error(f"Database Error: {e}")
    finally:
        cursor.close()
        conn.close()

# --- FUNGSI 2: AMBIL DATA (SELECT) JADI DATAFRAME ---
def get_data(query, params=None):
    """
    Fungsi untuk mengambil data (SELECT) dengan dukungan Parameter.
    Contoh pakai: get_data("SELECT * FROM user WHERE id=%s", (123,))
    """
    conn = create_connection()
    if conn is None:
        return pd.DataFrame() # Kembalikan dataframe kosong jika koneksi gagal

    try:
        # Menggunakan pandas read_sql (Standar Industri)
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
            
        conn.close()
        return df
        
    except Exception as e:
        st.error(f"Error Query Data: {e}")
        if conn.is_connected():
            conn.close()
        return pd.DataFrame()

# --- FUNGSI 3: CEK LOGIN (SANGAT PENTING!) ---
def check_login(username, password, role):
    """
    Fungsi untuk mengecek username & password di database.
    Mengembalikan data user (Dictionary) jika ketemu, atau None jika gagal.
    """
    conn = create_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Bedakan tabel berdasarkan Role
        if role == "Admin (Pakar/Medis)":
            # Asumsi tabel admin namanya 'tb_admin', sesuaikan jika beda
            query = "SELECT * FROM tb_admin WHERE username = %s AND password = %s"
        else:
            # Asumsi tabel user namanya 'tb_user'
            query = "SELECT * FROM tb_user WHERE username = %s AND password = %s"
            
        cursor.execute(query, (username, password))
        result = cursor.fetchone() # Ambil 1 data saja
        
        return result # Balikin data user (nama, id, dll)

    except Exception as e:
        st.error(f"Error Login: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()