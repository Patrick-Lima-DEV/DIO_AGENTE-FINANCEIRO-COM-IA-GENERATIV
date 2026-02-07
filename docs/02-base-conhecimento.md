# 02 - Base de Conhecimento do Agente

## 1. Estrutura de Dados e Fontes

A base de conhecimento do Agente Financeiro Inteligente é composta por dados estruturados e não-estruturados que alimentam as recomendações e respostas.

### Fontes de Dados

```
┌─────────────────────────────────────────┐
│     BASE DE CONHECIMENTO AGENTE         │
├─────────────────────────────────────────┤
│                                         │
│  ├─ DADOS ESTRUTURADOS (JSON/CSV)       │
│  │  ├─ Produtos Financeiros             │
│  │  ├─ Perfil de Investidor             │
│  │  ├─ Transações Históricas            │
│  │  └─ Histórico de Atendimento         │
│  │                                      │
│  ├─ REGRAS E LÓGICA                     │
│  │  ├─ Regras de Recomendação           │
│  │  ├─ Cálculos Financeiros             │
│  │  └─ Validações de Segurança          │
│  │                                      │
│  └─ CONHECIMENTO SEMÂNTICO              │
│     ├─ FAQs e Respostas Padrão          │
│     ├─ Conceitos Financeiros            │
│     └─ Casos de Uso Comuns              │
│                                         │
└─────────────────────────────────────────┘
```

---

## 2. Dados Estruturados

### 2.1 Produtos Financeiros (`produtos_financeiros.json`)

**Objetivo**: Catálogo atualizado de produtos recomendáveis

**Estrutura**:
```json
{
  "id": "PROD001",
  "nome": "Fundo Conservador ABC",
  "tipo": "Fundo de Renda Fixa",
  "rentabilidade_anual": 8.5,
  "minimo_investimento": 100.00,
  "taxa_administracao": 0.5,
  "risco": "baixo",
  "patrimonio": 50000000.00,
  "descricao": "Fundo focado em títulos públicos e privados com baixa volatilidade",
  "publico_alvo": "Iniciantes, conservadores",
  "perfil_recomendado": ["conservador", "moderado"]
}
```

**Campos Utilizados pelo Agente**:
- `tipo`: Para categorizar produtos
- `risco`: Para alinhar com perfil do cliente
- `rentabilidade_anual`: Para simulações de retorno
- `minimo_investimento`: Para ver viabilidade de purchase
- `taxa_administracao`: Para calcular custo real
- `perfil_recomendado`: Para recomendar produtos compatíveis

**Produtos Disponíveis**:
1. Fundo Conservador ABC (Renda Fixa)
2. Fundo Dinâmico XYZ (Ações)
3. CDB Seguro 120% CDI
4. Tesouro Direto
5. Seguro de Vida Universal
6. Cartão de Crédito Premium

---

### 2.2 Perfil de Investidor (`perfil_investidor.json`)

**Objetivo**: Contexto detalhado do cliente para personalização

**Campos Principais**:

| Campo | Objetivo |
|-------|----------|
| `cliente_id` | Identificação única |
| `renda_mensal` | Base para calcular % máximo de investimento |
| `saldo_atual` | Para simulações |
| `perfil_risco` | Definir agressividade de recomendações |
| `objetivo_principal` | Direcionar estratégia |
| `tempo_horizonte` | Definir produtos adequados |
| `investimentos_atuais` | Não duplicar recomendações |
| `limite_credito` | Informar capacidade de dívida |
| `emprestimos` | Considerar na recomendação |

**Questão de Diseño**: Qual é o impacto de cada campo?

```
investimentos_atuais → Se tem R$ 19.000 em fundos de ações,
                       talvez precise diversificar para renda fixa

emprestimos → Se tem R$ 150.000 devedor em imóvel,
              recomender investimento arriscado é irresponsável

limite_credito → Máximo que pode tomar emprestado
```

---

### 2.3 Transações Históricas (`transacoes.csv`)

**Objetivo**: Analisar padrões de gastos e receitas do cliente

**Campos**:
- `data`: Data da transação
- `tipo`: Crédito ou débito
- `descricao`: Detalhamento
- `valor`: Montante em R$
- `categoria`: Classificação (Alimentação, Transporte, etc.)
- `saldo_apos`: Saldo resultante

**Análises Derivadas**:

```python
# Calcular gastos por categoria
gastos_por_categoria = df[df['tipo'] == 'debito'].groupby('categoria')['valor'].sum()

# Média de gastos mensais
media_gastos = df[df['tipo'] == 'debito']['valor'].mean()

# Gastos em lazer vs. necessidades
discretos = ['Lazer', 'Compras Online', 'Restaurante']
gastos_discretos = df[df['categoria'].isin(discretos)]['valor'].sum()

# Receita total
receita_total = df[df['tipo'] == 'credito']['valor'].sum()
```

