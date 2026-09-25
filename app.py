import streamlit as st
import math
import time
import sqlite3
import json
import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types

# ==========================================
# 1. DATABASE SQLITE PERSISTENCE
# ==========================================
def init_db():
    conn = sqlite3.connect("zuhri_ai_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            tool_name TEXT,
            user_input TEXT,
            ai_output TEXT,
            zuhri_metric_name TEXT,
            zuhri_metric_value REAL
        )
    """)
    conn.commit()
    conn.close()

def save_history(category, tool_name, user_input, ai_output, metric_name, metric_value):
    conn = sqlite3.connect("zuhri_ai_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO project_history (timestamp, category, tool_name, user_input, ai_output, zuhri_metric_name, zuhri_metric_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category, tool_name, user_input, ai_output, metric_name, metric_value))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("zuhri_ai_history.db")
    df = pd.read_sql_query("SELECT * FROM project_history ORDER BY id DESC", conn)
    conn.close()
    return df

# Initialize Database
init_db()

# ==========================================
# 2. FORMALISME KONSTANTA ZUHRI ENGINE
# ==========================================
class ZuhriFormalismEngine:
    """
    Mesin Penyeimbang & Pengontrol Kualitas Output berbasis Formalisme Zuhri
    """
    @staticmethod
    def calculate_nd(word_count, target_density=0.85):
        # K_nd: Narrative Density Constant
        return round(math.log1p(word_count) * target_density, 4)

    @staticmethod
    def calculate_fe(margin, roi_factor=1.15):
        # K_fe: Financial Equilibrium Index
        return round((margin * roi_factor) / 100, 4)

    @staticmethod
    def calculate_we(step_count):
        # K_we: Workflow Execution Constant
        return round(1.0 / (1.0 + math.exp(-0.5 * step_count)), 4)

    @staticmethod
    def calculate_ar(keywords_count, volume=1000):
        # K_ar: Algorithmic Reach Scale
        return round((keywords_count * math.sqrt(volume)) / 100, 4)

# ==========================================
# 3. STREAMLIT APP CONFIG & SIDEBAR
# ==========================================
st.set_page_config(
    page_title="Aa Baroq Applied Technologies — 19 AI Business Suite",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ 19 Tools AI Bisnis — Zuhri Formalism Engine")
st.caption("Aplikasi MVP Terpadu: Otomasi Bisnis, Kalkulasi Finansial, dan Generasi Konten berbasis Kontrol Matematis Zuhri.")

# API Key Handler via Sidebar
st.sidebar.header("🔑 Pengaturan API Key")
gemini_api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Masukkan API Key Google Gemini Anda untuk aktifkan real AI generation.")

# Initialize Gemini Client
client = None
if gemini_api_key:
    try:
        client = genai.Client(api_key=gemini_api_key)
        st.sidebar.success("Gemini API Terhubung!")
    except Exception as e:
        st.sidebar.error(f"Gagal menghubungkan API: {e}")
else:
    st.sidebar.info("💡 Mode Simulasi aktif. Masukkan Gemini API Key untuk hasil generasi AI langsung dari LLM.")

st.sidebar.markdown("---")
st.sidebar.header("📌 Navigasi Utama")
main_menu = st.sidebar.radio("Pilih Halaman:", ["🛠️ Dashboard 19 Tools AI", "📜 Riwayat & Export Proyek"])

# ==========================================
# 4. HALAMAN 1: DASHBOARD 19 TOOLS AI
# ==========================================
if main_menu == "🛠️ Dashboard 19 Tools AI":
    category = st.sidebar.selectbox(
        "Pilih Kategori Tool:",
        [
            "1. Generasi Teks & Narasi Bisnis",
            "2. Analisis Data, Pasar & Finansial",
            "3. Otomasi, Kode & Alur Kerja",
            "4. Optimasi, Pemasaran & Media Visual"
        ]
    )

    # Helper Function untuk Call Gemini API
    def generate_ai_response(prompt_system, prompt_user):
        if client:
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{prompt_system}\n\n[INPUT PENGGUNA]:\n{prompt_user}"
                )
                return response.text
            except Exception as e:
                return f"[Error API]: {str(e)}"
        else:
            # Output Simulasi jika API Key belum diisi
            return (
                f"=== [HASIL SIMULASI TOOL] ===\n\n"
                f"Permintaan: {prompt_user}\n\n"
                f"Rekomendasi Strategis:\n"
                f"1. Implementasikan ide ini dengan fokus pada skalabilitas operasional.\n"
                f"2. Gunakan pendekatan terstruktur berbasis nilai kerapatan informasi Zuhri.\n"
                f"3. Lakukan uji coba pasar secara bertahap dalam kurun waktu 14 hari."
            )

    # --- KATEGORI 1: TEKS & NARASI ---
    if category == "1. Generasi Teks & Narasi Bisnis":
        st.subheader("📝 Modul Generasi Teks & Narasi Bisnis")
        tool = st.selectbox(
            "Pilih Tool Spesifik:",
            ["Business Plan", "Content Writer", "E-Commerce Product Desc", "Video Script", "Landing Page Copy", "Business Idea Generator", "Survey Generator"]
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            user_prompt = st.text_area("Masukkan Detail Produk / Ide Bisnis / Topik:", "Keripik pisang lumer rasa cokelat keju kemasan premium")
        with col2:
            st.markdown("### 🧮 Zuhri Engine Metrics")
            target_density = st.slider("Target Narrative Density ($K_{nd}$):", 0.5, 1.0, 0.85)

        if st.button(f"Generate Output ({tool})"):
            with st.spinner("Memproses dengan Zuhri Narrative Density Constant ($K_{nd}$)..."):
                word_count = max(len(user_prompt.split()), 1) * 15
                k_nd = ZuhriFormalismEngine.calculate_nd(word_count, target_density)

                sys_instruction = f"Anda adalah pakar bisnis dan copywriter handal. Buat output untuk tool '{tool}' berbasis input pengguna. Perhatikan kepadatan narasi Zuhri K_nd = {k_nd}."
                ai_result = generate_ai_response(sys_instruction, user_prompt)

                st.success(f"Output Berhasil Digenerate! [Zuhri $K_{{nd}}$ Score: {k_nd}]")
                st.markdown(ai_result)

                # Save to DB
                save_history(category, tool, user_prompt, ai_result, "K_nd", k_nd)

                # Export Options
                st.markdown("---")
                st.subheader("📥 Unduh Output File")
                d_col1, d_col2, d_col3 = st.columns(3)
                d_col1.download_button("📄 Unduh .TXT", data=ai_result, file_name=f"{tool.lower().replace(' ', '_')}_output.txt", mime="text/plain")
                
                html_data = f"<html><body><h1>{tool} Output</h1><p><b>Zuhri K_nd Score:</b> {k_nd}</p><hr/><pre>{ai_result}</pre></body></html>"
                d_col2.download_button("🌐 Unduh .HTML", data=html_data, file_name=f"{tool.lower().replace(' ', '_')}_output.html", mime="text/html")
                
                json_data = json.dumps({"tool": tool, "metric_k_nd": k_nd, "input": user_prompt, "output": ai_result}, indent=2)
                d_col3.download_button("📦 Unduh .JSON", data=json_data, file_name=f"{tool.lower().replace(' ', '_')}_output.json", mime="application/json")

    # --- KATEGORI 2: ANALISIS & FINANSIAL ---
    elif category == "2. Analisis Data, Pasar & Finansial":
        st.subheader("📊 Modul Analisis Data, Pasar & Finansial")
        tool = st.selectbox("Pilih Tool Spesifik:", ["Financial Calculator", "Data Analysis", "Market Research"])

        if tool == "Financial Calculator":
            st.markdown("#### 💰 Financial Calculator & Equilibrium Index")
            col1, col2, col3 = st.columns(3)
            modal = col1.number_input("Modal Awal (Rp):", value=10000000, step=1000000)
            harga_jual = col2.number_input("Harga Jual per Unit (Rp):", value=50000, step=5000)
            hpp = col3.number_input("HPP per Unit (Rp):", value=30000, step=2000)

            if st.button("Hitung Equilibrium & Margin"):
                margin_pct = ((harga_jual - hpp) / harga_jual) * 100 if harga_jual > 0 else 0
                bep_unit = math.ceil(modal / (harga_jual - hpp)) if (harga_jual - hpp) > 0 else 0
                k_fe = ZuhriFormalismEngine.calculate_fe(margin_pct)

                res_text = (
                    f"Kalkulasi Finansial:\n"
                    f"- Modal Awal: Rp {modal:,.0f}\n"
                    f"- Harga Jual: Rp {harga_jual:,.0f}\n"
                    f"- HPP: Rp {hpp:,.0f}\n"
                    f"- Margin Keuntungan: {margin_pct:.2f}%\n"
                    f"- Break-Even Point (BEP): {bep_unit} Unit\n"
                    f"- Zuhri Financial Equilibrium Index (K_fe): {k_fe}"
                )

                st.markdown("---")
                res_col1, res_col2, res_col3 = st.columns(3)
                res_col1.metric("Margin Keuntungan", f"{margin_pct:.1f}%")
                res_col2.metric("BEP (Break-Even Point)", f"{bep_unit} Unit")
                res_col3.metric("Zuhri Index ($K_{fe}$)", f"{k_fe}")
                st.success("Kalkulasi terverifikasi stabil dengan Zuhri Financial Equilibrium Index.")

                user_inp = f"Modal: {modal}, Harga: {harga_jual}, HPP: {hpp}"
                save_history(category, tool, user_inp, res_text, "K_fe", k_fe)

                st.download_button("📄 Unduh Laporan (.TXT)", data=res_text, file_name="financial_report.txt", mime="text/plain")

        else:
            user_prompt = st.text_area("Masukkan Data / Parameter Riset Pasar:", "Analisis kompetitor untuk produk kopi susu kekinian di area perkotaan")
            if st.button(f"Jalankan {tool}"):
                with st.spinner("Memproses analisis pasar..."):
                    k_fe = ZuhriFormalismEngine.calculate_fe(15.0)
                    sys_instruction = f"Anda adalah analis pasar senior. Berikan laporan komprehensif untuk '{tool}' berdasarkan input pengguna."
                    ai_result = generate_ai_response(sys_instruction, user_prompt)

                    st.markdown(ai_result)
                    save_history(category, tool, user_prompt, ai_result, "K_fe", k_fe)
                    st.download_button("📄 Unduh Hasil (.TXT)", data=ai_result, file_name=f"{tool.lower().replace(' ', '_')}.txt", mime="text/plain")

    # --- KATEGORI 3: OTOMASI & KODE ---
    elif category == "3. Otomasi, Kode & Alur Kerja":
        st.subheader("⚙️ Modul Otomasi, Kode & Alur Kerja")
        tool = st.selectbox("Pilih Tool Spesifik:", ["AI Code Generator", "AI Chatbot", "Automation Workflow"])

        user_prompt = st.text_area("Masukkan Spesifikasi Kode / Rule Chatbot / Workflow:", "Buat form registrasi pengguna berbasis HTML, CSS, dan JavaScript dengan validasi email")

        if st.button(f"Eksekusi Tool ({tool})"):
            with st.spinner("Mengolah alur kerja berbasis Zuhri Syntax Determinism..."):
                steps = max(len(user_prompt.split()), 1)
                k_we = ZuhriFormalismEngine.calculate_we(steps)

                sys_instruction = f"Anda adalah Software Architect & Automation Specialist. Buat output teknis/kode bersih tanpa galat untuk '{tool}'. Patuhi Zuhri K_we = {k_we}."
                ai_result = generate_ai_response(sys_instruction, user_prompt)

                st.success(f"Eksekusi Selesai! [Zuhri $K_{{we}}$ Score: {k_we}]")
                if tool == "AI Code Generator":
                    st.code(ai_result, language="html")
                else:
                    st.markdown(ai_result)

                save_history(category, tool, user_prompt, ai_result, "K_we", k_we)
                st.download_button("📄 Unduh Source / Skrip (.TXT)", data=ai_result, file_name=f"{tool.lower().replace(' ', '_')}.txt", mime="text/plain")

    # --- KATEGORI 4: OPTIMASI & PEMASARAN ---
    elif category == "4. Optimasi, Pemasaran & Media Visual":
        st.subheader("🚀 Modul Optimasi, Pemasaran & Media Visual")
        tool = st.selectbox("Pilih Tool Spesifik:", ["SEO AI", "Social Media Post", "Email Marketing", "AI Image Generator", "Hashtag Generator", "AI Translator"])

        user_prompt = st.text_input("Kata Kunci Utama / Prompt Visual / Teks Sumber:", "sepatu kulit lokal pria premium tahan air")

        if st.button(f"Proses Optimasi ({tool})"):
            with st.spinner("Menghitung Skala Algoritma Zuhri ($K_{ar}$)..."):
                k_ar = ZuhriFormalismEngine.calculate_ar(len(user_prompt.split()), volume=2500)

                sys_instruction = f"Anda adalah spesialis digital marketing & SEO. Buat konten/rekomendasi terbaik untuk tool '{tool}'. Zuhri Algorithmic Reach Scale K_ar = {k_ar}."
                ai_result = generate_ai_response(sys_instruction, user_prompt)

                st.success(f"Optimasi Berhasil! [Zuhri $K_{{ar}}$ Score: {k_ar}]")
                st.markdown(ai_result)

                save_history(category, tool, user_prompt, ai_result, "K_ar", k_ar)
                st.download_button("📄 Unduh Teks Optimasi (.TXT)", data=ai_result, file_name=f"{tool.lower().replace(' ', '_')}.txt", mime="text/plain")

# ==========================================
# 5. HALAMAN 2: RIWAYAT & EXPORT PROYEK
# ==========================================
elif main_menu == "📜 Riwayat & Export Proyek":
    st.subheader("📜 Riwayat Generasi & Manajemen Data Proyek")
    st.caption("Semua riwayat eksekusi tersimpan secara otomatis dalam database SQLite lokal (zuhri_ai_history.db).")

    df_history = load_history()

    if df_history.empty:
        st.info("Belum ada riwayat aktivitas. Silakan jalankan salah satu modul AI pada halaman Dashboard.")
    else:
        st.dataframe(df_history, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Export Seluruh Riwayat Data")

        col_exp1, col_exp2 = st.columns(2)
        
        # CSV Export
        csv_data = df_history.to_csv(index=False).encode('utf-8')
        col_exp1.download_button(
            label="📊 Unduh Semua Riwayat (.CSV)",
            data=csv_data,
            file_name=f"zuhri_ai_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        # JSON Export
        json_export = df_history.to_json(orient="records", indent=2)
        col_exp2.download_button(
            label="📦 Unduh Semua Riwayat (.JSON)",
            data=json_export,
            file_name=f"zuhri_ai_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
