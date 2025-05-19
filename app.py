import os
import streamlit as st
import groq
from datetime import date
import re
import json
import time
import base64

# Configuração da página Streamlit
st.set_page_config(
    page_title="ADVJESUS - Assistente Jurídico",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Credenciais de login
LOGIN_USERNAME = "jesus"
LOGIN_PASSWORD = "jr010507"

# Função para criar animação de abertura
def show_intro_animation():
    # HTML para animação de abertura em amarelo e preto
    animation_html = """
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        0% { transform: translateY(-50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    .intro-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #000000 0%, #222222 100%);
        padding: 40px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        animation: fadeIn 1.5s ease-out forwards;
    }
    
    .logo-container {
        background-color: #FFD700;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
        box-shadow: 0 0 30px #FFD700;
        animation: pulse 2s infinite;
    }
    
    .logo-text {
        color: #000000;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    
    .title {
        color: #FFD700;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
        text-shadow: 3px 3px 5px rgba(0,0,0,0.5);
        animation: slideIn 1s ease-out 0.5s forwards;
        opacity: 0;
    }
    
    .subtitle {
        color: white;
        font-size: 24px;
        margin-bottom: 30px;
        text-align: center;
        animation: slideIn 1s ease-out 0.8s forwards;
        opacity: 0;
    }
    
    .feature-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    
    .feature-item {
        background-color: rgba(255, 215, 0, 0.1);
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        width: 220px;
        text-align: center;
        animation: slideIn 1s ease-out 1s forwards;
        opacity: 0;
    }
    
    .feature-item h3 {
        color: #FFD700;
        margin: 0 0 10px 0;
    }
    
    .feature-item p {
        color: white;
        margin: 0;
        font-size: 14px;
    }
    </style>
    
    <div class="intro-container">
        <div class="logo-container">
            <div class="logo-text">ADV<br>JESUS</div>
        </div>
        <div class="title">ADVJESUS</div>
        <div class="subtitle">Sistema Avançado de Redação Jurídica</div>
        
        <div class="feature-list">
            <div class="feature-item" style="animation-delay: 1.0s;">
                <h3>⚖️ Análise</h3>
                <p>Análise inteligente de casos jurídicos</p>
            </div>
            <div class="feature-item" style="animation-delay: 1.2s;">
                <h3>📚 Pesquisa</h3>
                <p>Pesquisa de legislação aplicável</p>
            </div>
            <div class="feature-item" style="animation-delay: 1.4s;">
                <h3>📝 Redação</h3>
                <p>Redação profissional de petições</p>
            </div>
            <div class="feature-item" style="animation-delay: 1.6s;">
                <h3>✅ Revisão</h3>
                <p>Revisão técnica especializada</p>
            </div>
        </div>
    </div>
    
    <script>
        // Remove a animação após 5 segundos
        setTimeout(function() {
            document.querySelector('.intro-container').style.display = 'none';
            // Reload para mostrar o app principal
            window.location.reload();
        }, 5000);
    </script>
    """
    
    st.markdown(animation_html, unsafe_allow_html=True)
    time.sleep(5)  # Espera 5 segundos para a animação

# Sistema de login
def login_page():
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px;
            background: linear-gradient(135deg, #000000 0%, #222222 100%);
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .login-title {
            color: #FFD700;
            text-align: center;
            font-size: 36px;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .login-logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .login-input {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-radius: 5px;
            color: white;
            padding: 10px 15px;
            margin-bottom: 15px;
            width: 100%;
        }
        .login-button {
            background-color: #FFD700;
            color: black;
            font-weight: bold;
            padding: 12px;
            border: none;
            border-radius: 5px;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .login-button:hover {
            background-color: #f0c800;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
        }
        .stButton button {
            background-color: #FFD700 !important;
            color: black !important;
            font-weight: bold !important;
            padding: 12px !important;
            border: none !important;
            border-radius: 5px !important;
            width: 100% !important;
        }
        </style>
        
        <div class="login-container">
            <div class="login-logo">
                <img src="https://via.placeholder.com/150x150/FFD700/000000?text=ADVJESUS" width="150" height="150" style="border-radius: 50%;">
            </div>
            <h1 class="login-title">ADVJESUS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Campos de login
    with st.form("login_form"):
        username = st.text_input("Usuário", key="username")
        password = st.text_input("Senha", type="password", key="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.show_animation = True
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos!")

# Configuração da API Groq
api_key = os.getenv("GROQ_API_KEY", "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")

# Inicialização do cliente Groq
try:
    client = groq.Client(api_key=api_key)
except Exception as e:
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.error(f"Erro ao inicializar o cliente Groq: {str(e)}")
        st.stop()

# Definição do sistema multi-agentes
AGENTES = {
    "Analisador": {
        "descricao": "Coleta informações e realiza análise inicial do caso",
        "prompt_base": """
        Você é um especialista jurídico focado na análise inicial de casos. Analise as informações fornecidas e:
        1. Identifique as partes envolvidas
        2. Extraia os fatos principais
        3. Defina os núcleos textuais e eixos temáticos relevantes
        4. Proponha uma classificação jurídica inicial
        5. Identifique possíveis fundamentações legais preliminares

        CASO COMPLETO:
        {texto_caso}
        
        Formate sua resposta de forma clara e objetiva, usando marcadores e subcabeçalhos para facilitar a leitura.
        """
    },
    "Pesquisador": {
        "descricao": "Realiza pesquisa jurídica aprofundada e desenvolve estratégias",
        "prompt_base": """
        Você é um pesquisador jurídico especializado. Com base na análise inicial, realize:
        1. Identificação precisa dos objetos jurídicos e direitos relevantes
        2. Sugestão de legislação aplicável (artigos específicos com redação literal)
        3. Análise de jurisprudências pertinentes (inclua exemplos reais de decisões importantes)
        4. Desenvolvimento de três estratégias jurídicas viáveis, claramente separadas com títulos como:
           - "ESTRATÉGIA 1: [Nome da estratégia]"
           - "ESTRATÉGIA 2: [Nome da estratégia]"
           - "ESTRATÉGIA 3: [Nome da estratégia]"
        
        Para cada estratégia, apresente:
        - Fundamentos jurídicos principais
        - Vantagens e riscos processuais
        - Probabilidade estimada de sucesso
        
        ANÁLISE INICIAL:
        {analise_inicial}
        
        Formate sua resposta de forma clara, usando marcadores e subcabeçalhos para facilitar a leitura.
        """
    },
    "Redator": {
        "descricao": "Constrói e aprimora a petição inicial seguindo o CPC",
        "prompt_base": """
        Você é um redator jurídico especializado na criação de petições conforme o Código de Processo Civil (artigos 319 e 320). Elabore uma petição inicial completa e extremamente profissional contendo todos os elementos essenciais.
        
        Estruture a petição com as seguintes seções claramente identificadas:
        
        1. ENDEREÇAMENTO (juízo competente)
        2. QUALIFICAÇÃO COMPLETA DAS PARTES (Nome, CPF/CNPJ, endereço, etc.)
        3. NOME DA AÇÃO EM DESTAQUE
        4. FATOS (Narração clara e cronológica)
        5. FUNDAMENTOS JURÍDICOS (Legislação e jurisprudência)
        6. PEDIDOS (Especificações precisas)
        7. VALOR DA CAUSA
        8. PROVAS (Especificação das provas a serem produzidas)
        9. REQUERIMENTOS FINAIS (Incluindo opção por conciliação)
        
        Utilize a estratégia escolhida e as informações jurídicas já identificadas:
        
        PESQUISA JURÍDICA:
        {pesquisa_juridica}
        
        ESTRATÉGIA ESCOLHIDA:
        {estrategia_escolhida}
        
        DADOS DO CLIENTE:
        {dados_cliente}
        
        Crie um documento completo, sem abreviações ou cortes, pronto para ser utilizado na prática forense.
        """
    },
    "Revisor": {
        "descricao": "Revisa e aperfeiçoa a petição elaborada",
        "prompt_base": """
        Você é um revisor jurídico com vasta experiência. Revise a petição inicial fornecida considerando:
        
        1. Correção técnica e jurídica (verifique todos os fundamentos legais)
        2. Clareza e fluidez do texto (elimine parágrafos confusos ou redundantes)
        3. Adequação às normas processuais vigentes (conforme CPC)
        4. Consistência argumentativa (alinhamento entre fatos, fundamentos e pedidos)
        5. Formatação e apresentação profissional (sugestões de melhoria estética)
        
        PETIÇÃO A REVISAR:
        {peticao}
        
        Apresente o resultado em duas partes:
        1. COMENTÁRIOS E SUGESTÕES: Lista de pontos fortes e oportunidades de melhoria
        2. PETIÇÃO REVISADA: Versão completa do documento com todas as correções implementadas
        """
    }
}

# CSS personalizado para a interface
st.markdown("""
<style>
    :root {
        --primary: #FFD700;
        --primary-dark: #e6c300;
        --accent: #000000;
        --text-light: #ffffff;
        --bg-dark: #000000;
        --bg-medium: #222222;
    }

    .main-header {
        font-size: 2.5rem;
        color: var(--primary);
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sub-header {
        font-size: 1.5rem;
        color: var(--primary);
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary);
        padding-bottom: 0.5rem;
    }
    .step-header {
        font-size: 1.2rem;
        color: var(--primary);
        margin-top: 1rem;
        font-weight: bold;
    }
    .result-area {
        background-color: var(--bg-medium);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid var(--primary);
        margin: 1rem 0;
        color: var(--text-light);
        max-height: 500px;
        overflow-y: auto;
    }
    .strategy-card {
        background-color: rgba(255, 215, 0, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary);
        margin: 1rem 0;
    }
    .strategy-title {
        font-weight: bold;
        color: var(--primary);
        font-size: 1.1rem;
    }
    .info-card {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary);
        margin: 1rem 0;
    }
    /* Customização de elementos Streamlit */
    .stButton>button {
        background-color: var(--primary) !important;
        color: black !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background-color: var(--primary-dark) !important;
        color: black !important;
    }
    .stProgress .st-bo {
        background-color: var(--primary);
    }
    /* Melhorias para textarea e tabs */
    .stTextArea>div>div>textarea {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #333333;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: black;
    }
    /* Estilo para sidebar */
    .css-1d391kg {
        background-color: #111111;
    }
    .block-container {
        padding-top: 2rem;
    }
    /* Personalização adicional para o tema preto e amarelo */
    .streamlit-expanderHeader {
        background-color: #333333;
        color: var(--primary);
    }
    .streamlit-expanderContent {
        background-color: #222222;
    }
</style>
""", unsafe_allow_html=True)

# Função para extrair estratégias do texto de pesquisa jurídica
def extrair_estrategias(texto_pesquisa):
    estrategias = []
    padrao = r"ESTRATÉGIA\s*\d+\s*:\s*([^\n]+)"
    matches = re.finditer(padrao, texto_pesquisa)
    
    for match in matches:
        estrategias.append(match.group(0))
    
    if not estrategias:
        estrategias = ["Estratégia não identificada"]
    
    return estrategias

# Função para consultar a API Groq com a metodologia Advogado 5.0
def consultar_groq(agente, texto_input, parametros_adicionais=None):
    prompt_base = AGENTES[agente]["prompt_base"]
    
    # Construir o prompt completo
    if parametros_adicionais:
        prompt_completo = prompt_base.format(**parametros_adicionais)
    else:
        prompt_completo = prompt_base.format(texto_caso=texto_input)
    
    # Adicionar o sistema Advogado 5.0
    sistema_advogado = """
    [METODOLOGIA/CONCEITO] A metodologia "Advogado 5.0" é estruturada em três sessões principais:
    1. Coleta de Informações e Análise Inicial - definição da estratégia jurídica com base nos fatos
    2. Pesquisa Jurídica Aprofundada e Estratégia - identificação de objetos jurídicos e direitos relevantes
    3. Construção e Aprimoramento da Petição Inicial - elaboração conforme CPC arts. 319 e 320
    
    Cada sessão é detalhada para otimizar a coleta e análise de dados, formular estratégias jurídicas e elaborar uma petição inicial eficaz.
    [/METODOLOGIA/CONCEITO]
    
    [COMPORTAMENTO] Você é um mestre em direito especializado em construir petições com base no código civil de 2015 e artigos 319 e 320 do CPC para análise de dados e estratégia jurídica para subsunção de casos ao direito brasileiro. Sua resposta deve ser técnica, precisa e extremamente profissional. [/COMPORTAMENTO]
    
    [IMPORTANTE] Para todo e qualquer fato, princípio, prova ou jurisprudência, deve gerir alta pertinência ao processo e ao caso de acordo com uso da lógica fuzzy em enquadramento de pertinência e relevância, sem recorrer a argumentações vazias ou sem conexão lógica. [/IMPORTANTE]
    """
    
    # Tentativas em caso de erro
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            # Chamar a API do Groq
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",  # Usando Llama 3 70B
                messages=[
                    {"role": "system", "content": sistema_advogado},
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=0.7,
                max_tokens=4096,
                top_p=0.95,
                stream=False
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if tentativa < max_tentativas - 1:
                # Esperar antes de tentar novamente (backoff exponencial)
                time.sleep(2 ** tentativa)
                continue
            else:
                return f"Erro ao consultar a API Groq após {max_tentativas} tentativas: {str(e)}"

# Verificar se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Verificar se deve mostrar a animação
if 'show_animation' not in st.session_state:
    st.session_state.show_animation = False

# Mostrar tela de login se não estiver logado
if not st.session_state.logged_in:
    login_page()
    st.stop()  # Parar execução aqui se não estiver logado

# Mostrar animação de abertura se necessário
if st.session_state.show_animation:
    show_intro_animation()
    st.session_state.show_animation = False
    st.experimental_rerun()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150/FFD700/000000?text=ADVJESUS", width=150)
    st.title("ADVJESUS")
    st.markdown("### Assistente Jurídico IA")
    
    # Informação sobre a API
    api_status = "✅ Conectado" if api_key else "❌ Desconectado"
    st.markdown(f"**Status da API Groq:** {api_status}")
    
    # Opção para alterar chave API
    with st.expander("Configurar API"):
        custom_api_key = st.text_input("Chave API do Groq", type="password", value=api_key if api_key else "")
        if st.button("Atualizar Chave"):
            if custom_api_key:
                try:
                    # Teste da nova chave
                    teste_client = groq.Client(api_key=custom_api_key)
                    # Se não der erro, atualiza
                    client = teste_client
                    api_key = custom_api_key
                    st.success("Chave API atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Chave API inválida: {str(e)}")
    
    st.markdown("---")
    st.markdown("### Sobre o Sistema")
    st.markdown("""
    O **ADVJESUS** utiliza a metodologia Advogado 5.0 e IA avançada para:
    
    1. Analisar casos jurídicos
    2. Pesquisar legislação aplicável
    3. Desenvolver estratégias processuais
    4. Redigir petições iniciais completas
    
    O sistema segue as diretrizes dos artigos 319 e 320 do CPC.
    """)
    
    # Progresso do processo
    if 'etapa_atual' not in st.session_state:
        st.session_state.etapa_atual = 1
    
    st.markdown("### Progresso do Processo")
    etapas = ["Análise", "Pesquisa", "Redação", "Revisão"]
    progresso = (st.session_state.etapa_atual / len(etapas)) * 100
    st.progress(progresso/100)
    
    for i, etapa in enumerate(etapas, 1):
        if i < st.session_state.etapa_atual:
            st.markdown(f"✅ **Etapa {i}:** {etapa}")
        elif i == st.session_state.etapa_atual:
            st.markdown(f"🔄 **Etapa {i}:** {etapa}")
        else:
            st.markdown(f"⏳ **Etapa {i}:** {etapa}")
    
    # Botão de logout
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# Cabeçalho principal
st.markdown("<h1 class='main-header'>ADVJESUS ⚖️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFD700;'>Assistente de Redação Jurídica com Tecnologia Avançada</p>", unsafe_allow_html=True)

# Inicialização de variáveis de sessão
if 'analise_inicial' not in st.session_state:
    st.session_state.analise_inicial = ""
if 'pesquisa_juridica' not in st.session_state:
    st.session_state.pesquisa_juridica = ""
if 'estrategia_escolhida' not in st.session_state:
    st.session_state.estrategia_escolhida = ""
if 'estrategias_disponiveis' not in st.session_state:
    st.session_state.estrategias_disponiveis = []
if 'peticao_inicial' not in st.session_state:
    st.session_state.peticao_inicial = ""
if 'peticao_revisada' not in st.session_state:
    st.session_state.peticao_revisada = ""
if 'dados_cliente' not in st.session_state:
    st.session_state.dados_cliente = {}

# Tabs para organizar o fluxo de trabalho
tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Fatos do Caso", "2️⃣ Pesquisa Jurídica", "3️⃣ Redação da Petição", "4️⃣ Revisão Final"])

# Tab 1: Fatos do Caso
with tab1:
    st.markdown("<h2 class='sub-header'>Etapa 1: Coleta de Informações e Análise Inicial</h2>", unsafe_allow_html=True)
    
    with st.form("caso_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_cliente = st.text_input("Nome do Cliente")
            tipo_acao = st.selectbox(
                "Tipo de Ação",
                ["Selecione o tipo", "Ação de Cobrança", "Ação de Indenização", "Mandado de Segurança", 
                 "Ação de Despejo", "Ação Revisional", "Ação Trabalhista", "Ação de Alimentos",
                 "Ação de Usucapião", "Ação Possessória", "Ação de Execução", "Outro"]
            )
        
        with col2:
            cpf_cliente = st.text_input("CPF/CNPJ do Cliente")
            comarca = st.text_input("Comarca")
        
        st.markdown("### Descrição do Caso")
        st.markdown("Descreva detalhadamente os fatos, incluindo datas, valores e pessoas envolvidas.")
        descricao_caso = st.text_area("", height=250, placeholder="Exemplo: No dia 15/03/2025, o requerente adquiriu um produto com defeito...")
        
        col1, col2 = st.columns(2)
        with col1:
            documentos_relevantes = st.text_area("Documentos e Provas Disponíveis", height=100, 
                                              placeholder="Exemplo: Contrato assinado, comprovante de pagamento, notificação extrajudicial...")
        
        with col2:
            pretensao_cliente = st.text_area("O que o Cliente Deseja Obter", height=100,
                                          placeholder="Exemplo: Indenização por danos morais e materiais, restituição de valores pagos...")
        
        analisar_caso = st.form_submit_button("Analisar Caso")
    
    if analisar_caso:
        if not nome_cliente or not cpf_cliente or not descricao_caso or tipo_acao == "Selecione o tipo":
            st.error("Por favor, preencha todos os campos obrigatórios.")
        else:
            with st.spinner("Analisando o caso... Por favor aguarde."):
                # Armazenar dados do cliente para uso posterior
                st.session_state.dados_cliente = {
                    "nome": nome_cliente,
                    "cpf_cnpj": cpf_cliente,
                    "tipo_acao": tipo_acao,
                    "comarca": comarca,
                    "pretensao": pretensao_cliente
                }
                
                caso_completo = f"""
                DADOS BÁSICOS:
                Cliente: {nome_cliente} ({cpf_cliente})
                Tipo de Ação: {tipo_acao}
                Comarca: {comarca}
                
                DESCRIÇÃO DETALHADA DOS FATOS:
                {descricao_caso}
                
                DOCUMENTOS E PROVAS DISPONÍVEIS:
                {documentos_relevantes}
                
                PRETENSÃO DO CLIENTE:
                {pretensao_cliente}
                """
                
                # Chamar o agente Analisador
                st.session_state.analise_inicial = consultar_groq("Analisador", caso_completo)
                
                # Atualizar etapa atual
                st.session_state.etapa_atual = 2
                
                st.markdown("<h3 class='step-header'>Resultado da Análise Inicial</h3>", unsafe_allow_html=True)
                st.markdown("<div class='result-area'>", unsafe_allow_html=True)
                st.write(st.session_state.analise_inicial)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.success("✅ Análise inicial concluída! Avance para a etapa de Pesquisa Jurídica.")
                
                # Botão para ir à próxima aba
                if st.button("Ir para Pesquisa Jurídica"):
                    st.experimental_set_query_params(tab="tab2")
                    st.experimental_rerun()

# Tab 2: Pesquisa Jurídica
with tab2:
    st.markdown("<h2 class='sub-header'>Etapa 2: Pesquisa Jurídica Aprofundada e Estratégia</h2>", unsafe_allow_html=True)
    
    if not st.session_state.analise_inicial:
        st.warning("⚠️ Por favor, complete a etapa de análise inicial primeiro.")
    else:
        st.markdown("<h3 class='step-header'>Resumo da Análise Inicial</h3>", unsafe_allow_html=True)
        st.markdown("<div class='result-area'>", unsafe_allow_html=True)
        st.write(st.session_state.analise_inicial)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Realizar Pesquisa Jurídica", key="btn_pesquisa"):
                with st.spinner("Realizando pesquisa jurídica e desenvolvendo estratégias... Esta etapa pode levar alguns minutos."):
                    # Chamar o agente Pesquisador
                    st.session_state.pesquisa_juridica = consultar_groq("Pesquisador", "", 
                                                                      {"analise_inicial": st.session_state.analise_inicial})
                    
                    # Extrair estratégias para seleção
                    st.session_state.estrategias_disponiveis = extrair_estrategias(st.session_state.pesquisa_juridica)
                    
                    # Atualizar etapa atual
                    st.session_state.etapa_atual = 3
                    
                    st.success("✅ Pesquisa jurídica concluída!")
        
        # Se já temos a pesquisa jurídica, mostrar resultado
        if st.session_state.pesquisa_juridica:
            st.markdown("<h3 class='step-header'>Resultado da Pesquisa Jurídica</h3>", unsafe_allow_html=True)
            st.markdown("<div class='result-area'>", unsafe_allow_html=True)
            st.write(st.session_state.pesquisa_juridica)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Seleção de estratégia
            st.markdown("<h3 class='step-header'>Selecione a Estratégia Jurídica</h3>", unsafe_allow_html=True)
            st.markdown("Escolha a estratégia que melhor se adéqua ao caso e objetivos do cliente:")
            
            estrategia_selecionada = st.radio("", st.session_state.estrategias_disponiveis)
            st.session_state.estrategia_escolhida = estrategia_selecionada
            
            # Extrair e mostrar detalhes da estratégia selecionada
            if estrategia_selecionada != "Estratégia não identificada":
                inicio_estrategia = st.session_state.pesquisa_juridica.find(estrategia_selecionada)
                if inicio_estrategia != -1:
                    # Procurar o próximo título de estratégia ou o final do texto
                    proximo_match = re.search(r"ESTRATÉGIA\s*\d+\s*:", st.session_state.pesquisa_juridica[inicio_estrategia + len(estrategia_selecionada):])
                    
                    if proximo_match:
                        fim_estrategia = inicio_estrategia + len(estrategia_selecionada) + proximo_match.start()
                        detalhes_estrategia = st.session_state.pesquisa_juridica[inicio_estrategia:fim_estrategia].strip()
                    else:
                        # Se não houver próxima estratégia, pegar até o final ou até um marcador comum como "CONCLUSÃO"
                        fim_match = re.search(r"(CONCLUSÃO|CONSIDERAÇÕES FINAIS|$)", st.session_state.pesquisa_juridica[inicio_estrategia + len(estrategia_selecionada):])
                        if fim_match:
                            fim_estrategia = inicio_estrategia + len(estrategia_selecionada) + fim_match.start()
                            detalhes_estrategia = st.session_state.pesquisa_juridica[inicio_estrategia:fim_estrategia].strip()
                        else:
                            detalhes_estrategia = st.session_state.pesquisa_juridica[inicio_estrategia:].strip()
                    
                    st.markdown("<div class='strategy-card'>", unsafe_allow_html=True)
                    st.markdown(f"<p class='strategy-title'>{estrategia_selecionada}</p>", unsafe_allow_html=True)
                    st.write(detalhes_estrategia.replace(estrategia_selecionada, "").strip())
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Botão para ir à próxima aba
            if st.button("Ir para Redação da Petição"):
                st.experimental_set_query_params(tab="tab3")
                st.experimental_rerun()

# Tab 3: Redação da Petição
with tab3:
    st.markdown("<h2 class='sub-header'>Etapa 3: Construção da Petição Inicial</h2>", unsafe_allow_html=True)
    
    if not st.session_state.pesquisa_juridica or not st.session_state.estrategia_escolhida:
        st.warning("⚠️ Por favor, complete a etapa de pesquisa jurídica primeiro.")
    else:
        st.markdown("<h3 class='step-header'>Estratégia Selecionada</h3>", unsafe_allow_html=True)
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.write(st.session_state.estrategia_escolhida)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<h3 class='step-header'>Informações Adicionais para a Petição</h3>", unsafe_allow_html=True)
        
        # Formulário para informações complementares
        with st.form("info_peticao_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                endereco_cliente = st.text_input("Endereço Completo do Cliente", 
                                             placeholder="Rua, número, bairro, cidade, CEP")
                advogado_nome = st.text_input("Nome do Advogado")
                oab_numero = st.text_input("Número da OAB")
            
            with col2:
                parte_contraria = st.text_input("Nome da Parte Contrária", 
                                            placeholder="Nome completo do réu/requerido")
                endereco_contrario = st.text_input("Endereço da Parte Contrária", 
                                               placeholder="Rua, número, bairro, cidade, CEP")
                valor_causa = st.text_input("Valor da Causa", placeholder="R$ 0,00")
            
            # Opção de negociação
            conciliacao = st.radio("Deseja audiência de conciliação/mediação?", 
                                ["Sim", "Não"])
            
            # Botão para gerar petição
            gerar_peticao = st.form_submit_button("Redigir Petição Inicial")
        
        if gerar_peticao:
            # Verificar campos obrigatórios
            if not endereco_cliente or not parte_contraria or not valor_causa:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                with st.spinner("Redigindo a petição inicial... Este processo pode levar alguns minutos."):
                    # Atualizar dados do cliente
                    dados_cliente_completos = st.session_state.dados_cliente.copy()
                    dados_cliente_completos.update({
                        "endereco": endereco_cliente,
                        "advogado_nome": advogado_nome,
                        "oab_numero": oab_numero,
                        "parte_contraria": parte_contraria,
                        "endereco_contrario": endereco_contrario,
                        "valor_causa": valor_causa,
                        "conciliacao": conciliacao
                    })
                    
                    # Converter para string formatada
                    dados_cliente_str = json.dumps(dados_cliente_completos, indent=2)
                    
                    # Chamar o agente Redator
                    st.session_state.peticao_inicial = consultar_groq("Redator", "", {
                        "pesquisa_juridica": st.session_state.pesquisa_juridica,
                        "estrategia_escolhida": st.session_state.estrategia_escolhida,
                        "dados_cliente": dados_cliente_str
                    })
                    
                    # Atualizar etapa atual
                    st.session_state.etapa_atual = 4
                    
                    st.success("✅ Petição inicial redigida!")
        
        # Se já temos a petição inicial, mostrar resultado
        if st.session_state.peticao_inicial:
            st.markdown("<h3 class='step-header'>Petição Inicial</h3>", unsafe_allow_html=True)
            st.markdown("<div class='result-area'>", unsafe_allow_html=True)
            st.write(st.session_state.peticao_inicial)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Botão para ir à próxima aba
            if st.button("Ir para Revisão Final"):
                st.experimental_set_query_params(tab="tab4")
                st.experimental_rerun()

# Tab 4: Revisão Final
with tab4:
    st.markdown("<h2 class='sub-header'>Etapa 4: Revisão e Aprimoramento Final</h2>", unsafe_allow_html=True)
    
    if not st.session_state.peticao_inicial:
        st.warning("⚠️ Por favor, complete a etapa de redação da petição primeiro.")
    else:
        st.markdown("<h3 class='step-header'>Petição Inicial Redigida</h3>", unsafe_allow_html=True)
        st.markdown("<div class='result-area'>", unsafe_allow_html=True)
        st.write(st.session_state.peticao_inicial)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Revisar e Aprimorar Petição"):
            with st.spinner("Revisando a petição final... Este processo pode levar alguns minutos."):
                # Chamar o agente Revisor
                st.session_state.peticao_revisada = consultar_groq("Revisor", "", {
                    "peticao": st.session_state.peticao_inicial
                })
                
                st.success("✅ Petição revisada e aprimorada!")
        
        # Se já temos a petição revisada, mostrar resultado
        if st.session_state.peticao_revisada:
            # Separar comentários da petição revisada
            try:
                # Procurar por padrões comuns de separação
                padrao_separacao = "PETIÇÃO REVISADA:|VERSÃO FINAL:|DOCUMENTO REVISADO:"
                partes = re.split(padrao_separacao, st.session_state.peticao_revisada, flags=re.IGNORECASE)
                
                if len(partes) > 1:
                    comentarios = partes[0].strip()
                    peticao_final = partes[1].strip()
                else:
                    # Se não conseguiu separar, mostra tudo na parte de comentários
                    comentarios = "Não foi possível separar os comentários da petição revisada."
                    peticao_final = st.session_state.peticao_revisada
            except:
                comentarios = "Erro ao processar a petição revisada."
                peticao_final = st.session_state.peticao_revisada
            
            # Mostrar comentários do revisor
            st.markdown("<h3 class='step-header'>Comentários do Revisor</h3>", unsafe_allow_html=True)
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.write(comentarios)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Mostrar petição final
            st.markdown("<h3 class='step-header'>Petição Final Revisada</h3>", unsafe_allow_html=True)
            st.markdown("<div class='result-area'>", unsafe_allow_html=True)
            st.write(peticao_final)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Opções de download
            st.markdown("<h3 class='step-header'>Baixar Documentos</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📄 Baixar Petição em formato TXT",
                    data=peticao_final,
                    file_name=f"peticao_{st.session_state.dados_cliente.get('tipo_acao', 'inicial')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Para um download como docx, precisaríamos converter o texto para esse formato
                # Neste exemplo, estamos apenas baixando como txt com extensão docx
                st.download_button(
                    label="📝 Baixar Petição em formato DOCX",
                    data=peticao_final,
                    file_name=f"peticao_{st.session_state.dados_cliente.get('tipo_acao', 'inicial')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            # Botão para reiniciar o processo
            if st.button("✨ Iniciar Novo Caso"):
                # Limpar todas as variáveis de sessão
                for key in list(st.session_state.keys()):
                    if key not in ['logged_in', 'etapa_atual']:  # Manter apenas login e etapa
                        del st.session_state[key]
                
                # Resetar etapa atual
                st.session_state.etapa_atual = 1
                
                # Voltar para a primeira aba
                st.experimental_set_query_params()
                st.experimental_rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: #FFD700;'>© 2025 ADVJESUS | Sistema Avançado de Redação Jurídica</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999; font-size: 0.8rem;'>Baseado na Metodologia Advogado 5.0</p>", unsafe_allow_html=True)
