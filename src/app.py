"""
AGENTE FINANCEIRO INTELIGENTE - Sofia Finance
Chatbot de Consultoria Financeira com IA Generativa

Autor: DIO Challenge
Data: 2024
"""

import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="Sofia Finance - Consultora Financeira IA",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== IMPORTAR DADOS =====

@st.cache_data
def carregar_dados():
    """Carrega dados de configuração do agente"""
    data_dir = Path(__file__).parent.parent / "data"
    
    try:
        # Carregar transações
        df_transacoes = pd.read_csv(data_dir / "transacoes.csv")
        
        # Carregar perfil do investidor
        with open(data_dir / "perfil_investidor.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)
        
        # Carregar histórico de atendimento
        df_historico = pd.read_csv(data_dir / "historico_atendimento.csv")
        
        # Carregar produtos
        with open(data_dir / "produtos_financeiros.json", "r", encoding="utf-8") as f:
            produtos = json.load(f)
        
        return df_transacoes, perfil, df_historico, produtos
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None, None, None


# ===== FUNÇÕES DE ANÁLISE FINANCEIRA =====

def analisar_gastos(df_transacoes):
    """Analisa padrão de gastos do cliente"""
    df_debito = df_transacoes[df_transacoes['tipo'] == 'debito'].copy()
    
    analise = {
        "gastos_totais": df_debito['valor'].sum(),
        "gasto_medio": df_debito['valor'].mean(),
        "gasto_minimo": df_debito['valor'].min(),
        "gasto_maximo": df_debito['valor'].max(),
        "por_categoria": df_debito.groupby('categoria')['valor'].sum().to_dict()
    }
    
    return analise


def simular_retorno(valor_inicial, taxa_anual, anos):
    """Simula retorno de investimento"""
    valor_futuro = valor_inicial * ((1 + taxa_anual/100) ** anos)
    ganho = valor_futuro - valor_inicial
    
    return {
        "valor_futuro": round(valor_futuro, 2),
        "ganho": round(ganho, 2),
        "taxa_efetiva": round((ganho / valor_inicial) * 100, 2) if valor_inicial > 0 else 0
    }


def calcular_tempo_meta(valor_atual, meta, economia_mensal, taxa_anual):
    """Calcula tempo para atingir meta financeira"""
    meses = 0
    saldo = valor_atual
    
    while saldo < meta and meses < 600:  # Max 50 anos
        saldo += economia_mensal
        saldo += saldo * (taxa_anual / 100 / 12)
        meses += 1
    
    return {
        "meses": meses,
        "anos": round(meses / 12, 1),
        "alcancavel": saldo >= meta
    }


def recomendar_produtos(perfil, produtos_lista):
    """Recomenda produtos baseado no perfil do cliente"""
    recomendacoes = []
    
    for produto in produtos_lista["produtos"]:
        # Validar compatibilidade
        if perfil["perfil_risco"] in produto.get("perfil_recomendado", []):
            compatibilidade = 5
        elif perfil["perfil_risco"] == "moderado" and "moderado" in produto.get("perfil_recomendado", []):
            compatibilidade = 4
        else:
            compatibilidade = 2
        
        # Validar saldo
        if perfil["saldo_atual"] >= produto.get("minimo_investimento", 0):
            elegibilidade = "Elegível"
        else:
            elegibilidade = "Saldo insuficiente"
        
        recomendacoes.append({
            "nome": produto["nome"],
            "tipo": produto["tipo"],
            "compatibilidade": compatibilidade,
            "elegibilidade": elegibilidade,
            "rentabilidade": produto.get("rentabilidade_anual", 0),
            "risco": produto.get("risco", "desconhecido"),
            "minimo": produto.get("minimo_investimento", 0),
            "taxa_admin": produto.get("taxa_administracao", 0)
        })
    
    # Ordenar por compatibilidade
    recomendacoes.sort(key=lambda x: x["compatibilidade"], reverse=True)
    return recomendacoes


# ===== INTERFACE STREAMLIT =====

def main():
    # Header
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("💰 Sofia Finance")
        st.markdown("*Consultora Financeira Inteligente com IA*")
    
    with col2:
        st.image("", use_column_width=True) if os.path.exists("assets/logo.png") else None
    
    st.markdown("---")
    
    # Carregar dados
    df_transacoes, perfil, df_historico, produtos = carregar_dados()
    
    if df_transacoes is None:
        st.error("⚠️ Não foi possível carregar os dados. Verifique a pasta `/data`.")
        return
    
    # Sidebar com menu
    st.sidebar.title("🧭 Menu")
    pagina = st.sidebar.radio(
        "Escolha uma opção:",
        [
            "💬 Chat com Sofia",
            "📊 Análise de Gastos",
            "🎯 Simulador de Investimentos",
            "📈 Recomendações Personalizadas",
            "ℹ️ Sobre Sofia",
            "💬 histórico"
        ]
    )
    
    # ===== PÁGINA 1: CHAT COM SOFIA =====
    if pagina == "💬 Chat com Sofia":
        st.header("Chat com Sofia Finance")
        st.markdown("""
        Olá! Sou Sofia, sua consultora financeira digital. 
        Posso ajudar com:
        - 💡 Recomendações de investimento
        - 📊 Análise de gastos e economia
        - 🧮 Cálculos e simulações  
        - 📚 Educação financeira
        """)
        
        st.markdown("---")
        
        # Inicializar histórico de chat
        if "historico_chat" not in st.session_state:
            st.session_state.historico_chat = [
                {
                    "role": "assistant",
                    "content": "👋 Sou a Sofia Finance. Como posso ajudá-lo hoje?"
                }
            ]
        
        # Exibir histórico
        for msg in st.session_state.historico_chat:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input do usuário
        user_input = st.chat_input("Digite sua pergunta aqui...")
        
        if user_input:
            # Adicionar msg do usuário
            st.session_state.historico_chat.append({
                "role": "user",
                "content": user_input
            })
            
            # Gerar resposta (resposta inteligente baseada em padrões)
            resposta = gerar_resposta_sofia(
                user_input, 
                perfil, 
                df_transacoes, 
                produtos
            )
            
            st.session_state.historico_chat.append({
                "role": "assistant",
                "content": resposta
            })
            
            st.rerun()
    
    # ===== PÁGINA 2: ANÁLISE DE GASTOS =====
    elif pagina == "📊 Análise de Gastos":
        st.header("📊 Análise de Gastos e Receitas")
        
        analise = analisar_gastos(df_transacoes)
        receita_total = df_transacoes[df_transacoes['tipo'] == 'credito']['valor'].sum()
        
        # Cards com métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💵 Renda Total", f"R$ {receita_total:,.2f}")
        
        with col2:
            st.metric("💸 Gastos Totais", f"R$ {analise['gastos_totais']:,.2f}")
        
        with col3:
            taxa_poupanca = ((receita_total - analise['gastos_totais']) / receita_total * 100) if receita_total > 0 else 0
            st.metric("📈 Taxa de Poupança", f"{taxa_poupanca:.1f}%")
        
        with col4:
            st.metric("💰 Saldo Atual", f"R$ {perfil['saldo_atual']:,.2f}")
        
        st.markdown("---")
        
        # Gráficos
        st.subheader("Gastos por Categoria")
        
        df_categorias = pd.DataFrame(
            list(analise['por_categoria'].items()),
            columns=['Categoria', 'Valor']
        ).sort_values('Valor', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(df_categorias.set_index('Categoria'))
        
        with col2:
            st.pie_chart(df_categorias.set_index('Categoria'))
        
        st.markdown("---")
        
        # Tabela detalhada
        st.subheader("Extrato Detalhado (Últimas 15 transações)")
        st.dataframe(
            df_transacoes.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
        
        # Recomendação automática
        st.markdown("---")
        st.subheader("💡 Recomendação Automática")
        
        maior_categoria = max(analise['por_categoria'], key=analise['por_categoria'].get)
        maior_valor = analise['por_categoria'][maior_categoria]
        
        if maior_valor > perfil['renda_mensal'] * 0.3:
            st.info(
                f"⚠️ Você está gastando {(maior_valor/perfil['renda_mensal']*100):.1f}% "
                f"da renda em {maior_categoria.lower()}. "
                f"Considere revisar esses gastos!"
            )
        else:
            st.success(
                "✅ Seus gastos parecem bem distribuídos! "
                "Você tem potencial para investir e fazer seu patrimônio crescer."
            )
    
    # ===== PÁGINA 3: SIMULADOR =====
    elif pagina == "🎯 Simulador de Investimentos":
        st.header("🎯 Simulador de Investimentos")
        
        st.markdown("Use este simulador para ver como seu dinheiro pode crescer!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            valor_inv = st.number_input(
                "Valor Inicial (R$)",
                min_value=0.0,
                value=float(perfil['saldo_atual']),
                step=500.0
            )
        
        with col2:
            taxa = st.number_input(
                "Taxa Anual (%)",
                min_value=0.0,
                max_value=50.0,
                value=8.5,
                step=0.5
            )
        
        with col3:
            anos = st.number_input(
                "Período (Anos)",
                min_value=1,
                max_value=50,
                value=5,
                step=1
            )
        
        if st.button("▶️ Calcular", use_container_width=True):
            resultado = simular_retorno(valor_inv, taxa, anos)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Valor Futuro",
                    f"R$ {resultado['valor_futuro']:,.2f}"
                )
            
            with col2:
                st.metric(
                    "Ganho Esperado",
                    f"R$ {resultado['ganho']:,.2f}",
                    delta=f"{resultado['taxa_efetiva']:.2f}%"
                )
            
            with col3:
                st.metric(
                    "Taxa Equivalente",
                    f"{resultado['taxa_efetiva']:.2f}%"
                )
            
            st.markdown("---")
            
            # Gráfico de crescimento ao longo do tempo
            ano_list = list(range(1, anos + 1))
            valor_list = [
                valor_inv * ((1 + taxa/100) ** ano) for ano in ano_list
            ]
            
            df_crescimento = pd.DataFrame({
                'Ano': ano_list,
                'Saldo': valor_list
            })
            
            st.line_chart(df_crescimento.set_index('Ano'))
    
    # ===== PÁGINA 4: RECOMENDAÇÕES =====
    elif pagina == "📈 Recomendações Personalizadas":
        st.header("📈 Recomendações Personalizadas")
        
        st.markdown(f"""
        **Seu Perfil financeiro:**
        - Renda Mensal: R$ {perfil['renda_mensal']:,.2f}
        - Saldo Atual: R$ {perfil['saldo_atual']:,.2f}
        - Perfil de Risco: {perfil['perfil_risco'].upper()}
        - Objetivo: {perfil['objetivo_principal']}
        - Horizonte: {perfil['tempo_horizonte']}
        """)
        
        st.markdown("---")
        
        # Obter recomendações
        recomendacoes = recomendar_produtos(perfil, produtos)
        
        # Filtrar por elegibilidade
        elegíveis = [r for r in recomendacoes if r['elegibilidade'] == 'Elegível']
        
        st.subheader(f"✅ Produtos Recomendados ({len(elegíveis)})")
        
        for i, rec in enumerate(elegíveis[:3], 1):
            with st.expander(f"**{i}. {rec['nome']}** - ⭐ Compatibilidade: {rec['compatibilidade']}/5"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Tipo", rec['tipo'])
                    st.metric("Risco", rec['risco'].upper())
                
                with col2:
                    st.metric("Rentabilidade", f"{rec['rentabilidade']:.1f}%/ano")
                    st.metric("Taxa Admin", f"{rec['taxa_admin']:.2f}%")
                
                with col3:
                    st.metric("Mínimo", f"R$ {rec['minimo']:.2f}")
                    st.metric("Status", rec['elegibilidade'])
                
                # Mini simulação
                st.markdown("---")
                st.markdown("**Simulação Rápida:**")
                resultado = simular_retorno(5000, rec['rentabilidade'], 1)
                st.write(f"Se investir R$ 5.000, em 1 ano teria: **R$ {resultado['valor_futuro']:,.2f}** (ganho de **R$ {resultado['ganho']:,.2f}**)")
        
        if not elegíveis:
            st.warning("⚠️ Nenhum produto elegível no momento. Acumule mais saldo para começar a investir!")
    
    # ===== PÁGINA 5: SOBRE =====
    elif pagina == "ℹ️ Sobre Sofia":
        st.header("ℹ️ Sobre a Sofia Finance")
        
        st.markdown("""
        ## Quem sou?
        
        Sou **Sofia Finance**, uma consultora financeira digital inteligente, criada para ajudar você a:
        
        ✅ **Entender** suas finanças pessoais  
        ✅ **Otimizar** seus gastos e economias  
        ✅ **Investir** de forma segura e inteligente  
        ✅ **Construir** patrimônio ao longo do tempo  
        
        ## Meus Diferenciais
        
        🤖 **IA Generativa** - Conversas naturais e personalizadas  
        📊 **Dados Reais** - Baseada em seu perfil e transações reais  
        🎯 **Recomendações Seguras** - Sem alucinações, sem garantias falsas  
        📚 **Educadora** - Explico cada conceito de forma clara  
        🛡️ **Segura** - Suas informações estão protegidas  
        
        ## Como Funciono?
        
        1. **Coleto seu contexto** - Seu perfil, renda, objetivos, gastos
        2. **Analiso padrões** - Onde você gasta mais, quanto economiza
        3. **Recomendo produtos** - CDB, Fundo, Tesouro, alinhados com seu perfil
        4. **Faço simulações** - Mostro quanto cada investimento renderá
        5. **Educo** - Explico o "por quê" de cada recomendação
        
        ## Roadmap Futuro
        
        🟦 **V1** (Atual) - Chat + Análise de Gastos + Simulações  
        🟩 **V2** (Próxima) - Integração com APIs bancárias reais  
        🟥 **V3** (Futura) - Alertas automáticos, previsões de mercado  
        
        ## Contato / Feedback
        
        Tem sugestões? Detectou algum erro? Quer dar feedback?  
        Entre em contato conosco: **[seu-email@exemplo.com]**
        
        ---
        
        **Última atualização**: {datetime.now().strftime("%d/%m/%Y %H:%M")}
        """)
    
    # ===== PÁGINA 6: HISTÓRICO =====
    elif pagina == "💬 histórico":
        st.header("📜 Histórico de Atendimentos")
        
        st.markdown("Veja como clientes foram atendidos pela Sofia no passado:")
        
        st.dataframe(
            df_historico,
            use_container_width=True,
            hide_index=True
        )
        
        # Estatísticas
        st.markdown("---")
        st.subheader("📊 Estatísticas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Atendimentos", len(df_historico))
        
        with col2:
            satisfacao_media = df_historico['satisfacao'].mean()
            st.metric("Satisfação Média", f"{satisfacao_media:.1f}/5")
        
        with col3:
            dúvida_top = df_historico['tipo_duvida'].value_counts().index[0]
            st.metric("Dúvida Mais Comum", dúvida_top)
        
        # Gráfico de satisfação
        st.bar_chart(df_historico.groupby('tipo_duvida')['satisfacao'].mean())
    
    # ===== RODAPÉ =====
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #777; font-size: 0.85em; padding: 20px 0;">
            <p>Desenvolvido por patrick lima, parte do projeto de certificação DIO</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def gerar_resposta_sofia(pergunta, perfil, df_transacoes, produtos):
    """
    Gera resposta inteligente baseada na pergunta e contexto
    
    Estratégia:
    - Detectar padrões na pergunta
    - Usar conhecimento do perfil e transações
    - Fornecer resposta contextualizada
    """
    pergunta_lower = pergunta.lower()
    
    # ===== INTENÇÕES DETECTADAS =====
    
    # 1. PERGUNTA SOBRE INVESTIMENTOS
    if any(word in pergunta_lower for word in ["investir", "investimento", "rendimento", "retorno"]):
        analise = analisar_gastos(df_transacoes)
        economia_mensal = perfil['renda_mensal'] - analise['gastos_totais'] / len(df_transacoes)
        
        return f"""
Ótima pergunta! {perfil['nome']}, vejo que sua situação é:

📊 **SUA SITUAÇÃO**:
- Renda Mensal: R$ {perfil['renda_mensal']:,.2f}
- Gastos Totais: R$ {analise['gastos_totais']:,.2f}
- Saldo Atual: R$ {perfil['saldo_atual']:,.2f}
- Economia Mensal: ~R$ {economia_mensal:,.2f}

💡 **RECOMENDAÇÃO**:
Para seu perfil **{perfil['perfil_risco'].upper()}**, sugiro:
1. **CDB** - Seguro, rendimento de 10.5% ao ano
2. **Fundo Conservador** - Diversificação, 8.5% ao ano
3. **Tesouro Direto** - Muito seguro, 9.2% ao ano

Se investir R$ 5.000 em CDB:
- Ano 1: R$ 5.525 (ganho de R$ 525)
- Ano 3: R$ 6.637 (ganho de R$ 1.637)
- Ano 5: R$ 8.053 (ganho de R$ 3.053)

Qual desses produtos você gostaria de explorar mais?
"""
    
    # 2. PERGUNTA SOBRE GASTOS
    elif any(word in pergunta_lower for word in ["gasto", "despesa", "economia", "economizar"]):
        analise = analisar_gastos(df_transacoes)
        maior_categoria = max(analise['por_categoria'], key=analise['por_categoria'].get)
        maior_valor = analise['por_categoria'][maior_categoria]
        
        return f"""
Vamos analisar seus gastos, {perfil['nome']}!

💸 **RESUMO**:
- Total Gasto: R$ {analise['gastos_totais']:,.2f}
- Gasto Médio: R$ {analise['gasto_medio']:,.2f}
- Categoria Principal: {maior_categoria} (R$ {maior_valor:,.2f})

📊 **SUAS CATEGORIAS**:
"""+ "\n".join([f"- {cat}: R$ {val:,.2f}" for cat, val in analise['por_categoria'].items()]) + f"""

⚠️ **OPORTUNIDADE**:
Se você reduzir {maior_categoria} em 20%, economizaria R$ {maior_valor * 0.2:,.2f}/mês.
Em um ano: **R$ {maior_valor * 0.2 * 12:,.2f}**!

Quer que a ajude a criar um plano de economia?
"""
    
    # 3. PERGUNTA SOBRE METAS/OBJETIVOS
    elif any(word in pergunta_lower for word in ["meta", "objetivo", "quanto tempo", "futuro"]):
        return f"""
Ótimo, {perfil['nome']}! Seu objetivo é: **{perfil['objetivo_principal']}**

Vamos calcular como chegar lá:

🎯 **SEU OBJETIVO**:
- Horizonte: {perfil['tempo_horizonte']}
- Perfil: {perfil['perfil_risco']}

💰 **ESTIMAÇÃO**:
Com seu saldo atual de R$ {perfil['saldo_atual']:,.2f}, investindo em produtos com rendimento de 8-10% ao ano:
- Ano 5: R$ {perfil['saldo_atual'] * 1.47:,.2f}
- Ano 10: R$ {perfil['saldo_atual'] * 2.16:,.2f}
- Ano 20: R$ {perfil['saldo_atual'] * 4.66:,.2f}

Se adicionar R$ 500/mês:
- Ano 5: R$ {perfil['saldo_atual'] * 1.47 + 35000:,.2f}
- Ano 10: R$ {perfil['saldo_atual'] * 2.16 + 80000:,.2f}
- Ano 20: R$ {perfil['saldo_atual'] * 4.66 + 200000:,.2f}

Seu objetivo é totalmente alcançável! Quer criar um plano?
"""
    
    # 4. PERGUNTA EDUCACIONAL
    elif any(word in pergunta_lower for word in ["o que é", "como funciona", "diferença", "explica"]):
        if "cdb" in pergunta_lower:
            return f"""
Ótima pergunta, {perfil['nome']}! Deixa eu explicar:

## O que é CDB?

CDB = **Certificado de Depósito Bancário**

É como você emprestasse dinheiro para o banco, e ele te paga juros por isso.

### Como funciona:
1. Você investe R$ 5.000 no CDB
2. Banco garante ~10.5% de retorno ao ano
3. Após 1 ano, você recebe R$ 5.525

### Por que é seguro?
- Se o banco quebra, você é protegido (até R$ 250 mil - FGC)
- Risco é MUITO BAIXO
- Retorno é GARANTIDO

### Comparação:
- **Poupança**: 0.5%/ano (pouco retorno)
- **CDB**: 10.5%/ano (melhor!)
- **Fundo**: 8.5%/ano (menos seguro que CDB, mais que ações)

## Recomendação para você:
Para começar, recomendo CDB! É seguro, retorna bem, e você entende facilmente.

Quer investir?
"""
        elif "fundo" in pergunta_lower:
            return f"""
Ótima pergunta, {perfil['nome']}! Deixa eu explicar:

## O que é Fundo de Investimento?

Um **Fundo** é como um clube de investidores. Você coloca seu dinheiro, e um gestor investe em vários ativos.

### Como funciona:
1. Você investe R$ 5.000
2. Gestor investe em múltiplos produtos (ações, títulos, etc.)
3. Você lucra com a diversificação

### Tipos:
- **Conservador**: Títulos seguros (8.5%/ano)
- **Moderado**: Mix de seguro + risco (9-11%/ano)
- **Agressivo**: Ações e crescimento (12%+/ano)

### Diferença do CDB:
| CDB | Fundo |
|-----|-------|
| Garantido | Não garantido (menos previsível) |
| 10.5% | 8-12% |
| Menos diversificado | Muito diversificado |
| Sem volatilidade | Com volatilidade |

## Recomendação para você:
Para diversificar, sugiro: 60% CDB + 40% Fundo

Faz sentido?
"""
        else:
            return f"""
Entendi sua pergunta, {perfil['nome']}! Vou tentar esclarecer:

### Conceitos Financeiros Básicos:

💰 **Investimento**: Colocar dinheiro em ativos para gerar retorno
📊 **Rentabilidade**: Quanto seu dinheiro rende (%)
🎯 **Risco**: Possibilidade de perder dinheiro
⏱️ **Horizonte**: Tempo até precisar do dinheiro

Se quiser saber mais sobre um conceito específico, pergunte!

Alguns termos que posso explicar:
- O que é CDB?
- O que é Fundo?
- O que é Tesouro Direto?
- Como funciona a Bolsa?
- O que é Diversificação?

Qual desses você quer aprender?
"""
    
    # 5. PERGUNTA GENÉRICA
    else:
        return f"""
Oi {perfil['nome']}! 👋

Entendi sua pergunta, mas vou precisar de mais detalhes para ajudar melhor!

Posso ajudá-lo com:
📊 **Análise de Gastos** - Onde você gasta dinheiro
💰 **Recomendações de Investimento** - Qual produto é melhor para você
🧮 **Simulações** - Quanto seus investimentos renderão
📚 **Educação Financeira** - Explicar conceitos (CDB, Fundo, etc.)
🎯 **Planejamento de Metas** - Como atingir seus objetivos

O que você gostaria de fazer?
"""


if __name__ == "__main__":
    main()
