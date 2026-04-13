import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- 1. Audio Setup & Safety Check -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

# ----- 2. Styling & Branding -----
def set_colorful_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e); }
        .main-header { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, [data-testid="stHeader"], .stMarkdown, p, span, label { color: white !important; }
        .stButton button { background-color: #ff6b6b; color: white; border-radius: 30px; font-weight: bold; width: 100%; }
        .stTabs [role="tab"] { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#grad1)" stroke="#ffcc00" stroke-width="3"/>
                <defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff007f"/><stop offset="100%" stop-color="#00ffcc"/></linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ----- 3. Audio Engine (The Part That Was Missing) -----
async def save_speech(text, file_path):
    # Using the Brazilian Portuguese voice Antonio
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.warning("⚠️ Áudio desabilitado. Verifique o seu requirements.txt.")
        return
    
    if st.button(f"🔊 Ouvir", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{data}" controls autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ----- 4. App Logic & Auth -----
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    set_colorful_style()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Portuguese</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if pwd == "20082010": 
                st.session_state.auth = True
                st.rerun()
    st.stop()

# ----- 5. Main Content -----
set_colorful_style()
st.markdown('<div class="main-header"><h1>📘 Let\'s Learn Portuguese with Gesner</h1><p>Lição 1 - 20</p></div>', unsafe_allow_html=True)

temas = ["Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções", "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações", "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário", "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"]

with st.sidebar:
    show_logo()
    lesson = st.selectbox("Escolha a Lição", range(1, 21))
    st.write(f"**Desenvolvedor:** Gesner Deslandes")

tema = temas[lesson-1]
st.markdown(f"## Lição {lesson}: {tema}")

tab1, tab2 = st.tabs(["💬 Conversa", "📚 Vocabulário"])

with tab1:
    txt = f"A: Olá! Como você está?\nB: Estou muito bem, obrigado! Estou estudando {tema}."
    st.text(txt)
    reproducir_audio(txt, f"conv_{lesson}")

with tab2:
    palavras = ["Olá", "Obrigado", "Por favor", "Sim", "Não"]
    cols = st.columns(len(palavras))
    for idx, p in enumerate(palavras):
        with cols[idx]:
            st.write(f"**{p}**")
            reproducir_audio(p, f"voc_{lesson}_{idx}")
