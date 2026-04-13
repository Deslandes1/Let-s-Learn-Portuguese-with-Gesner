import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Audio Setup Fix -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

def set_colorful_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e); }
        .main-header { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stText { color: white !important; font-size: 1rem; background: transparent !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(255,255,255,0.1); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: rgba(255,255,255,0.3); color: white !important; }
        .stButton button { background-color: #ff6b6b; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #feca57; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #1a0b2e, #2d1b4e); }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #2d1b4e; border: 1px solid #ffcc00; border-radius: 10px; }
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

# ----- 1. Authentication Logic -----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_colorful_style()
    st.title("🔐 Acesso Necessário")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Portuguese with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #FFD700;'>Livro 1 – Lições 1 a 20</p>", unsafe_allow_html=True)
        password_input = st.text_input("Digite a senha para acessar", type="password")
        if st.button("Entrar"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta. Acesso negado.")
    st.stop()

# ----- 2. UI Setup -----
set_colorful_style()
st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn Portuguese with Gesner</h1>
    <p>Livro 1 – 20 lições interativas | Conversas cotidianas | Vocabulário | Gramática | Pronúncia | Questionários</p>
</div>
""", unsafe_allow_html=True)

# ----- 3. Content Definition -----
temas = [
    "Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções",
    "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações",
    "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário",
    "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"
]

def generar_conversaciones(tema):
    conv1 = f"A: Olá! Como você está hoje?\nB: Estou bem, obrigado! Estou aprendendo sobre {tema}.\nA: Isso é maravilhoso. Pode me contar mais?\nB: Com certeza! Eu pratico todos os dias."
    conv2 = f"A: Com licença, você poderia me ajudar com {tema}?\nB: Claro! O que você precisa saber?\nA: Quero melhorar meu português.\nB: Essa é uma ótima meta. Continue praticando!"
    conv3 = f"A: Olá, sou novo aqui. Você pode me explicar {tema}?\nB: Com certeza! É muito útil para a vida diária.\nA: Muito obrigado!\nB: De nada. Vamos praticar juntos."
    return [conv1, conv2, conv3]

def generar_vocabulario(tema):
    base_words = ["olá", "tchau", "por favor", "obrigado", "sim", "não", "talvez", "sempre", "às vezes", "nunca",
                  "rápido", "devagar", "cuidadosamente", "felizmente", "infelizmente", "alto", "baixo", "claro", "escuro", "suavemente"]
    return base_words[:20]

def generar_reglas_gramaticales():
    return [
        "1. Use o presente simples para fatos e rotinas.",
        "2. Use 'ser' e 'estar' corretamente (permanente vs. temporário).",
        "3. Use 'ter' para expressar posse e idade.",
        "4. Use 'poder' para expressar habilidade ou permissão.",
        "5. Use 'fazer' para perguntar sobre o tempo (Como está o tempo?).",
        "6. Advérbios de frequência geralmente vêm antes do verbo.",
        "7. Use preposições de lugar (em, sobre, embaixo de) corretamente.",
        "8. Use 'há' para indicar que algo existe.",
        "9. Use 'eu gostaria' para pedidos formais.",
        "10. Use 'ir + infinitivo' para planos futuros."
    ]

# ----- 4. Audio Engine (Portuguese Voice) -----
async def save_speech(text, file_path):
    # Using 'pt-BR-AntonioNeural' for high-quality Brazilian Portuguese
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desabilitado. Verifique a instalação do edge-tts.")
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
                if os.path.exists(tmp.name): os.unlink(tmp.name)

# ----- 5. Sidebar & Navigation -----
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Selecione a lição")
    lesson_number = st.selectbox("Lição", list(range(1, 21)), index=0)
    st.progress(lesson_number / 20)
    st.markdown("---")
    st.markdown("**Fundador e Desenvolvedor:**")
    st.markdown("Gesner Deslandes")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ----- 6. Lesson Rendering -----
tema_atual = temas[lesson_number - 1]
st.markdown(f"## 📖 Lição {lesson_number}: {tema_atual}")

tab1, tab2, tab3 = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática"])

with tab1:
    conversas = generar_conversaciones(tema_atual)
    for i, conv in enumerate(conversas, 1):
        st.markdown(f"**Conversa {i}**")
        st.text(conv)
        reproducir_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

with tab2:
    vocab = generar_vocabulario(tema_atual)
    cols = st.columns(4)
    for idx, palavra in enumerate(vocab):
        with cols[idx % 4]:
            st.markdown(f"**{palabra.capitalize()}**")
            reproducir_audio(palabra, f"vocab_{lesson_number}_{idx}")

with tab3:
    for regra in generar_reglas_gramaticales():
        st.markdown(f"- {regra}")
