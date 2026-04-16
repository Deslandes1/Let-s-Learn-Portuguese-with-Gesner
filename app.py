import streamlit as st
import asyncio
import tempfile
import base64
import os

# ----- Audio Setup (edge-tts) -----
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

# ----- Lesson topics (Portuguese) -----
topics = [
    "Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções",
    "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações",
    "Comprar roupa", "No banco", "Usar transporte público", "Alugar um apartamento", "Celebrar um aniversário",
    "Ir ao cinema", "No ginásio", "Fazer uma chamada", "Escrever um e-mail", "Falar de hobbies"
]

def generate_conversations(topic):
    conv1 = f"A: Olá! Como você está hoje?\nB: Estou bem, obrigado! Estou aprendendo sobre {topic}.\nA: Isso é maravilhoso. Pode me contar mais?\nB: Claro! Eu pratico todos os dias."
    conv2 = f"A: Com licença, você poderia me ajudar com {topic}?\nB: Claro! O que você precisa saber?\nA: Quero melhorar meu português.\nB: Esse é um ótimo objetivo. Continue praticando!"
    conv3 = f"A: Olá, sou novo aqui. Pode explicar {topic}?\nB: Absolutamente! É muito útil para a vida diária.\nA: Muito obrigado!\nB: De nada. Vamos praticar juntos."
    return [conv1, conv2, conv3]

def generate_vocabulary(topic):
    base_words = ["olá", "adeus", "por favor", "obrigado", "sim", "não", "talvez", "sempre", "às vezes", "nunca",
                  "rapidamente", "lentamente", "cuidadosamente", "felizmente", "tristemente", "em voz alta", "em voz baixa", "brilhantemente", "escuramente", "suavemente"]
    topic_words = [topic.lower().replace(" ", "_") + str(i) for i in range(1, 6)]
    all_words = base_words[:15] + topic_words
    return all_words[:20]

def get_grammar_rules():
    return [
        {
            "rule": "1. Use o presente simples para fatos e rotinas.",
            "examples": [
                "Eu trabalho todos os dias.",
                "Ela estuda português.",
                "O sol nasce de manhã."
            ]
        },
        {
            "rule": "2. Use 'ser' e 'estar' corretamente (características permanentes vs. estados temporários).",
            "examples": [
                "Ela é inteligente. (permanente)",
                "Hoje estou cansado. (temporário)",
                "A mesa é de madeira. (permanente)"
            ]
        },
        {
            "rule": "3. Use 'ter' para posse e idade.",
            "examples": [
                "Eu tenho um carro novo.",
                "Eles têm dois filhos.",
                "Minha irmã tem 25 anos."
            ]
        },
        {
            "rule": "4. Use 'poder' para habilidade ou permissão.",
            "examples": [
                "Eu posso falar português.",
                "Posso abrir a janela?",
                "Ela não pode vir hoje."
            ]
        },
        {
            "rule": "5. Use 'fazer' para perguntar sobre o clima (Que tempo faz?).",
            "examples": [
                "Que tempo faz hoje?",
                "Faz muito calor no verão.",
                "Faz vento na praia."
            ]
        },
        {
            "rule": "6. Os advérbios de frequência (sempre, às vezes, nunca) vêm antes do verbo principal.",
            "examples": [
                "Eu sempre tomo café às 8.",
                "Às vezes vou ao cinema.",
                "Nunca chego atrasado."
            ]
        },
        {
            "rule": "7. Use preposições de lugar (em, sobre, debaixo de) corretamente.",
            "examples": [
                "O livro está na mesa.",
                "A lâmpada está sobre a mesa.",
                "O gato está debaixo da cadeira."
            ]
        },
        {
            "rule": "8. Use 'há' para dizer que algo existe.",
            "examples": [
                "Há um restaurante perto.",
                "Há muitas pessoas aqui.",
                "Há leite no frigorífico?"
            ]
        },
        {
            "rule": "9. Use 'gostaria de' para pedidos educados.",
            "examples": [
                "Gostaria de um café, por favor.",
                "Gostaria de visitar Portugal.",
                "Gostaria de aprender mais."
            ]
        },
        {
            "rule": "10. Use 'ir + infinitivo' para planos futuros.",
            "examples": [
                "Vou viajar amanhã.",
                "Eles vão comer pizza.",
                "Vais estudar esta noite?"
            ]
        }
    ]