---

### 2.4 Histórico de Atendimento (`historico_atendimento.csv`)

**Objetivo**: Aprender com interações passadas e melhorar respostas

**Campos**:
- `data_atendimento`: Quando foi o atendimento
- `tipo_duvida`: Categoria (Investimentos, Empréstimo, etc.)
- `pergunta`: Pergunta original do cliente
- `resposta_agente`: O que foi respondido
- `satisfacao`: Score 1-5 de satisfaction

**Utilização**:
1. **Few-Shot Learning**: Usar exemplos de respostas bem-avaliadas
2. **Detecção de Padrões**: Dúvidas frequentes → criar FAQs
3. **Melhoria Contínua**: Quais tipos de pergunta geram insatisfação?

---

## 3. Regras de Recomendação

### 3.1 Matriz de Recomendação Perfil → Produtos

```
┌──────────────┬──────────┬──────────┬────────┬────────┬──────┐
│ Perfil       │ Fundo    │ Fundo    │ CDB    │Tesouro │Seg   │
│              │ Cons.    │ Dinâmico │        │Direto  │      │
├──────────────┼──────────┼──────────┼────────┼────────┼──────┤
│ Conservador  │ ★★★★★   │ ✗        │ ★★★★★ │ ★★★★★ │ ★★★  │
│ Moderado     │ ★★★★    │ ★★       │ ★★★★  │ ★★★★  │ ★★★★ │
│ Agressivo    │ ★★      │ ★★★★★   │ ★★    │ ★★    │ ★★   │
└──────────────┴──────────┴──────────┴────────┴────────┴──────┘

★ = Recomendação de força (5 = Altamente Recomendado)
```

### 3.2 Lógica de Elegibilidade

```python
def pode_recomendar_produto(cliente, produto):
    """
    Valida se produto é adequado para cliente
    """
    # 1. Verifique se cliente tem saldo mínimo
    if cliente['saldo_atual'] < produto['minimo_investimento']:
        return False, "Saldo insuficiente"
    
    # 2. Verifique compatibilidade de perfil de risco
    if cliente['perfil_risco'] not in produto['perfil_recomendado']:
        return False, "Perfil incompatível"
    
    # 3. Se tem empréstimo alto, evite produtos arriscados
    if cliente['saldo_devedor'] > cliente['renda_mensal'] * 12:
        if produto['risco'] in ['alto', 'muito_alto']:
            return False, "Endividamento alto"
    
    # 4. Verifique se já tem investimento similar
    if produto['tipo'] in cliente['investimentos_atuais']:
        recomendacao = "Pode diversificar"  # Warn only
    
    return True, "Elegível"
```

---

## 4. Cálculos Financeiros Essenciais

### 4.1 Simulação de Retorno

```python
def simular_retorno(valor_investimento, taxa_anual, anos, composicao="anual"):
    """
    Calcula retorno estimado de um investimento
    Formula: FV = PV * (1 + r)^n
    """
    resultado = valor_investimento * (1 + taxa_anual/100) ** anos
    ganho = resultado - valor_investimento
    
    return {
        "valor_futuro": round(resultado, 2),
        "ganho_esperado": round(ganho, 2),
        "taxa_efetiva": round((ganho / valor_investimento) * 100, 2)
    }

# Exemplo
simular_retorno(5000, 8.5, 1)
# Output: {'valor_futuro': 5425.0, 'ganho_esperado': 425.0, 'taxa_efetiva': 8.5}
```

### 4.2 Análise de Gastos vs. Receita

```python
def analisar_saude_financeira(cliente_df, perfil):
    """
    Calcula ratio gastos/receita e identifica oportunidades
    """
    receita_total = perfil['renda_mensal']
    gastos_total = cliente_df[cliente_df['tipo'] == 'debito']['valor'].sum()
    
    taxa_poupanca = (receita_total - gastos_total) / receita_total * 100
    
    # Classificação
    if taxa_poupanca >= 20:
        saude = "Excelente (economizando bem)"
    elif taxa_poupanca >= 10:
        saude = "Boa (pode melhorar)"
    else:
        saude = "Crítica (gastos altos)"
    
    return {
        "receita_mensal": receita_total,
        "gastos_mensais": gastos_total,
        "economia_mensal": receita_total - gastos_total,
        "taxa_poupanca": round(taxa_poupanca, 2),
        "saude": saude
    }
```

### 4.3 Tempo para Atingir Meta

```python
def calcular_tempo_meta(valor_atual, meta, economia_mensal, taxa_anual):
    """
    Monte Carlo simplificado: quanto tempo para atingir objetivo?
    """
    meses = 0
    saldo = valor_atual
    
    while saldo < meta and meses < 600:  # Max 50 anos
        # Adiciona economia mensal
        saldo += economia_mensal
        # Adiciona retorno do investimento
        saldo += saldo * (taxa_anual / 100 / 12)
        meses += 1
    
    return {
        "meses": meses,
        "anos": round(meses / 12, 1),
        "alcancar": saldo >= meta
    }
```

