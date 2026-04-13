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
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff007f"/>
                    <stop offset="50%" stop-color="#ffcc00"/>
                    <stop offset="100%" stop-color="#00ffcc"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ----- 3. Content Definitions -----
temas = [
    "Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções",
    "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações",
    "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário",
    "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"
]

def get_lesson_data(n):
    tema = temas[n-1]
    return {
        "conversas": [
            f"A: Olá! Como você está?\nB: Estou muito bem, obrigado! Estou estudando {tema}.",
            f"A: Com licença, você pode me ajudar com {tema}?\nB: Claro! É muito simples.",
            f"A: Eu amo aprender português.\nB: Eu também! Praticar {tema} é ótimo."
        ],
        "vocabulario": ["Olá", "Obrigado", "Por favor", "Sim", "Não", "Bom dia", "Boa tarde", "Boa noite", "Tchau", "Até logo"],
        "gramatica": [
            "1. 'Ser' é para características permanentes.",
            "2. 'Estar' é para estados temporários.",
            "3. Use 'há' para indicar existência (There is/are).",
            "4. A maioria das palavras terminadas em 'o' são masculinas."
        ]
    }

# ----- 4. Audio Engine (pt-BR Voice) -----
async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
    await communicate.save(file_path)

def reproduzir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desabilitado no servidor.")
        return
    if st.button(f"🔊 Ouvir", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ----- 5. Authentication Logic -----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_colorful_style()
    st.title("🔐 Acesso Necessário")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Portuguese</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Digite a senha", type="password")
        if st.button("Entrar"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

# ----- 6. Sidebar (Professional Info Always Visible) -----
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Menu de Lições")
    lesson_number = st.selectbox("Selecione a lição", list(range(1, 21)), index=0)
    st.progress(lesson_number / 20)
    st.markdown("---")
    
    # User Branding and Information
    st.markdown("### 👨‍🏫 Informações do Desenvolvedor")
    st.markdown("**Nome:** Gesner Deslandes")
    st.markdown("📞 **WhatsApp:** (509) 4738-5663")
    st.markdown("📧 **Email:** deslandes78@gmail.com")
    st.markdown("🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ----- 7. Main UI Content -----
set_colorful_style()
st.markdown("""<div class="main-header"><h1>📘 Let's Learn Portuguese with Gesner</h1><p>Livro 1 – 20 lições interativas</p></div>""", unsafe_allow_html=True)

data = get_lesson_data(lesson_number)
st.markdown(f"## Lição {lesson_number}: {temas[lesson_number-1]}")

tabs = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática"])

with tabs[0]:
    for i, conv in enumerate(data["conversas"]):
        st.text(conv)
        reproducir_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

with tabs[1]:
    cols = st.columns(2)
    # Corrected loop variable: 'palavra'
    for idx, palavra in enumerate(data["vocabulario"]):
        with cols[idx % 2]:
            st.markdown(f"**{palavra.capitalize()}**")
            reproducir_audio(palavra, f"voc_{lesson_number}_{idx}")

with tabs[2]:
    for regra in data["gramatica"]:
        st.write(f"- {regra}")
