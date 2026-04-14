import streamlit as st
import asyncio
import tempfile
import base64
import os

# ----- 1. Audio Engine & Safety -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

# ----- 2. Styling (Purple Margins & Force White Sidebar Text) -----
def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"] { 
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e) !important; 
        }
        .main-header { 
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); 
            padding: 1.5rem; 
            border-radius: 20px; 
            text-align: center; 
            margin-bottom: 1rem; 
        }
        .main-header h1 { color: white !important; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] label p { color: white !important; font-weight: bold !important; }
        html, body, [data-testid="stHeader"], .stMarkdown, p, span, label, h2, h3 { color: white !important; }
        .stButton button { background-color: #ff6b6b; color: white !important; border-radius: 30px; font-weight: bold; width: 100%; border: none; }
        .stButton button:hover { background-color: #feca57; color: black !important; }
        .stTabs [role="tab"] { color: white !important; }
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

# ----- 3. Audio & Data Functions -----
async def save_speech(text, file_path):
    # Using Portuguese (Portugal) for a neutral European sound, or change to pt-BR-FranciscaNeural for Brazil
    communicate = edge_tts.Communicate(text, "pt-PT-RaquelNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desabilitado.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name): os.unlink(tmp.name)

temas = ["Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções", "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações", "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário", "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"]

def get_lesson_content(n):
    tema = temas[n-1]
    return {
        "conversas": [
            f"A: Olá! Hoje vamos praticar {tema}.\nB: Sim! É um assunto muito importante.",
            f"A: Você já conhece bem {tema}?\nB: Estou aprendendo agora com o mestre Gesner.",
            f"A: Excelente progresso!\nB: Obrigado, o português é fantástico."
        ],
        "vocabulario": ["Olá", "Oi", "Bom dia", "Boa tarde", "Boa noite", "Obrigado", "Sim", "Não", "Nome", "Prazer", "Tchau", "Até logo", "Amigo", "Escola", "Casa", "Água", "Livro", "Família", "Bem", "Mal"],
        "gramatica": [f"1. Como usar verbos em {tema}.", "2. Pronomes pessoais.", "3. Gênero das palavras.", "4. Artigos.", "5. Plural.", "6. Interrogações.", "7. Negações.", "8. Saudação formal.", "9. Verbos terminados em -ar.", "10. Uso de 'você'."],
        "pronuncia": [f"Eu quero aprender mais sobre {tema}.", "Qual é o seu nome?", "Eu sou professor de tecnologia.", "Muito prazer em conhecê-lo.", "Até amanhã."]
    }

# ----- 4. Authentication -----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    apply_custom_style()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h1 style='text-align: center;'>🔐 Login Required</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Let's Learn Portuguese with Gesner</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

# ----- 5. Main UI & Sidebar -----
apply_custom_style()
with st.sidebar:
    show_logo()
    st.markdown("### 🎯 Menu de Lições")
    lesson_number = st.selectbox("Selecione a lição", list(range(1, 21)), index=0, key="lesson_selector")
    st.progress(lesson_number / 20)
    st.markdown("---")
    st.markdown("### 👨‍🏫 Desenvolvedor")
    st.markdown("**Gesner Deslandes**")
    st.markdown("📞 (509) 4738-5663")
    st.markdown("🌐 **GlobalInternet.py**")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.markdown(f'<div class="main-header"><h1>📘 Let\'s Learn Portuguese with Gesner</h1><p>Lição {lesson_number}: {temas[lesson_number-1]}</p></div>', unsafe_allow_html=True)

content = get_lesson_content(lesson_number)
tabs = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "🎧 Pronúncia", "❓ Quiz"])

with tabs[0]:
    for i, c in enumerate(content["conversas"]):
        st.markdown(f"**Conversa {i+1}**")
        st.text(c)
        reproducir_audio(c, f"c_{lesson_number}_{i}")
        st.markdown("---")

with tabs[1]:
    cols = st.columns(4)
    for idx, v in enumerate(content["vocabulario"]):
        with cols[idx % 4]:
            st.markdown(f"**{v}**")
            reproducir_audio(v, f"v_{lesson_number}_{idx}")

with tabs[2]:
    st.subheader("💡 Regras Gramaticais")
    for g in content["gramatica"]:
        st.markdown(f"- {g}")
    
    st.markdown("---")
    
    # NEW SECTION: O BÁSICO
    st.subheader("🌟 O Básico (Os Fundamentos)")
    
    with st.expander("🔤 O Alfabeto Português"):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZÇ"
        cols = st.columns(7)
        for i, letra in enumerate(alfabeto):
            with cols[i % 7]:
                st.write(f"### {letra}")
                reproducir_audio(letra, f"alpha_{letra}_{lesson_number}")

    with st.expander("🔢 Números (Cardinais e Ordinais)"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Cardinais**")
            nums = ["Um", "Dois", "Três", "Dez", "Vinte", "Cem"]
            for n in nums:
                col_t, col_a = st.columns([3, 1])
                col_t.write(n)
                with col_a: reproducir_audio(n, f"card_{n}_{lesson_number}")
        with c2:
            st.markdown("**Ordinais**")
            ords = ["Primeiro", "Segundo", "Terceiro", "Décimo"]
            for o in ords:
                col_t, col_a = st.columns([3, 1])
                col_t.write(o)
                with col_a: reproducir_audio(o, f"ord_{o}_{lesson_number}")

    with st.expander("🗣️ Expressões Idiomáticas"):
        expressoes = [
            {"p": "Dar o nó", "m": "Casar-se."},
            {"p": "Estar com a pulga atrás da orelha", "m": "Estar desconfiado."},
            {"p": "Pão-duro", "m": "Pessoa que não gosta de gastar dinheiro."}
        ]
        for idx, item in enumerate(expressoes):
            st.markdown(f"**{item['p']}**")
            st.caption(f"Significado: {item['m']}")
            reproducir_audio(f"{item['p']}. Significa {item['m']}", f"idm_{idx}_{lesson_number}")
            st.markdown("---")

with tabs[3]:
    st.markdown("### Pratique sua pronúncia")
    for idx, p in enumerate(content["pronuncia"]):
        st.write(f"{idx+1}. {p}")
        reproducir_audio(p, f"p_{lesson_number}_{idx}")
        st.markdown("---")

with tabs[4]:
    st.markdown("### Teste seu conhecimento")
    q = st.radio(f"Sobre o que é a lição {lesson_number}?", [temas[lesson_number-1], "Culinária", "Espaço"], key=f"quiz_{lesson_number}")
    if st.button("Verificar"):
        if q == temas[lesson_number-1]:
            st.success("Correto! Parabéns!")
            st.balloons()
        else:
            st.error("Tente novamente.")