def generate_pronunciation_sentences(topic):
    return [
        f"Estou aprendendo sobre {topic} hoje.",
        f"Você poderia explicar {topic} para mim, por favor?",
        f"Praticar {topic} me ajuda a melhorar meu português.",
        f"Vamos falar sobre {topic} juntos.",
        f"Entender {topic} é muito útil."
    ]

def generate_quiz_questions(topic):
    return [
        {"question": "Qual é o tema principal desta lição?", "options": [topic, "Desportos", "Música", "Filmes"], "answer": topic},
        {"question": "Qual palavra significa 'agradecer'?", "options": ["Por favor", "Desculpe", "Obrigado", "Com licença"], "answer": "Obrigado"},
        {"question": "Como se pede ajuda educadamente?", "options": ["Dá-me ajuda", "Ajuda agora", "Pode ajudar-me, por favor?", "Deves ajudar"], "answer": "Pode ajudar-me, por favor?"},
        {"question": "O que significa 'sempre'?", "options": ["Nunca", "Às vezes", "Cada vez", "Raramente"], "answer": "Cada vez"},
        {"question": "Qual frase está correta?", "options": ["Ele ir à escola", "Ele vai à escola", "Ele indo à escola", "Ele ido à escola"], "answer": "Ele vai à escola"}
    ]

@st.cache_data
def get_lesson_data(num_lesson):
    topic = topics[num_lesson - 1]
    return {
        "topic": topic,
        "conversations": generate_conversations(topic),
        "vocabulary": generate_vocabulary(topic),
        "grammar": get_grammar_rules(),
        "pronunciation": generate_pronunciation_sentences(topic),
        "quiz": generate_quiz_questions(topic)
    }

lesson_data = get_lesson_data(lesson_number)
st.markdown(f"## 📖 Lição {lesson_number}: {lesson_data['topic']}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "🎧 Pronúncia", "❓ Questionário"])

# ----- Audio function (Brazilian Portuguese voice) -----
async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "pt-BR-FranciscaNeural")
    await communicate.save(file_path)

def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desativado. Instale edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(text, tmp.name))
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro de áudio: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ----- TAB 1: CONVERSAS -----
with tab1:
    for i, conv in enumerate(lesson_data["conversations"], 1):
        st.markdown(f"**Conversa {i}**")
        st.text(conv)
        play_audio(conv, f"conv_{lesson_number}_{i}")
        st.markdown("---")

# ----- TAB 2: VOCABULÁRIO -----
with tab2:
    cols = st.columns(4)
    for idx, word in enumerate(lesson_data["vocabulary"]):
        with cols[idx % 4]:
            st.markdown(f"**{word.capitalize()}**")
            play_audio(word, f"vocab_{lesson_number}_{idx}")

# ----- TAB 3: GRAMÁTICA -----
with tab3:
    st.subheader("💡 Regras Gramaticais (com exemplos e áudio)")
    for idx, item in enumerate(lesson_data["grammar"]):
        st.markdown(f"**{item['rule']}**")
        play_audio(item['rule'], f"gram_rule_{lesson_number}_{idx}")
        st.markdown("**Exemplos:**")
        for ex_idx, ex in enumerate(item['examples']):
            col_ex, col_btn = st.columns([4, 1])
            col_ex.write(f"• {ex}")
            with col_btn:
                play_audio(ex, f"gram_ex_{lesson_number}_{idx}_{ex_idx}")
        st.markdown("---")
    
    st.markdown("---")
    st.subheader("🌟 O Básico")
    with st.expander("🔤 O Alfabeto Português", expanded=True):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Note: Portuguese alphabet has 26 letters (no Ñ, but includes K, W, Y)
        cols = st.columns(7)
        for i, letter in enumerate(alphabet):
            with cols[i % 7]:
                st.write(f"### {letter}")
                play_audio(letter, f"alpha_{letter}_{lesson_number}")

    with st.expander("🔢 Números (Cardinais e Ordinais)"):
        st.markdown("**Números Cardinais (1 a 10)**")
        cardinals = [
            ("1", "um"), ("2", "dois"), ("3", "três"), ("4", "quatro"),
            ("5", "cinco"), ("6", "seis"), ("7", "sete"), ("8", "oito"),
            ("9", "nove"), ("10", "dez")
        ]
        cols_card = st.columns(5)
        for idx, (num, word) in enumerate(cardinals):
            with cols_card[idx % 5]:
                st.write(f"**{num}** – {word}")
                play_audio(word, f"card_{num}_{lesson_number}")
        
        st.markdown("---")
        st.markdown("**Números Ordinais (1º ao 10º)**")
        ordinals = [
            ("1º", "primeiro"), ("2º", "segundo"), ("3º", "terceiro"), ("4º", "quarto"),
            ("5º", "quinto"), ("6º", "sexto"), ("7º", "sétimo"), ("8º", "oitavo"),
            ("9º", "nono"), ("10º", "décimo")
        ]
        cols_ord = st.columns(5)
        for idx, (num, word) in enumerate(ordinals):
            with cols_ord[idx % 5]:
                st.write(f"**{num}** – {word}")
                play_audio(word, f"ord_{num}_{lesson_number}")

    with st.expander("🗣️ Expressões Idiomáticas Top"):
        idioms = [
            {"phrase": "Chover no molhado", "meaning": "Dizer algo já sabido, repetir o óbvio."},
            {"phrase": "Pagar o pato", "meaning": "Ser culpado por algo que não fez."},
            {"phrase": "Ter olho grande", "meaning": "Ser ganancioso ou cobiçar algo."}
        ]
        for idx, item in enumerate(idioms):
            st.markdown(f"**{item['phrase']}**")
            st.caption(item['meaning'])
            play_audio(f"{item['phrase']}. Significa: {item['meaning']}", f"idiom_{idx}_{lesson_number}")
            st.markdown("---")

