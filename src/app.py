"""
AGENTE FINANCEIRO INTELIGENTE - MetaFinance
Chatbot de Consultoria Financeira com IA Generativa

Autor: Patrick Lima - Certificação DIO
Data: 2026
"""

import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# ===== CONFIGURAÇÃO DE AMBIENTE =====
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Se não encontrou no .env, tenta do Streamlit Secrets (para produção/cloud)
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except:
        api_key = None

@st.cache_resource
def init_gemini():
    """Inicializa o modelo Gemini com cache"""
    try:
        if api_key:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.5-flash')
        else:
            st.warning("⚠️ GOOGLE_API_KEY não configurada. Configure em Streamlit Secrets (produção) ou .env (desenvolvimento)")
            return None
    except Exception as e:
        st.error(f"⚠️ Erro ao conectar Gemini: {str(e)}")
        return None

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="MetaFinance - IA Financeira",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS GLOBAL PREMIUM =====
st.markdown("""
<style>
    /* === RESET === */
    .block-container { padding-top: 1rem; max-width: 1200px; }
    header[data-testid="stHeader"] { background: transparent; }

    /* === SIDEBAR DARK === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
    [data-testid="stSidebar"] .stRadio label { transition: all 0.2s; padding: 3px 0; }
    [data-testid="stSidebar"] .stRadio label:hover { padding-left: 6px; }

    /* === HEADER HERO === */
    .hero {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    @media (max-width: 768px) {
        .hero { flex-direction: column; text-align: center; gap: 1rem; padding: 1.5rem; }
        .hero-left { flex-direction: column; gap: 0.5rem; }
        .hero-badge { 
            order: -1; 
            margin-bottom: 0.5rem; 
            width: 100%;
            text-align: center;
            font-size: 0.78em;
            padding: 0.45rem 0.9rem;
            letter-spacing: 0.8px;
            white-space: normal;
            line-height: 1.2;
            opacity: 0.9;
        }
        .hero-title { font-size: 1.8em; }
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }
    .hero-left { display: flex; align-items: center; gap: 1.2rem; z-index: 1; }
    .hero-icon { font-size: 2.8em; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15)); }
    .hero-title { font-size: 2.2em; font-weight: 800; letter-spacing: -1px; }
    .hero-sub { font-size: 0.95em; opacity: 0.85; margin-top: 2px; }
    .hero-badge {
        background: rgba(255,255,255,0.1);
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.75em;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        z-index: 1;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* === SIDEBAR PROFILE === */
    .sb-profile {
        background: linear-gradient(135deg, rgba(102,126,234,0.25), rgba(118,75,162,0.25));
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1.5rem;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sb-avatar {
        width: 64px; height: 64px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 0.8rem;
        font-size: 1.6em;
        box-shadow: 0 4px 20px rgba(102,126,234,0.5);
        border: 3px solid rgba(255,255,255,0.15);
    }
    .sb-name { font-size: 1.15em; font-weight: 700; color: white !important; }
    .sb-role { font-size: 0.8em; opacity: 0.65; margin-top: 2px; }
    .sb-stats { display: flex; justify-content: space-around; margin-top: 1.2rem; gap: 6px; }
    .sb-stat {
        text-align: center;
        padding: 0.6rem 0.4rem;
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        flex: 1;
    }
    .sb-stat-val { font-size: 0.82em; font-weight: 700; color: #a78bfa !important; }
    .sb-stat-lbl { font-size: 0.68em; opacity: 0.6; margin-top: 3px; }

    /* === METRIC CARDS === */
    .m-card {
        background: white;
        border-radius: 18px;
        padding: 1.4rem;
        text-align: center;
        box-shadow: 0 2px 16px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f5;
        transition: all 0.25s ease;
    }
    .m-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }
    .m-icon { font-size: 2em; margin-bottom: 0.4rem; }
    .m-label { font-size: 0.82em; color: #999; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .m-value { font-size: 1.5em; font-weight: 800; margin: 0.25rem 0; }

    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, rgba(102,126,234,0.07), rgba(118,75,162,0.07));
        border-left: 4px solid #667eea;
        padding: 1.2rem 1.5rem;
        border-radius: 0 14px 14px 0;
        margin-bottom: 1.5rem;
        font-size: 0.95em;
        line-height: 1.7;
    }

    /* === PRODUCT CARD === */
    .p-card {
        background: white;
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f5;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
    }
    .p-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }
    .p-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
    .p-name { font-size: 1.15em; font-weight: 700; color: #333; }
    .p-badge { padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.78em; font-weight: 600; }
    .bg-green { background: #dcfce7; color: #166534; }
    .bg-yellow { background: #fef9c3; color: #854d0e; }
    .bg-red { background: #fee2e2; color: #991b1b; }
    .p-meta { margin-bottom: 1rem; font-size: 0.88em; color: #999; }
    .p-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; }
    @media (max-width: 768px) {
        .p-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .p-stat { text-align: center; padding: 0.8rem 0.4rem; background: #f8f9fc; border-radius: 12px; }
    .p-stat-val { font-size: 1.05em; font-weight: 700; color: #667eea; }
    .p-stat-lbl { font-size: 0.72em; color: #999; margin-top: 3px; }

    /* === SECTION TITLE === */
    .sec-title {
        font-size: 1.25em;
        font-weight: 700;
        color: #333;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f5;
    }

    /* === DIVIDER === */
    .divider { height: 1px; background: linear-gradient(90deg, transparent, #e5e5ea, transparent); margin: 2rem 0; }

    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #bbb;
        font-size: 0.85em;
        border-top: 1px solid #f0f0f5;
        margin-top: 3rem;
    }
    .footer a { color: #667eea; text-decoration: none; font-weight: 600; }
    .footer a:hover { text-decoration: underline; }

    /* === CHAT === */
    .stChatMessage { border-radius: 14px !important; margin-bottom: 0.5rem !important; }

    /* === BUTTONS PREMIUM === */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        padding: 0.75rem !important;
        height: auto !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important;
    }

    /* === ONBOARDING CARD === */
    .onboarding-card {
        background: #fff;
        border: 2px solid #667eea;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(102,126,234,0.1);
    }
    .onboarding-text { 
        font-size: 1.05em; 
        color: #1e1b4b; 
        margin-bottom: 1.2rem; 
        line-height: 1.5;
        font-weight: 500;
    }

    /* === MOBILE NAV === */
    .mobile-nav { 
        display: none; 
        background: #f8f9fc;
        padding: 0.8rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid #eef2f6;
    }
    @media (max-width: 900px) {
        .mobile-nav { display: block; }
        .mobile-nav [data-testid="stSelectbox"] { margin-bottom: 0; }
        .m-card { margin-bottom: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)


# ===== IMPORTAR DADOS =====

@st.cache_data
def carregar_dados():
    """Carrega dados de configuração do agente"""
    data_dir = Path(__file__).parent.parent / "data"
    try:
        df_transacoes = pd.read_csv(data_dir / "transacoes.csv")
        with open(data_dir / "perfil_investidor.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)
        df_historico = pd.read_csv(data_dir / "historico_atendimento.csv")
        with open(data_dir / "produtos_financeiros.json", "r", encoding="utf-8") as f:
            produtos = json.load(f)
        return df_transacoes, perfil, df_historico, produtos
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None, None, None


# ===== FUNÇÕES DE ANÁLISE =====

def analisar_gastos(df_transacoes):
    df_debito = df_transacoes[df_transacoes['tipo'] == 'debito'].copy()
    return {
        "gastos_totais": df_debito['valor'].sum(),
        "gasto_medio": df_debito['valor'].mean(),
        "gasto_minimo": df_debito['valor'].min(),
        "gasto_maximo": df_debito['valor'].max(),
        "por_categoria": df_debito.groupby('categoria')['valor'].sum().to_dict()
    }

def simular_retorno(valor_inicial, taxa_anual, anos):
    valor_futuro = valor_inicial * ((1 + taxa_anual / 100) ** anos)
    ganho = valor_futuro - valor_inicial
    return {
        "valor_futuro": round(valor_futuro, 2),
        "ganho": round(ganho, 2),
        "taxa_efetiva": round((ganho / valor_inicial) * 100, 2) if valor_inicial > 0 else 0,
    }

def calcular_tempo_meta(valor_atual, meta, economia_mensal, taxa_anual):
    meses, saldo = 0, valor_atual
    while saldo < meta and meses < 600:
        saldo += economia_mensal
        saldo += saldo * (taxa_anual / 100 / 12)
        meses += 1
    return {"meses": meses, "anos": round(meses / 12, 1), "alcancavel": saldo >= meta}

def recomendar_produtos(perfil, produtos_lista):
    recomendacoes = []
    for produto in produtos_lista["produtos"]:
        if perfil["perfil_risco"] in produto.get("perfil_recomendado", []):
            compatibilidade = 5
        elif perfil["perfil_risco"] == "moderado":
            compatibilidade = 4
        else:
            compatibilidade = 2
        elegibilidade = "Elegível" if perfil["saldo_atual"] >= produto.get("minimo_investimento", 0) else "Saldo insuficiente"
        recomendacoes.append({
            "nome": produto["nome"],
            "tipo": produto["tipo"],
            "compatibilidade": compatibilidade,
            "elegibilidade": elegibilidade,
            "rentabilidade": produto.get("rentabilidade_anual", 0),
            "risco": produto.get("risco", "desconhecido"),
            "minimo": produto.get("minimo_investimento", 0),
            "taxa_admin": produto.get("taxa_administracao", 0),
        })
    recomendacoes.sort(key=lambda x: x["compatibilidade"], reverse=True)
    return recomendacoes


# ===== COMPONENTES =====

def render_metric(col, icon, label, value, color):
    col.markdown(
        f'<div class="m-card"><div class="m-icon">{icon}</div><div class="m-label">{label}</div><div class="m-value" style="color:{color};">{value}</div></div>',
        unsafe_allow_html=True,
    )

def render_divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def render_info(text):
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# INTERFACE PRINCIPAL
# ═══════════════════════════════════════════════

def main():
    # Inicializar modelo Gemini
    modelo_gemini = init_gemini()
    
    # ── HERO HEADER ──
    st.markdown("""
        <div class="hero">
            <div class="hero-left">
                <div class="hero-icon">🚀</div>
                <div>
                    <div class="hero-title">MetaFinance</div>
                    <div class="hero-sub">Seu Consultor Financeiro com IA Generativa</div>
                </div>
            </div>
            <div class="hero-badge">✨ Powered by Gemini AI</div>
        </div>
    """, unsafe_allow_html=True)

    # Carregar dados
    df_transacoes, perfil, df_historico, produtos = carregar_dados()
    if df_transacoes is None:
        st.error("⚠️ Não foi possível carregar os dados. Verifique a pasta `/data`.")
        return

    # ── INICIALIZAR SESSION STATE ──
    if "usuario_customizado" not in st.session_state:
        st.session_state.usuario_customizado = False
    if "perfil_usuario" not in st.session_state:
        st.session_state.perfil_usuario = perfil.copy()  # Começa com valores padrão, mas pode ser customizado

    # Usar perfil customizado se disponível, caso contrário usar padrão
    perfil_ativo = st.session_state.perfil_usuario

    # ── SIDEBAR ──
    nome = perfil_ativo.get("nome", "Usuário")
    renda_fmt = f"R$ {perfil_ativo.get('renda_mensal', 0):,.0f}" if perfil_ativo.get('renda_mensal', 0) > 0 else "Não informado"
    saldo_fmt = f"R$ {perfil_ativo.get('saldo_atual', 0):,.0f}" if perfil_ativo.get('saldo_atual', 0) > 0 else "Não informado"
    risco = perfil_ativo.get("perfil_risco", "moderado").capitalize()

    st.sidebar.markdown(f"""
        <div class="sb-profile">
            <div class="sb-avatar">👤</div>
            <div class="sb-name">{nome}</div>
            <div class="sb-role">Perfil {risco}</div>
            <div class="sb-stats">
                <div class="sb-stat">
                    <div class="sb-stat-val">{renda_fmt}</div>
                    <div class="sb-stat-lbl">Renda</div>
                </div>
                <div class="sb-stat">
                    <div class="sb-stat-val">{saldo_fmt}</div>
                    <div class="sb-stat-lbl">Saldo</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    opcoes_paginas = [
        "💬 Chat IA",
        "📊 Gastos",
        "🎯 Simulador",
        "📈 Recomendações",
        "👤 Meu Perfil",
        "ℹ️ Sobre",
        "📜 Histórico",
    ]

    if "pagina" not in st.session_state:
        st.session_state.pagina = "💬 Chat IA"

    def on_sidebar_change():
        st.session_state.nav_source = "sidebar"

    def on_mobile_change():
        st.session_state.nav_source = "mobile"
        st.session_state.pagina = st.session_state.pagina_mobile

    def go_to_profile():
        st.session_state.nav_source = "cta"
        st.session_state.pagina = "👤 Meu Perfil"
        st.session_state.pagina_mobile = "👤 Meu Perfil"

    pagina = st.sidebar.radio(
        "🧭 Navegação",
        opcoes_paginas,
        label_visibility="collapsed",
        key="pagina",
        on_change=on_sidebar_change,
    )

    # Navegação mobile (aparece apenas em telas menores)
    if "pagina_mobile" not in st.session_state:
        st.session_state.pagina_mobile = st.session_state.pagina
    if st.session_state.get("nav_source") in ("sidebar", "cta"):
        st.session_state.pagina_mobile = st.session_state.pagina
        st.session_state.nav_source = None

    st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
    pagina_mobile = st.selectbox(
        "Menu rápido",
        opcoes_paginas,
        index=opcoes_paginas.index(st.session_state.pagina),
        key="pagina_mobile",
        on_change=on_mobile_change,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("nav_source") == "mobile":
        st.session_state.nav_source = None

    st.sidebar.markdown("---")
    if modelo_gemini:
        st.sidebar.success("🟢 IA Gemini ativa")
    else:
        st.sidebar.warning("🟡 IA offline — respostas padrão")

    # ═══════════════════════════════════════
    # PÁGINA: CHAT IA
    # ═══════════════════════════════════════
    if pagina == "💬 Chat IA":
        st.markdown('<div class="sec-title">💬 Chat com MetaFinance</div>', unsafe_allow_html=True)

        # Mostrar aviso se usuário não customizou perfil
        if not st.session_state.usuario_customizado:
            st.markdown("""
                <div class="onboarding-card">
                    <div class="onboarding-text">
                        ℹ️ <b>Configure seu perfil primeiro!</b> Clique no botão abaixo ou em 👤 <b>Meu Perfil</b> na navegação para fornecer seus dados e receber análises personalizadas.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.button(
                "👤 Acessar Meu Perfil Agora",
                key="cta_perfil_main",
                on_click=go_to_profile,
            )

        render_info(
            "Olá! Sou a <b>MetaFinance</b>, sua consultora financeira com IA. Pergunte sobre "
            "<b>investimentos</b>, <b>economia</b>, <b>produtos financeiros</b> "
            "ou peça <b>dicas educativas</b>. 🚀"
        )

        if "historico_chat" not in st.session_state:
            st.session_state.historico_chat = [
                {"role": "assistant", "content": "👋 Olá! Sou a **MetaFinance**, sua consultora financeira com IA. Como posso ajudá-lo hoje?"}
            ]

        for msg in st.session_state.historico_chat:
            avatar = "🤖" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        user_input = st.chat_input("Pergunte algo sobre finanças...")
        if user_input:
            st.session_state.historico_chat.append({"role": "user", "content": user_input})
            with st.spinner("🤔 MetaFinance está analisando..."):
                resposta = gerar_resposta_meta(user_input, perfil_ativo, df_transacoes, produtos, modelo_gemini, st.session_state.usuario_customizado)
            st.session_state.historico_chat.append({"role": "assistant", "content": resposta})
            st.rerun()

    # ═══════════════════════════════════════
    # PÁGINA: GASTOS
    # ═══════════════════════════════════════
    elif pagina == "📊 Gastos":
        st.markdown('<div class="sec-title">📊 Análise de Gastos e Receitas</div>', unsafe_allow_html=True)

        analise = analisar_gastos(df_transacoes)
        receita_total = df_transacoes[df_transacoes["tipo"] == "credito"]["valor"].sum()
        taxa_poupanca = ((receita_total - analise["gastos_totais"]) / receita_total * 100) if receita_total > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        render_metric(col1, "💵", "Renda Total", f"R$ {receita_total:,.0f}", "#10b981")
        render_metric(col2, "💸", "Gastos Totais", f"R$ {analise['gastos_totais']:,.0f}", "#ef4444")
        render_metric(col3, "📈", "Tx. Poupança", f"{taxa_poupanca:.1f}%", "#f59e0b")
        render_metric(col4, "💰", "Saldo", f"R$ {perfil['saldo_atual']:,.0f}", "#667eea")

        render_divider()

        df_cat = pd.DataFrame(list(analise["por_categoria"].items()), columns=["Categoria", "Valor"]).sort_values("Valor", ascending=False)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="sec-title">📊 Gastos por Categoria</div>', unsafe_allow_html=True)
            st.bar_chart(df_cat.set_index("Categoria"), color="#667eea")
        with col_r:
            st.markdown('<div class="sec-title">🥧 Distribuição</div>', unsafe_allow_html=True)
            df_view = df_cat.copy()
            df_view["% do Total"] = (df_view["Valor"] / df_view["Valor"].sum() * 100).round(1).astype(str) + "%"
            df_view["Valor"] = df_view["Valor"].apply(lambda x: f"R$ {x:,.0f}")
            st.dataframe(df_view, use_container_width=True, hide_index=True)

        render_divider()

        st.markdown('<div class="sec-title">📋 Extrato Recente</div>', unsafe_allow_html=True)
        st.dataframe(df_transacoes.iloc[::-1].head(15), use_container_width=True, hide_index=True)

        render_divider()

        maior_cat = max(analise["por_categoria"], key=analise["por_categoria"].get)
        maior_val = analise["por_categoria"][maior_cat]
        if maior_val > perfil["renda_mensal"] * 0.3:
            st.warning(f"⚠️ Gastos em **{maior_cat.lower()}** = **{(maior_val/perfil['renda_mensal']*100):.0f}%** da renda. Considere revisar!")
        else:
            st.success("✅ Gastos bem distribuídos. Ótimo potencial para investir!")

    # ═══════════════════════════════════════
    # PÁGINA: SIMULADOR
    # ═══════════════════════════════════════
    elif pagina == "🎯 Simulador":
        st.markdown('<div class="sec-title">🎯 Simulador de Investimentos</div>', unsafe_allow_html=True)
        render_info("Descubra como seu dinheiro pode crescer! Ajuste os parâmetros e veja a projeção em tempo real.")

        col1, col2, col3 = st.columns(3)
        with col1:
            valor_inv = st.number_input("💰 Valor Inicial (R$)", min_value=0.0, value=1000.0, step=500.0)
        with col2:
            taxa = st.number_input("📈 Taxa Anual (%)", min_value=0.0, max_value=50.0, value=10.0, step=0.5)
        with col3:
            anos = st.number_input("📅 Período (Anos)", min_value=1, max_value=50, value=5, step=1)

        if st.button("🚀 Calcular Projeção", use_container_width=True, type="primary"):
            resultado = simular_retorno(valor_inv, taxa, anos)

            col1, col2, col3 = st.columns(3)
            render_metric(col1, "🏦", "Valor Futuro", f"R$ {resultado['valor_futuro']:,.2f}", "#10b981")
            render_metric(col2, "📈", "Ganho Total", f"R$ {resultado['ganho']:,.2f}", "#667eea")
            render_metric(col3, "⚡", "Rendimento", f"{resultado['taxa_efetiva']:.1f}%", "#f59e0b")

            render_divider()

            st.markdown('<div class="sec-title">📈 Projeção de Crescimento</div>', unsafe_allow_html=True)
            ano_list = list(range(0, anos + 1))
            valor_list = [valor_inv * ((1 + taxa / 100) ** a) for a in ano_list]
            df_chart = pd.DataFrame({"Ano": ano_list, "Patrimônio (R$)": valor_list})
            st.area_chart(df_chart.set_index("Ano"), color="#667eea")

    # ═══════════════════════════════════════
    # PÁGINA: RECOMENDAÇÕES
    # ═══════════════════════════════════════
    elif pagina == "📈 Recomendações":
        st.markdown('<div class="sec-title">📈 Recomendações Personalizadas</div>', unsafe_allow_html=True)

        # Gerar análise personalizada com IA
        analise_ia = gerar_analise_perfil_ia(perfil_ativo, modelo_gemini, st.session_state.usuario_customizado)
        render_info(analise_ia)

        recomendacoes = recomendar_produtos(perfil, produtos)
        elegiveis = [r for r in recomendacoes if r["elegibilidade"] == "Elegível"]

        if elegiveis:
            for rec in elegiveis[:5]:
                badge_cls = "bg-green" if rec["risco"] == "baixo" else ("bg-yellow" if rec["risco"] == "medio" else "bg-red")
                stars = "⭐" * rec["compatibilidade"]

                st.markdown(f"""
                    <div class="p-card">
                        <div class="p-head">
                            <div class="p-name">{rec['nome']}</div>
                            <div class="p-badge {badge_cls}">Risco {rec['risco'].upper()}</div>
                        </div>
                        <div class="p-meta">{rec['tipo']} &bull; Compatibilidade: {stars}</div>
                        <div class="p-grid">
                            <div class="p-stat">
                                <div class="p-stat-val">{rec['rentabilidade']:.1f}%</div>
                                <div class="p-stat-lbl">Rent. Anual</div>
                            </div>
                            <div class="p-stat">
                                <div class="p-stat-val">R$ {rec['minimo']:,.0f}</div>
                                <div class="p-stat-lbl">Mín. Investimento</div>
                            </div>
                            <div class="p-stat">
                                <div class="p-stat-val">{rec['taxa_admin']:.2f}%</div>
                                <div class="p-stat-lbl">Taxa Admin</div>
                            </div>
                            <div class="p-stat">
                                <div class="p-stat-val">✅</div>
                                <div class="p-stat-lbl">{rec['elegibilidade']}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Nenhum produto elegível no momento. Acumule mais saldo para começar!")

    # ═══════════════════════════════════════
    # PÁGINA: MEU PERFIL
    # ═══════════════════════════════════════
    elif pagina == "👤 Meu Perfil":
        st.markdown('<div class="sec-title">👤 Meu Perfil Financeiro</div>', unsafe_allow_html=True)
        render_info(
            "Configure seus dados pessoais e financeiros para receber recomendações mais precisas e personalizadas. "
            "Todos os dados são mantidos em segurança localmente. 🔒"
        )

        st.markdown('<div class="sec-title">📝 Dados Pessoais</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            nome_novo = st.text_input("👤 Nome Completo", value=st.session_state.perfil_usuario.get("nome", ""), placeholder="Seu nome aqui")
        with col2:
            idade_nova = st.number_input("🎂 Idade", min_value=18, max_value=100, value=st.session_state.perfil_usuario.get("idade", 30), step=1)
        with col3:
            profissao_nova = st.text_input("💼 Profissão", value=st.session_state.perfil_usuario.get("profissao", ""), placeholder="Ex: Analista de Sistemas")

        st.markdown('<div class="sec-title">💰 Dados Financeiros</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            renda_nova = st.number_input("💵 Renda Mensal (R$)", min_value=0.0, value=float(st.session_state.perfil_usuario.get("renda_mensal", 0)), step=100.0)
        with col2:
            saldo_novo = st.number_input("💰 Saldo Atual (R$)", min_value=0.0, value=float(st.session_state.perfil_usuario.get("saldo_atual", 0)), step=100.0)
        with col3:
            patrimonio_novo = st.number_input("🏦 Patrimônio Total (R$)", min_value=0.0, value=float(st.session_state.perfil_usuario.get("patrimonio_total", 0)), step=100.0)

        st.markdown('<div class="sec-title">🎯 Perfil de Investimento</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            risco_novo = st.selectbox(
                "🎲 Perfil de Risco",
                ["conservador", "moderado", "agressivo"],
                index=["conservador", "moderado", "agressivo"].index(st.session_state.perfil_usuario.get("perfil_risco", "moderado"))
            )
        with col2:
            experiencia_nova = st.selectbox(
                "📚 Experiência em Investimentos",
                ["iniciante", "intermediaria", "avancada"],
                index=["iniciante", "intermediaria", "avancada"].index(st.session_state.perfil_usuario.get("experiencia_investimentos", "intermediaria"))
            )

        st.markdown('<div class="sec-title">🎯 Objetivos Financeiros</div>', unsafe_allow_html=True)
        objetivo_principal_novo = st.text_input(
            "🎯 Objetivo Principal",
            value=st.session_state.perfil_usuario.get("objetivo_principal", ""),
            placeholder="Ex: Aposentadoria em 25 anos"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            # Normalizar tempo_horizonte para compatibilidade com dados antigos
            tempo_atual = st.session_state.perfil_usuario.get("tempo_horizonte", "longo prazo (5+ anos)")
            opcoes_tempo = ["curto prazo (0-2 anos)", "médio prazo (2-5 anos)", "longo prazo (5+ anos)"]
            
            # Mapeamento para compatibilidade com valores antigos do JSON
            mapeamento_tempo = {
                "curto prazo": "curto prazo (0-2 anos)",
                "médio prazo": "médio prazo (2-5 anos)",
                "longo prazo": "longo prazo (5+ anos)",
            }
            
            # Normalizar o valor se estiver no formato antigo
            tempo_normalizado = mapeamento_tempo.get(tempo_atual, tempo_atual)
            
            # Garantir que o valor está nas opções
            if tempo_normalizado not in opcoes_tempo:
                tempo_normalizado = "longo prazo (5+ anos)"
            
            tempo_horizonte_novo = st.selectbox(
                "⏱️ Horizonte de Tempo",
                opcoes_tempo,
                index=opcoes_tempo.index(tempo_normalizado)
            )
        with col2:
            # Normalizar objetivos secundários para compatibilidade com dados antigos
            opcoes_objetivos = ["Casa própria", "Educação dos filhos", "Viagem internacional", "Carro novo", "Negócio próprio", "Outros"]
            
            # Mapeamento de valores antigos para novos
            mapeamento_objetivos = {
                "Fundo para educação do filho": "Educação dos filhos",
                "Casa própria em 5 anos": "Casa própria",
                "Educação do filho": "Educação dos filhos",
                "Educação do filhos": "Educação dos filhos",  # Typos
            }
            
            # Obter objetivos e normalizá-los
            objetivos_atuais = st.session_state.perfil_usuario.get("objetivos_secundarios", [])
            objetivos_normalizados = []
            
            for obj in objetivos_atuais:
                # Se está no mapeamento, usar o novo valor
                obj_novo = mapeamento_objetivos.get(obj, obj)
                # Se está nas opções, adicionar à lista
                if obj_novo in opcoes_objetivos:
                    objetivos_normalizados.append(obj_novo)
                # Se não mapeou e está direto nas opções, ok
                elif obj in opcoes_objetivos:
                    objetivos_normalizados.append(obj)
            
            objetivos_sec = st.multiselect(
                "📌 Objetivos Secundários",
                opcoes_objetivos,
                default=objetivos_normalizados
            )

        render_divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar Alterações", use_container_width=True, type="primary"):
                st.session_state.perfil_usuario = {
                    **st.session_state.perfil_usuario,
                    "nome": nome_novo or "Usuário",
                    "idade": idade_nova,
                    "profissao": profissao_nova,
                    "renda_mensal": renda_nova,
                    "saldo_atual": saldo_novo,
                    "patrimonio_total": patrimonio_novo,
                    "perfil_risco": risco_novo,
                    "experiencia_investimentos": experiencia_nova,
                    "objetivo_principal": objetivo_principal_novo,
                    "tempo_horizonte": tempo_horizonte_novo,
                    "objetivos_secundarios": objetivos_sec,
                }
                st.session_state.usuario_customizado = True
                st.success("✅ Perfil atualizado com sucesso!")
                st.balloons()
        
        with col2:
            if st.button("🔄 Usar Dados de Exemplo", use_container_width=True):
                st.session_state.perfil_usuario = perfil.copy()
                st.session_state.usuario_customizado = False
                st.info("ℹ️ Recarregue a página para ver os dados de exemplo")

        render_divider()

        st.markdown('<div class="sec-title">ℹ️ Como Seus Dados São Usados</div>', unsafe_allow_html=True)
        st.markdown("""
        - **Chat IA**: Personaliza respostas com base no seu perfil
        - **Recomendações**: Sugere produtos adequados ao seu risco e objetivos
        - **Análises**: Contextualiza gastos com base na sua renda
        - **Privacidade**: Todos os dados são mantidos localmente no seu navegador
        - **Sem Compartilhamento**: Nenhum dado é enviado a terceiros
        """)

    # ═══════════════════════════════════════
    # PÁGINA: SOBRE
    # ═══════════════════════════════════════
    elif pagina == "ℹ️ Sobre":
        st.markdown('<div class="sec-title">ℹ️ Sobre a MetaFinance</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
**MetaFinance** é um agente financeiro inteligente que usa **IA Generativa (Gemini)**
para oferecer consultoria financeira personalizada e acessível.

### 🧩 Funcionalidades
- 🤖 **Chat inteligente** com respostas de IA generativa
- 📊 **Análise de gastos** com insights automáticos
- 🎯 **Simulações** de investimento em tempo real
- 📈 **Recomendações** de produtos financeiros por perfil
- 📚 **Educação financeira** gratuita e acessível

### 🛠 Stack Tecnológica
| Tecnologia | Uso |
|---|---|
| **Streamlit** | Interface web interativa |
| **Google Gemini AI** | IA generativa |
| **Python + Pandas** | Análise de dados |
| **python-dotenv** | Gerenciamento seguro de chaves |
            """)
        with col2:
            st.markdown("""
### 🗺️ Roadmap

🟦 **V1** (Atual)
Chat + Análise + Simulações

🟩 **V2** (Próxima)
APIs bancárias reais

🟥 **V3** (Futura)
Alertas e previsões com ML
            """)

    # ═══════════════════════════════════════
    # PÁGINA: HISTÓRICO
    # ═══════════════════════════════════════
    elif pagina == "📜 Histórico":
        st.markdown('<div class="sec-title">📜 Histórico de Atendimentos</div>', unsafe_allow_html=True)
        render_info("Registros de atendimentos anteriores realizados pela MetaFinance.")

        col1, col2, col3 = st.columns(3)
        render_metric(col1, "📋", "Total", str(len(df_historico)), "#667eea")
        render_metric(col2, "⭐", "Satisfação", f"{df_historico['satisfacao'].mean():.1f}/5", "#f59e0b")
        top_d = df_historico["tipo_duvida"].value_counts().index[0]
        render_metric(col3, "❓", "Dúvida Top", top_d, "#10b981")

        render_divider()

        st.dataframe(df_historico, use_container_width=True, hide_index=True)

        render_divider()

        st.markdown('<div class="sec-title">📊 Satisfação por Tipo</div>', unsafe_allow_html=True)
        st.bar_chart(df_historico.groupby("tipo_duvida")["satisfacao"].mean(), color="#667eea")

    # ═══════════════════════════════════════
    # RODAPÉ
    # ═══════════════════════════════════════
    st.markdown("""
        <div class="footer">
            Projeto desenvolvido por <b>Patrick Lima</b>, como parte da certificação
            <a href="https://www.dio.me/" target="_blank">DIO (Digital Innovation One)</a><br>
            <span style="opacity: 0.5;">MetaFinance v1.0 &bull; 2026</span>
        </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# FUNÇÕES DE RESPOSTA COM IA
# ═══════════════════════════════════════════════

def gerar_analise_perfil_ia(perfil, modelo_gemini=None, usuario_customizado=False):
    """Gera uma análise personalizada do perfil do cliente usando IA"""
    
    # Se usuário não forneceu dados, usar mensagem padrão
    if not usuario_customizado:
        return render_analise_inicial_padrao()
    
    objetivos = perfil.get('objetivo_principal', 'não definido')
    objetivos_sec = perfil.get('objetivos_secundarios', [])
    
    if objetivos_sec:
        objetivos += " • " + " • ".join(objetivos_sec)
    
    if modelo_gemini:
        try:
            prompt = f"""
Você é MetaFinance, uma consultora financeira com IA. Faça uma análise breve e personalizada do perfil deste cliente para apresentar as recomendações adequadas.

## PERFIL DO CLIENTE
- **Idade**: {perfil.get('idade', 'N/A')} anos
- **Experiência em Investimentos**: {perfil.get('experiencia_investimentos', 'iniciante')}
- **Perfil de Risco**: {perfil['perfil_risco']}
- **Horizonte de Tempo**: {perfil.get('tempo_horizonte', 'não informado')}
- **Objetivos**: {objetivos}
- **Estado Civil**: {perfil.get('estado_civil', 'não informado')}
- **Dependentes**: {perfil.get('dependentes', 0)}

## INSTRUÇÕES
1. Gere um parágrafo de apresentação que considere TODOS os objetivos mencionados
2. NÃO diga "Pelo seu perfil, vejo que seu grande objetivo é aposentadoria em 25 anos" — isso é genérico demais
3. Reconheça a pluralidade de objetivos: "Vejo que você está equilibrando múltiplos objetivos..."
4. Mencione como o perfil de risco se alinha com os objetivos
5. Seja empático — nem todos têm 25 anos para aposentar
6. Máximo 120 palavras
7. Use tom conversacional, nunca técnico
8. Inclua 1-2 emojis
9. SEMPRE se apresente como **MetaFinance**, não use outro nome
            """
            response = modelo_gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            return gerar_analise_padrao(perfil)
    
    return gerar_analise_padrao(perfil)


def render_analise_inicial_padrao():
    """Mensagem padrão quando usuário ainda não customizou seu perfil"""
    return """
    <b>👋 Bem-vindo à MetaFinance!</b><br><br>
    Para começar, configure seu perfil financeiro clicando em <b>👤 Meu Perfil</b> na navegação lateral. 
    Isso vai personalizar todas as análises, recomendações e simulações para sua situação específica. 💡<br><br>
    <em>Todos os seus dados são mantidos em segurança localmente no seu navegador — nada é compartilhado!</em> 🔒
    """


def gerar_analise_padrao(perfil):
    """Análise padrão quando IA não está disponível"""
    objetivos = perfil.get('objetivo_principal', 'não definido')
    objetivos_sec = perfil.get('objetivos_secundarios', [])
    
    texto_objetivos = f"<b>{objetivos}</b>"
    if objetivos_sec:
        texto_objetivos += " • " + " • ".join([f"<b>{o}</b>" for o in objetivos_sec])
    
    risco = perfil['perfil_risco'].capitalize()
    experiencia = perfil.get('experiencia_investimentos', 'iniciante').capitalize()
    
    return f"""
Análise do seu perfil: Você é um investidor com perfil <b>{risco}</b>, experiência <b>{experiencia}</b>, 
com múltiplos objetivos financeiros: {texto_objetivos}. 
Vou recomendar produtos que alinhem com seu horizonte de tempo e tolerância a risco. 🎯
    """

def gerar_resposta_meta(pergunta, perfil, df_transacoes, produtos, modelo_gemini=None, usuario_customizado=False):
    if modelo_gemini:
        try:
            # Construir contexto de objetivos de forma dinâmica
            objetivos = perfil.get('objetivo_principal', 'Não definido')
            objetivos_sec = perfil.get('objetivos_secundarios', [])
            
            if objetivos_sec:
                objetivos += " + " + ", ".join(objetivos_sec)
            
            # Se usuário não customizou, não mencionar dados específicos
            contexto_usuario = ""
            if usuario_customizado:
                contexto_usuario = f"""
## CONTEXTO DO CLIENTE
**Perfil**: {perfil['perfil_risco'].capitalize()} (tolerância a risco) | Idade: {perfil.get('idade', 'não informada')} anos
**Horizonte**: {perfil.get('tempo_horizonte', 'não informado')}
**Objetivos**: {objetivos}
**Experiência**: {perfil.get('experiencia_investimentos', 'não informada')}
            """
            else:
                contexto_usuario = f"""
## LEMBRANÇA
O cliente ainda não forneceu dados pessoais específicos.
Dê respostas genéricas e educativas, incentivando a **configuração do perfil em "👤 Meu Perfil"** para recomendações mais precisas.
            """
            
            prompt = f"""
Você é MetaFinance, uma consultora financeira com IA especializada em finanças pessoais brasileiras.

{contexto_usuario}

## PERGUNTA: {pergunta}

## INSTRUÇÕES CRITICAS:
1. **Personalize** a resposta para este perfil específico, NÃO genérico
2. **Reconheça os objetivos reais** do cliente — cada pessoa tem prioridades diferentes
3. Se for sobre objetivos de vida/meta, fale sobre TODOS os objetivos mencionados
4. Responda de forma conversacional, educativa, nunca alarmista
5. Não especule sobre valores de renda/saldo — fale de forma relativa
6. Inclua exemplos práticos quando possível
7. Use tom empático — entenda que nem todos têm 25 anos para aposentar
8. Se há dúvida, pergunte/esclareça antes de recomendar
9. Máximo 280 palavras, use emojis naturalmente
10. SEMPRE mencione que é consultoria genérica, não consultoria tributária/legal
11. Se usuário não customizou perfil, sugira que customize para obter análises mais precisas
12. SEMPRE se apresente como **MetaFinance**, nunca use outro nome ou "Sofia Finance"
            """
            response = modelo_gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            st.warning(f"⚠️ Erro na IA: {str(e)}. Usando resposta padrão...")
            return gerar_resposta_padrao(pergunta, perfil, df_transacoes, produtos, usuario_customizado)
    return gerar_resposta_padrao(pergunta, perfil, df_transacoes, produtos, usuario_customizado)


def gerar_resposta_padrao(pergunta, perfil, df_transacoes, produtos, usuario_customizado=False):
    pergunta_lower = pergunta.lower()
    
    dica_perfil = ""
    if not usuario_customizado:
        dica_perfil = "\n\n💡 *Para respostas mais personalizadas, configure seu perfil em **👤 Meu Perfil***"
    
    objetivos = perfil.get('objetivo_principal', '')
    objetivos_sec = perfil.get('objetivos_secundarios', [])
    
    # Montar string de objetivos
    objetivos_texto = objetivos
    if objetivos_sec:
        objetivos_texto += " • " + " • ".join(objetivos_sec)

    if any(w in pergunta_lower for w in ["investir", "investimento", "rendimento", "retorno"]):
        return f"""
Ótima pergunta! Vou te ajudar com investimentos! 🚀

💡 **RECOMENDAÇÕES PARA PERFIL {perfil['perfil_risco'].upper()}**:

1. **CDB** — Seguro (FGC até R$ 250 mil) • ~10.5% ao ano
2. **Tesouro Direto** — Garantia do governo • ~9.2% ao ano
3. **Fundos** — Boa diversificação • 8-12% ao ano

📊 **Exemplo**: R$ 1.000 em CDB a 10.5%/ano:
- 1 ano: R$ 1.105 | 3 anos: R$ 1.349 | 5 anos: R$ 1.645

💡 O mais importante é **começar**, mesmo com pouco!

⚠️ *Consultoria genérica — consulte especialista para análise tributária*{dica_perfil}
"""

    elif any(w in pergunta_lower for w in ["gasto", "despesa", "economia", "economizar"]):
        return f"""
Vamos otimizar suas finanças! 💰

📊 **Regra 50-30-20**:
- 50% → Necessidades | 30% → Desejos | 20% → Investimentos

🔍 **Dicas práticas**:
- Revise assinaturas mensais não utilizadas
- Faça lista antes de ir ao mercado
- Negocie taxas bancárias
- Reduza delivery e comer fora

💡 Economizando R$ 100/mês a 10% ao ano = **R$ 7.700 em 5 anos**!

⚠️ *Cada perfil tem metas diferentes — personalize conforme sua realidade*{dica_perfil}
"""

    elif any(w in pergunta_lower for w in ["meta", "objetivo", "quanto tempo", "futuro"]):
        return f"""
Que ótimo pensar no futuro! 🎯

**Seus objetivos**: {objetivos_texto if usuario_customizado else "Configure em 👤 Meu Perfil para ver análise personalizada"}

📋 **Estratégia para Múltiplos Objetivos**:
1. Liste objetivos por prazo: curto (0-2 anos) | médio (2-5) | longo (5+)
2. Aloque % de renda para cada um
3. Escolha produtos conforme o prazo
4. Revise 1x por trimestre

📊 **Exemplo**: R$ 200/mês a 10%/ano:
- 5 anos: ~R$ 15.400 | 10 anos: ~R$ 40.800 | 20 anos: ~R$ 151.800

💡 O segredo é a **consistência** e **diversificação** entre metas!

⚠️ *Prazos realistas — nem todo mundo tem 25 anos para aposentar*{dica_perfil}
"""

    elif any(w in pergunta_lower for w in ["o que é", "como funciona", "diferença", "explica"]):
        if "cdb" in pergunta_lower:
            return f"""
📚 **O que é CDB?**

CDB = Certificado de Depósito Bancário. Você empresta dinheiro ao banco e recebe juros.

✅ Protegido pelo FGC (até R$ 250 mil)
📈 Rendimento: ~10.5% ao ano
🔒 Risco muito baixo

| Produto | Rent. Anual |
|---------|------------|
| Poupança | ~0.5% |
| **CDB** | **~10.5%** |
| Tesouro | ~9.2% |
| Fundos | 8-12% |

💡 Ótima porta de entrada para investidores iniciantes!{dica_perfil}
"""
        elif "fundo" in pergunta_lower:
            return f"""
📚 **O que é Fundo de Investimento?**

Um gestor profissional investe seu dinheiro em vários ativos.

🟢 Conservador: ~8.5%/ano
🟡 Moderado: ~9-11%/ano
🔴 Agressivo: ~12%+/ano

| Aspecto | CDB | Fundo |
|---------|-----|-------|
| Retorno | Garantido | Variável |
| Diversificação | Baixa | Alta |

💡 Combine CDB (segurança) + Fundos (diversificação)!{dica_perfil}
"""
        return f"""
📚 **Conceitos Financeiros**:

💰 Investimento • 📊 Rentabilidade • 🎯 Risco • ⏱️ Horizonte
🔄 Juros Compostos • 🛡️ FGC (proteção até R$ 250 mil)

Posso explicar: CDB, Fundos, Tesouro Direto, Bolsa, Diversificação.
Qual tema você quer aprender?{dica_perfil}
"""

    return f"""
Olá! 👋 Sou a **MetaFinance**, sua consultora com IA!

Posso ajudar com:
📊 Gastos | 💰 Investimentos | 🧮 Simulações | 📚 Educação | 🎯 Metas

Experimente: *"Como investir?"* · *"O que é CDB?"* · *"Como economizar?"*{dica_perfil}
"""


if __name__ == "__main__":
    main()