---

## 5. FAQs Estruturadas

### 5.1 Por Tipo de Produto

#### Fundos de Investimento
- **P: Qual é a diferença entre Fundo Conservador e Dinâmico?**  
  R: Conservador investe em títulos baixo-risco (renda fixa). Dinâmico em ações, mais volátil mas com potencial maior.

- **P: Existe risco de perder todo meu dinheiro em um fundo?**  
  R: Fundos são diversificados, reduzindo risco. Breakup total é raro, mas possível em cenários extremos.

#### CDB e Tesouro Direto
- **P: Qual a diferença entre CDB e Tesouro Direto?**  
  R: CDB é dívida bancária (instituição específica). TD é dívida do governo (mais seguro).

- **P: Posso sacar meu CDB antes do prazo?**  
  R: Sim, mas pode receber menos due a variação de taxas.

#### Seguros
- **P: Preciso de seguro de vida?**  
  R: Se tem dependentes ou dívidas, sim. Garante suporte financeiro à família.

### 5.2 Por Cenário Financeiro

#### Cliente com Dívida Alta
- Priorize pagar dívida primeiro
- Invista pouco até reduzir endividamento
- Maximize taxa de poupança

#### Cliente com Renda Instável (Freelancer)
- Fundo emergência 6 meses de gastos
- Investimentos conservadores
- Simulações pessimistas (renda -20%)

#### Cliente Próximo à Aposentadoria
- Reduzir volatilidade gradualmente
- Focar em renda fixa
- Planejamento tributário (pode exigir especialista)

---

## 6. Verificações de Segurança

### 6.1 Checks Antes de Recomendar

```python
def validar_recomendacao(cliente, produto, valor):
    """
    Verifica segurança da recomendação antes de oferecer
    """
    checks = {
        "saldo_suficiente": cliente['saldo_atual'] >= valor,
        "perfil_compativel": cliente['perfil_risco'] in produto['perfil_recomendado'],
        "endereco_baixo": cliente['saldo_devedor'] / cliente['renda_mensal'] < 3,
        "diversificacao": produto['tipo'] not in cliente['investimentos_atuais'],
        "prazo_adequado": cliente['tempo_horizonte'] >= produto['prazo_minimo']
    }
    
    # Se não passar em algum check, marque como "warn"
    warnings = [k for k, v in checks.items() if not v]
    
    return all(checks.values()), warnings
```

### 6.2 Disclaimers Obrigatórios

**Para Ações / Produtos Arriscados**:
> "⚠️ Fundos de Ações têm volatilidade alta. Seu saldo pode cair significativamente no curto prazo. Recomendado apenas para horizonte > 5 anos e perfil agressivo."

**Para Valores Altos**:
> "⚠️ Você está considerando investir R$ 50.000. Confirme que possui fundo emergencial e que este valor não fará falta nos próximos 12 meses."

---

## 7. Fluxo de Consulta de Conhecimento

```
1. Cliente faz pergunta
   ↓
2. NLP identifica intenção + entidades
   ↓
3. Agente coleta contexto relevante:
   - Perfil do cliente
   - Transações relevantes
   - Histórico de atendimento similar
   - Produtos compatíveis
   ↓
4. Agente busca em FAQs estruturadas
   ↓
5. Se existe resposta direta → Return
   Se não → Racional:
   ↓
6. Usa regras + cálculos para raciocinar
   ↓
7. Valida recomendação (checks de segurança)
   ↓
8. Formata resposta com:
   - Explicação clara
   - Cálculos demonstrativos
   - Produtos recomendados (com ★)
   - Disclaimers se necessário
   ↓
9. Armazena interação no histórico para aprendizado
```

---

## 8. Métricas de Qualidade da Base

### 8.1 Cobertura de Knowledge

```
Cobertura = (Perguntas respondidas com dados) / Total ×100%
Meta: 85%+

Exemplo:
- Pergunta: "Qual fundo tem melhor rendimento?" ✓ (em produtos_financeiros.json)
- Pergunta: "Qual é o dólar hoje?" ✗ (não em base)
```

### 8.2 Acurácia de Recomendação

```
Acurácia = Clientes satisfeitos com recomendação / Total × 100%
Meta: 80%+

Medição: Score de satisfação nos atendimentos
```

---

## Conclusão

A base de conhecimento do Agente é construída em camadas:
1. **Dados Brutos**: Transações, perfil, produtos
2. **Regras Lógicas**: Quando recomendar cada produto
3. **Cálculos**: Simulações precisas
4. **FAQs**: Respostas rápidas e consistentes
5. **Safeguards**: Evita alucinações e recomendações perigosas

Essa estrutura permite respostas confiáveis, personalizadas e sempre grounded em dados reais.