# ----- TAB 4: PRONÚNCIA -----
with tab4:
    st.markdown("Ouça cada frase e repita em voz alta.")
    for idx, sentence in enumerate(lesson_data["pronunciation"]):
        st.markdown(f"**Frase {idx+1}:** {sentence}")
        play_audio(sentence, f"pron_{lesson_number}_{idx}")
        st.markdown("---")

# ----- TAB 5: QUESTIONÁRIO (com áudio para perguntas, opções e respostas corretas) -----
with tab5:
    st.markdown("Teste a sua compreensão desta lição.")
    
    quiz_key = f"quiz_answers_{lesson_number}"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = {}
    
    questions = lesson_data["quiz"]
    
    for q_idx, q in enumerate(questions):
        st.markdown(f"**{q_idx+1}. {q['question']}**")
        play_audio(q['question'], f"quiz_question_{lesson_number}_{q_idx}")
        
        selected = st.session_state[quiz_key].get(q_idx, None)
        for opt_idx, opt in enumerate(q['options']):
            col_text, col_audio = st.columns([5, 1])
            with col_text:
                if st.button(opt, key=f"select_{lesson_number}_{q_idx}_{opt_idx}"):
                    st.session_state[quiz_key][q_idx] = opt
                    st.rerun()
            with col_audio:
                play_audio(opt, f"quiz_opt_{lesson_number}_{q_idx}_{opt_idx}")
            st.markdown("---")
        if selected:
            st.success(f"Selecionado: {selected}")
        else:
            st.info("Você ainda não selecionou uma resposta. Clique numa opção acima.")
        st.markdown("---")
    
    if st.button("Verificar respostas", key=f"check_{lesson_number}"):
        score = 0
        for q_idx, q in enumerate(questions):
            if st.session_state[quiz_key].get(q_idx) == q["answer"]:
                score += 1
        st.success(f"Você acertou {score} de {len(questions)}!")
        if score == len(questions):
            st.balloons()
            st.markdown("🎉 Perfeito! Você dominou esta lição.")
        else:
            with st.expander("Ver respostas corretas"):
                for q_idx, q in enumerate(questions):
                    col_text, col_audio = st.columns([5, 1])
                    with col_text:
                        st.write(f"{q_idx+1}. {q['question']} → Resposta correta: {q['answer']}")
                    with col_audio:
                        correct_text = f"{q['question']} Resposta correta: {q['answer']}"
                        play_audio(correct_text, f"correct_ans_{lesson_number}_{q_idx}")

# ----- FIM DO LIVRO -----
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Parabéns! Você completou o Livro 1.")
    st.markdown("""
    ### 📞 Para continuar com o Livro 2, entre em contato:
    - **Gesner Deslandes** – Fundador
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    O Livro 2 conterá conversas mais avançadas, vocabulário, gramática e simulações da vida real.
    """)
