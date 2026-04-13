import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- 1. Audio Engine & Safety -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

# ----- 2. Global Styling (Purple Gradient & White Text) -----
def apply_custom_style():
    st.markdown("""
        <style>
        /* Purple Gradient Background */
        .stApp { background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e); }
        
        /* Header Styling */
        .main-header { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        
        /* Force Text Colors to White */
        html, body, [data-testid="stHeader"], .stMarkdown, p, span, label, h1, h2, h3, .stSelectbox label { color: white !important; }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #1a0b2e, #2d1b4e); border-right: 1px solid rgba(255,255,255,0.1); }
        section[data-testid="stSidebar"] .stMarkdown p { color: white !important; }
        
        /* Buttons & Tabs */
        .stButton button { background-color: #ff6b6b; color: white; border-radius: 30px; font-weight: bold; width: 100%; border: none; }
        .stButton button:hover { background-color: #feca57; color: black; }
        .stTabs [role="tab"] { color: white !important; background: rgba(255,255,255,0.05); }
        .stTabs [role="tab"][aria-selected="true"] { background: rgba(255,255,255,0.2); }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="80" height="80" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="2"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff007f"/><stop offset="100%" stop-color="#00ffcc"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ----- 3. Functional Definitions (Must be before use) -----
async def save_speech(text, file_path):
    # Using Spanish voice as requested: es-ES-AlvaroNeural
    communicate = edge_tts.Communicate(text, "es-ES-AlvaroNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desabilitado.")
        return
    if st.button(f"🔊 Ouvir", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name): os.unlink(tmp.name)

temas = ["Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções", "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações", "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário", "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"]

def get_lesson_data(n):
    tema = temas[n-1]
    return {
        "conversas": [f"A: Olá! Como vai?\nB: Tudo bem! Estou estudando {tema}.", f"A: Você pode me ajudar?\nB: Sim, vamos praticar {tema}.", f"A: Gosto de português.\nB: Eu também!"],
        "vocabulario": ["Olá", "Tchau", "Obrigado", "Por favor", "Sim", "Não", "Talvez", "Sempre", "Nunca", "Hoje", "Amanhã", "Agora", "Amigo", "Família", "Casa", "Escola", "Trabalho", "Comida", "Água", "Livro"],
        "gramatica": ["1. Use 'ser' para fatos fixos.", "2. Use 'estar' para estados temporários.", "3. 'Há' significa 'There is'.", "4. Masculino termina em 'o'.", "5. Feminino termina em 'a'.", "6. Plural usa 's'.", "7. Artigo definido: O/A.", "8. Artigo indefinido: Um/Uma.", "9. Verbos -AR no presente.", "10. Pronomes: Eu, Você, Ele/Ela."]
    }

# ----- 4. Authentication -----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    apply_custom_style()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Portuguese</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

# ----- 5. Sidebar & UI -----
apply_custom_style()
with st.sidebar:
    show_logo()
    st.markdown("### 🎯 Menu de Lições")
    lesson_number = st.selectbox("Selecione a lição", list(range(1, 21)), index=0)
    st.progress(lesson_number / 20)
    st.markdown("---")
    st.markdown("### 👨‍🏫 Informações do Desenvolvedor")
    st.markdown("**Nome:** Gesner Deslandes")
    st.markdown("📞 **WhatsApp:** (509) 4738-5663")
    st.markdown("📧 **Email:** deslandes78@gmail.com")
    st.markdown("🌐 **GlobalInternet.py**")
    st.markdown("---")
    st.markdown("💰 **Preço:** $299 USD")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.markdown('<div class="main-header"><h1>📘 Let\'s Learn Portuguese with Gesner</h1><p>Lições Interativas 1 a 20</p></div>', unsafe_allow_html=True)
data = get_lesson_data(lesson_number)
st.markdown(f"## Lição {lesson_number}: {temas[lesson_number-1]}")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "❓ Quiz"])

with tab1:
    for i, conv in enumerate(data["conversas"]):
        st.text(conv)
        reproducir_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

with tab2:
    cols = st.columns(4)
    for idx, palavra in enumerate(data["vocabulario"]):
        with cols[idx % 4]:
            st.markdown(f"**{palavra}**")
            reproducir_audio(palavra, f"voc_{lesson_number}_{idx}")

with tab3:
    for r in data["gramatica"]:
        st.markdown(f"- {r}")

with tab4:
    st.markdown("Pratique o que aprendeu!")
    resp = st.radio("Qual o tema desta lição?", [temas[lesson_number-1], "Culinária", "Esportes"])
    if st.button("Verificar"):
        if resp == temas[lesson_number-1]: st.success("Correto!")
        else: st.error("Tente novamente.")
