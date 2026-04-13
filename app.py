import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Safe import for edge_tts with detailed error -----
EDGE_TTS_AVAILABLE = False
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except Exception as e:
    st.error(f"❌ Erro de importação de áudio: {type(e).__name__}: {e}")
    st.warning("""
    **Áudio desabilitado**.  
    Certifique-se de que o `requirements.txt` contenha:Depois faça o redeploy.
""")
# ---------------------------------------------------------

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

def set_colorful_style():
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e); }
    .main-header { background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
    .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
    .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
    html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label,
    .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader,
    .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable,
    .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander,
    .stProgress > div, .stMetric label, .stMetric value,
    div, p, span, pre, code, .element-container, .stTextArea label,
    .stText p, .stText div, .stText span, .stText code {
        color: white !important;
    }
    .stText { color: white !important; font-size: 1rem; background: transparent !important; }
    .stTabs [role="tab"] { color: white !important; background: rgba(255,255,255,0.1); border-radius: 10px; margin: 0 2px; }
    .stTabs [role="tab"][aria-selected="true"] { background: rgba(255,255,255,0.3); color: white !important; }
    .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
    .stButton button { background-color: #ff6b6b; color: white; border-radius: 30px; font-weight: bold; }
    .stButton button:hover { background-color: #feca57; color: black; }
    section[data-testid="stSidebar"] { background: linear-gradient(135deg, #1a0b2e, #2d1b4e); }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
    section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #2d1b4e; border: 1px solid #ffcc00; border-radius: 10px; }
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
    section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span { color: white !important; }
    div[data-baseweb="popover"] ul { background-color: #2d1b4e; border: 1px solid #ffcc00; }
    div[data-baseweb="popover"] li { color: white !important; background-color: #2d1b4e; }
    div[data-baseweb="popover"] li:hover { background-color: #ff6b6b; }
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

# Authentication
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

set_colorful_style()
st.markdown("""
<div class="main-header">
<h1>📘 Let's Learn Portuguese with Gesner</h1>
<p>Livro 1 – 20 lições interativas | Conversas do dia a dia | Vocabulário | Gramática | Pronúncia | Questionários</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
show_logo()
st.markdown("## 🎯 Selecione a lição")
lesson_number = st.selectbox("Lição", list(range(1, 21)), index=0)
st.markdown("---")
st.markdown("### 📚 Seu progresso")
st.progress(lesson_number / 20)
st.markdown(f"✅ Lição {lesson_number} de 20 concluída")
st.markdown("---")
st.markdown("**Fundador e Desenvolvedor:**")
st.markdown("Gesner Deslandes")
st.markdown("📞 WhatsApp: (509) 4738-5663")
st.markdown("📧 Email: deslandes78@gmail.com")
st.markdown("🌐 [Site principal](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
st.markdown("---")
st.markdown("### 💰 Preço")
st.markdown("**$299 USD** (livro completo – 20 lições, código fonte incluído)")
st.markdown("---")
st.markdown("### © 2025 GlobalInternet.py")
st.markdown("Todos os direitos reservados")
st.markdown("---")
if st.button("🚪 Sair", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# ------------------------------
# TEMAS DAS 20 LIÇÕES (português brasileiro)
# ------------------------------
temas = [
"Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções",
"Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações",
"Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário",
"Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"
]

def gerar_conversas(tema):
conv1 = f"A: Olá! Como você está hoje?\nB: Estou bem, obrigado! Estou aprendendo sobre {tema}.\nA: Isso é maravilhoso. Pode me contar mais?\nB: Claro! Pratico todos os dias."
conv2 = f"A: Com licença, você poderia me ajudar com {tema}?\nB: Claro! O que você precisa saber?\nA: Quero melhorar meu português.\nB: Essa é uma ótima meta. Continue praticando!"
conv3 = f"A: Olá, sou novo aqui. Você pode me explicar {tema}?\nB: Absolutamente! É muito útil para o dia a dia.\nA: Muito obrigado!\nB: De nada. Vamos praticar juntos."
return [conv1, conv2, conv3]

def gerar_vocabulario(tema):
base_words = ["olá", "tchau", "por favor", "obrigado", "sim", "não", "talvez", "sempre", "às vezes", "nunca",
              "rapidamente", "lentamente", "cuidadosamente", "felizmente", "tristemente", "em voz alta", "em voz baixa", "brilhantemente", "escuramente", "suavemente"]
tema_words = [tema.lower().replace(" ", "_") + str(i) for i in range(1, 6)]
all_words = base_words[:15] + tema_words
return all_words[:20]

def gerar_regras_gramaticais(tema):
regras = [
    "1. Use o presente simples para fatos e rotinas.",
    "2. Use 'ser' e 'estar' corretamente (características permanentes vs. estados temporários).",
    "3. Use 'ter' para expressar posse e idade.",
    "4. Use 'poder' para expressar habilidade ou permissão.",
    "5. Use 'fazer' para perguntar sobre o clima (Que tempo faz?).",
    "6. Os advérbios de frequência (sempre, às vezes, nunca) vêm antes do verbo principal.",
    "7. Use as preposições de lugar (em, sobre, debaixo de) corretamente.",
    "8. Use 'há' para dizer que algo existe.",
    "9. Use 'gostaria de' para pedidos educados.",
    "10. Use 'ir + infinitivo' para planos futuros."
]
random.shuffle(regras)
return regras

def gerar_oracoes_pronuncia(tema):
return [
    f"Estou aprendendo sobre {tema} hoje.",
    f"Você poderia me explicar {tema} por favor?",
    f"Praticar {tema} me ajuda a melhorar meu português.",
    f"Vamos falar sobre {tema} juntos.",
    f"Entender {tema} é muito útil."
]

def gerar_perguntas_questionario(tema):
return [
    {"pergunta": "Qual é o tema principal desta lição?", "opcoes": [tema, "Esportes", "Música", "Filmes"], "resposta": tema},
    {"pergunta": "Qual palavra significa 'dar as graças'?", "opcoes": ["Por favor", "Desculpe", "Obrigado", "Com licença"], "resposta": "Obrigado"},
    {"pergunta": "Como se pede ajuda educadamente?", "opcoes": ["Me dê ajuda", "Ajude agora", "Você poderia me ajudar por favor?", "Você deve ajudar"], "resposta": "Você poderia me ajudar por favor?"},
    {"pergunta": "O que significa 'sempre'?", "opcoes": ["Nunca", "Às vezes", "Toda vez", "Raramente"], "resposta": "Toda vez"},
    {"pergunta": "Qual frase está correta?", "opcoes": ["Ele ir para escola", "Ele vai para a escola", "Ele indo para escola", "Ele ido para escola"], "resposta": "Ele vai para a escola"}
]

@st.cache_data
def obter_dados_licao(num_licao):
tema = temas[num_licao - 1]
return {
    "tema": tema,
    "conversas": gerar_conversas(tema),
    "vocabulario": gerar_vocabulario(tema),
    "gramatica": gerar_regras_gramaticais(tema),
    "pronuncia": gerar_oracoes_pronuncia(tema),
    "questionario": gerar_perguntas_questionario(tema)
}

dados_licao = obter_dados_licao(lesson_number)
st.markdown(f"## 📖 Lição {lesson_number}: {dados_licao['tema']}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "🎧 Pronúncia", "❓ Questionário"])

def reproduzir_audio(texto, key):
if not EDGE_TTS_AVAILABLE:
    st.info("🔇 Áudio indisponível – instale edge-tts e nest-asyncio.")
    return
if st.button(f"🔊 Ouvir áudio", key=key):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        try:
            asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, edge_tts.Communicate(texto, "pt-BR-AntonioNeural").save(tmp.name))
                future.result()
        except RuntimeError:
            asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural").save(tmp.name))
        with open(tmp.name, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
        os.unlink(tmp.name)

with tab1:
for i, conv in enumerate(dados_licao["conversas"], 1):
    st.markdown(f"**Conversa {i}**")
    st.text(conv)
    reproduzir_audio(conv, f"conv_{lesson_number}_{i}")
    st.markdown("---")

with tab2:
cols = st.columns(4)
for idx, palavra in enumerate(dados_licao["vocabulario"]):
    with cols[idx % 4]:
        st.markdown(f"**{palavra.capitalize()}**")
        reproduzir_audio(palavra, f"vocab_{lesson_number}_{idx}")

with tab3:
for regra in dados_licao["gramatica"]:
    st.markdown(f"- {regra}")

with tab4:
st.markdown("Ouça cada frase e depois repita em voz alta.")
for idx, oracao in enumerate(dados_licao["pronuncia"]):
    st.markdown(f"**Frase {idx+1}:** {oracao}")
    reproduzir_audio(oracao, f"pron_{lesson_number}_{idx}")
    st.markdown("---")

with tab5:
st.markdown("Teste sua compreensão desta lição.")
if f"quiz_answers_{lesson_number}" not in st.session_state:
    st.session_state[f"quiz_answers_{lesson_number}"] = {}
pontuacao = 0
for q_idx, q in enumerate(dados_licao["questionario"]):
    st.markdown(f"**{q_idx+1}. {q['pergunta']}**")
    resposta = st.radio(" ", q["opcoes"], key=f"quiz_{lesson_number}_{q_idx}", label_visibility="hidden")
    st.session_state[f"quiz_answers_{lesson_number}"][q_idx] = resposta
    if resposta == q["resposta"]:
        pontuacao += 1
if st.button("Verificar respostas", key=f"check_{lesson_number}"):
    st.success(f"Você acertou {pontuacao} de {len(dados_licao['questionario'])}!")
    if pontuacao == len(dados_licao["questionario"]):
        st.balloons()
        st.markdown("🎉 Perfeito! Você dominou esta lição.")

if lesson_number == 20:
st.markdown("---")
st.markdown("## 🎓 Parabéns! Você completou o Livro 1.")
st.markdown("""
### 📞 Para continuar com o Livro 2, entre em contato:
- **Gesner Deslandes** – Fundador
- 📱 WhatsApp: (509) 4738-5663
- 📧 Email: deslandes78@gmail.com
- 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)

O Livro 2 terá conversas mais avançadas, vocabulário, gramática e simulações da vida real.
""")
