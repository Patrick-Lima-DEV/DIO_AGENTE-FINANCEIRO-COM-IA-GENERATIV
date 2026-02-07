# 📚 Exemplos de Implementação

Este diretório contém exemplos de implementação para extensões e integrações da Sofia Finance.

## 📋 Índice

1. [Integração com OpenAI GPT](#integração-com-openai-gpt)
2. [Integração com Google Gemini](#integração-com-google-gemini)
3. [Cálculo de Recomendações](#cálculo-de-recomendações)
4. [Análise de Gastos Avançada](#análise-de-gastos-avançada)
5. [Persistência de Dados](#persistência-de-dados)

---

## 🤖 Integração com OpenAI GPT

### Setup Básico
```python
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def consultar_gpt(pergunta, contexto_cliente):
    """
    Consulta GPT-4 com prompt estruturado
    """
    system_prompt = """
    Você é Sofia Finance, uma consultora financeira digital.
    Personalize as respostas com base no contexto do cliente.
    Nunca invente dados. Se não souber, diga 'Não tenho essa informação'.
    """
    
    user_message = f"""
    Contexto do Cliente:
    - Nome: {contexto_cliente['nome']}
    - Renda: R$ {contexto_cliente['renda']:,.2f}
    - Saldo: R$ {contexto_cliente['saldo']:,.2f}
    - Perfil: {contexto_cliente['perfil_risco']}
    
    Pergunta: {pergunta}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message['content']

# Exemplo de uso
cliente = {
    "nome": "João",
    "renda": 5000,
    "saldo": 15000,
    "perfil_risco": "moderado"
}

resposta = consultar_gpt(
    "Devo investir em fundo ou CDB?",
    cliente
)

print(resposta)
```

### Com Stream (Resposta em Tempo Real)
```python
def consultar_gpt_stream(pergunta, contexto_cliente):
    """
    Usa streaming para resposta em tempo real
    """
    system_prompt = """Você é Sofia Finance..."""
    
    user_message = f"""Contexto do Cliente:..."""
    
    stream = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[...],
        stream=True
    )
    
    resposta_completa = ""
    for chunk in stream:
        if "content" in chunk["choices"][0]["delta"]:
            texto = chunk["choices"][0]["delta"]["content"]
            resposta_completa += texto
            print(texto, end="", flush=True)  # Mostra em tempo real
    
    return resposta_completa
```

---

## 🌐 Integração com Google Gemini

### Setup Básico
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def consultar_gemini(pergunta, contexto_cliente):
    """
    Consulta Google Gemini com prompt estruturado
    """
    model = genai.GenerativeModel('gemini-pro')
    
    prompt_completo = f"""
    Você é Sofia Finance, consultora financeira digital.
    
    Contexto do Cliente:
    - Nome: {contexto_cliente['nome']}
    - Renda: R$ {contexto_cliente['renda']:,.2f}
    - Saldo: R$ {contexto_cliente['saldo']:,.2f}
    - Perfil: {contexto_cliente['perfil_risco']}
    
    Pergunta: {pergunta}
    
    Responda de forma personalizada, educativa e segura.
    """
    
    response = model.generate_content(
        prompt_completo,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.8,
        }
    )
    
    return response.text

# Exemplo de uso
cliente = {
    "nome": "Maria",
    "renda": 6000,
    "saldo": 20000,
    "perfil_risco": "agressivo"
}

resposta = consultar_gemini(
    "Como investir R$ 5.000?",
    cliente
)

print(resposta)
```

---

## 📊 Cálculo de Recomendações

### Sistema de Scoring
```python
import json

def calcular_score_produto(cliente, produto):
    """
    Calcula score de compatibilidade entre cliente e produto
    Escala: 0-100
    """
    score = 0
    detalhes = {}
    
    # 1. Compatibilidade de Risco (40 pontos)
    if cliente['perfil_risco'] in produto.get('perfil_recomendado', []):
        score += 40
        detalhes['risco'] = 'Totalmente compatível'
    elif cliente['perfil_risco'] == 'moderado' and 'moderado' in produto.get('perfil_recomendado', []):
        score += 30
        detalhes['risco'] = 'Compatível'
    else:
        score += 0
        detalhes['risco'] = 'Incompatível'
    
    # 2. Elegibilidade de Saldo (30 pontos)
    saldo_minimo = produto.get('minimo_investimento', 0)
    if cliente['saldo'] >= saldo_minimo * 2:
        score += 30
        detalhes['saldo'] = 'Excelente'
    elif cliente['saldo'] >= saldo_minimo:
        score += 20
        detalhes['saldo'] = 'Adequado'
    else:
        score += 0
        detalhes['saldo'] = 'Insuficiente'
    
    # 3. Alinhamento com Objetivo (20 pontos)
    if 'longo prazo' in cliente.get('tempo_horizonte', ''):
        if produto.get('risco') in ['baixo', 'muito_baixo']:
            score += 20
            detalhes['objetivo'] = 'Alinhado'
    else:
        score += 10
        detalhes['objetivo'] = 'Parcialmente alinhado'
    
    # 4. Não-Duplicação (10 pontos)
    if produto['tipo'] not in cliente.get('investimentos_atuais', []):
        score += 10
        detalhes['diversificacao'] = 'Boa'
    else:
        score += 0
        detalhes['diversificacao'] = 'Possibilita diversificação'
    
    return {
        'score': score,
        'percentual': f"{score:.0f}%",
        'detalhes': detalhes
    }

# Exemplo de uso
cliente = {
    'nome': 'Pedro',
    'perfil_risco': 'moderado',
    'saldo': 5000,
    'tempo_horizonte': 'longo prazo',
    'investimentos_atuais': []
}

produto = {
    'nome': 'CDB Seguro',
    'tipo': 'Certificado',
    'perfil_recomendado': ['conservador', 'moderado'],
    'minimo_investimento': 50,
    'risco': 'muito_baixo'
}

resultado = calcular_score_produto(cliente, produto)
print(f"Score: {resultado['percentual']}")
print(f"Detalhes: {resultado['detalhes']}")
```

### Filtragem Inteligente
```python
def filtrar_produtos_recomendados(cliente, produtos_json):
    """
    Filtra e ordena produtos por relevância
    """
    with open(produtos_json) as f:
        produtos_db = json.load(f)
    
    recomendacoes = []
    
    for produto in produtos_db['produtos']:
        score_resultado = calcular_score_produto(cliente, produto)
        
        if score_resultado['score'] >= 50:  # Mínimo 50%
            recomendacoes.append({
                'produto': produto['nome'],
                'score': score_resultado['score'],
                'tipo': produto['tipo'],
                'rentabilidade': produto.get('rentabilidade_anual'),
                'detalhes': score_resultado['detalhes']
            })
    
    # Ordenar por score (descendente)
    recomendacoes.sort(key=lambda x: x['score'], reverse=True)
    
    return recomendacoes

# Exemplo
cliente = {...}
top_produtos = filtrar_produtos_recomendados(cliente, 'data/produtos_financeiros.json')

for i, prod in enumerate(top_produtos[:3], 1):
    print(f"{i}. {prod['produto']}: {prod['score']:.0f}%")
```

---

## 💰 Análise de Gastos Avançada

### Clustering de Gastos
```python
import pandas as pd
from collections import defaultdict

def analisar_gastos_por_periodo(df_transacoes):
    """
    Agrupa gastos por período e identifica tendências
    """
    df = pd.read_csv(df_transacoes) if isinstance(df_transacoes, str) else df_transacoes
    df['data'] = pd.to_datetime(df['data'])
    
    df_debito = df[df['tipo'] == 'debito'].copy()
    df_debito['mes'] = df_debito['data'].dt.to_period('M')
    
    analise_mensal = df_debito.groupby(['mes', 'categoria'])['valor'].sum().unstack(fill_value=0)
    
    return analise_mensal

def identificar_anomalias(df_transacoes, threshold_desvio=2.0):
    """
    Identifica transações anômalas (outliers)
    """
    df = pd.read_csv(df_transacoes) if isinstance(df_transacoes, str) else df_transacoes
    df_debito = df[df['tipo'] == 'debito'].copy()
    
    # Calcular média e desvio padrão
    media = df_debito['valor'].mean()
    desvio = df_debito['valor'].std()
    limite_superior = media + (desvio * threshold_desvio)
    
    anomalias = df_debito[df_debito['valor'] > limite_superior]
    
    return {
        'media': media,
        'desvio': desvio,
        'limite': limite_superior,
        'anomalias': anomalias.to_dict('records')
    }

# Exemplo
analise = analisar_gastos_por_periodo('data/transacoes.csv')
print(analise)

anomalias = identificar_anomalias('data/transacoes.csv')
print(f"Gastos anômalos (> R$ {anomalias['limite']:,.2f}):")
for anom in anomalias['anomalias']:
    print(f"  - {anom['descricao']}: R$ {anom['valor']:.2f}")
```

---

## 💾 Persistência de Dados

### Salvar Conversa em Banco de Dados
```python
import sqlite3
from datetime import datetime

def salvar_interacao(cliente_id, pergunta, resposta, satisfacao=None):
    """
    Salva interação em banco SQLite
    """
    conexao = sqlite3.connect('data/conversas.db')
    cursor = conexao.cursor()
    
    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interacoes (
            id INTEGER PRIMARY KEY,
            cliente_id TEXT,
            data TIMESTAMP,
            pergunta TEXT,
            resposta TEXT,
            satisfacao INTEGER
        )
    ''')
    
    cursor.execute('''
        INSERT INTO interacoes (cliente_id, data, pergunta, resposta, satisfacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, datetime.now(), pergunta, resposta, satisfacao))
    
    conexao.commit()
    conexao.close()

def recuperar_historico_cliente(cliente_id, limite=10):
    """
    Recupera últimas interações do cliente
    """
    conexao = sqlite3.connect('data/conversas.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
        SELECT pergunta, resposta, data, satisfacao
        FROM interacoes
        WHERE cliente_id = ?
        ORDER BY data DESC
        LIMIT ?
    ''', (cliente_id, limite))
    
    resultados = cursor.fetchall()
    conexao.close()
    
    return resultados

# Exemplo
salvar_interacao(
    cliente_id="CLI001",
    pergunta="Como investir R$ 5.000?",
    resposta="Recomendo CDB + Fundo...",
    satisfacao=5
)

historico = recuperar_historico_cliente("CLI001")
for pergunta, resposta, data, satisfacao in historico:
    print(f"[{data}] {pergunta} → ⭐{satisfacao}")
```

---

## 🧪 Testes Unitários

```python
import unittest
from app import simular_retorno, analisar_gastos

class TestCalculosFinanceiros(unittest.TestCase):
    
    def test_simular_retorno(self):
        """Testa cálculo de retorno"""
        resultado = simular_retorno(1000, 10, 1)
        self.assertEqual(resultado['valor_futuro'], 1100.0)
        self.assertEqual(resultado['ganho'], 100.0)
    
    def test_simular_retorno_zero(self):
        """Testa com taxa zero"""
        resultado = simular_retorno(1000, 0, 1)
        self.assertEqual(resultado['valor_futuro'], 1000.0)
    
    def test_analisar_gastos(self):
        """Testa análise de gastos"""
        import pandas as pd
        df = pd.DataFrame({
            'tipo': ['debito', 'debito', 'credito'],
            'valor': [100, 200, 1000],
            'categoria': ['Alimentação', 'Transporte', 'Salário']
        })
        
        analise = analisar_gastos(df)
        self.assertEqual(analise['gastos_totais'], 300)

if __name__ == '__main__':
    unittest.main()
```

---

## 🚀 Deploy em Produção

### Streamlit Cloud
```bash
# 1. Criar conta em https://streamlit.io/cloud
# 2. Conectar repositório GitHub
# 3. Configurar secrets (API keys)
# 4. Deploy automático
```

### Variáveis de Ambiente Necessárias
```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
DATABASE_URL=postgres://...
```

---

## 📖 Recursos Adicionais

- [Streamlit Docs](https://docs.streamlit.io)
- [OpenAI API](https://platform.openai.com/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Dúvidas ou sugestões?** Abra uma issue no GitHub!

