import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# PENGATURAN API KEY DAN MODEL (PENTING! UBAH SESUAI KEBUTUHAN ANDA)
# ==============================================================================

# GANTI INI DENGAN API KEY GEMINI ANDA!
# Catatan: Simpan API Key sebagai Secret di Streamlit Cloud untuk keamanan.
# st.secrets["GEMINI_API_KEY"]
API_KEY = "AIzaSyDLxnmmEOksLM4WPVPTs3DIEPOo1IW5faw" # <--- GANTI BAGIAN INI!

# Nama model Gemini yang akan digunakan.
MODEL_NAME = 'gemini-1.5-flash'

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================

# Definisikan peran chatbot Anda di sini.
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah Budayawan. Tuliskan tentang kebudayaan yang ingin diketahui. Jawaban singkat dan jelas. Tolak pertanyaan selain tentang budaya"]
    },
    {
        "role": "model",
        "parts": ["Baik! Saya akan menjawab tentang budaya!."]
    }
]

# ==============================================================================
# FUNGSI STREAMLIT UTAMA
# ==============================================================================

def main():
    st.set_page_config(page_title="Gemini Chatbot Budaya")
    st.title("Gemini Chatbot Budaya 🇮🇩")
    st.caption("Aplikasi chatbot sederhana dengan Gemini dan Streamlit.")

    # Inisialisasi API Key
    try:
        if API_KEY and API_KEY != "AIzaSyDLxnmmEOksLM4WPVPTs3DIEPOo1IW5faw":
            genai.configure(api_key=API_KEY)
        else:
            st.error("Peringatan: API Key belum diatur. Harap ganti 'AIza...' dengan API Key Anda.")
            return
    except Exception as e:
        st.error(f"Kesalahan saat mengonfigurasi API Key: {e}")
        return

    # Inisialisasi model
    if 'model' not in st.session_state:
        try:
            st.session_state.model = genai.GenerativeModel(
                MODEL_NAME,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=500
                )
            )
        except Exception as e:
            st.error(f"Kesalahan saat inisialisasi model '{MODEL_NAME}': {e}")
            return

    # Inisialisasi riwayat chat di Streamlit Session State
    if "messages" not in st.session_state:
        st.session_state.messages = list(INITIAL_CHATBOT_CONTEXT)

    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0])
    
    # Ambil input pengguna
    if user_input := st.chat_input("Tanyakan sesuatu tentang budaya..."):
        # Tambahkan pesan pengguna ke riwayat dan tampilkan
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Kirim riwayat chat ke model dan dapatkan balasan
        with st.chat_message("assistant"):
            with st.spinner("Sedang membalas..."):
                try:
                    chat_session = st.session_state.model.start_chat(history=st.session_state.messages[:-1])
                    response = chat_session.send_message(user_input, request_options={"timeout": 60})
                    
                    if response and response.text:
                        st.markdown(response.text)
                        # Tambahkan balasan model ke riwayat
                        st.session_state.messages.append({"role": "model", "parts": [response.text]})
                    else:
                        st.warning("Maaf, saya tidak bisa memberikan balasan.")
                        
                except Exception as e:
                    st.error(f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {e}")

if __name__ == "__main__":
    main()
