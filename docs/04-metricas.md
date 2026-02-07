# 04 - Avaliação e Métricas

## 1. Framework de Avaliação

O Agente Financeiro Inteligente será avaliado em 4 dimensões:

```
┌──────────────────────────────────────────────────┐
│         FRAMEWORK DE AVALIAÇÃO DO AGENTE         │
├──────────────────────────────────────────────────┤
│                                                  │
│ ✓ PRECISÃO & ASSERTIVIDADE                       │
│   └─ Informações corretas e alinhadas com dados │
│                                                  │
│ ✓ SEGURANÇA & CONFIABILIDADE                     │
│   └─ Sem alucinações, sem garantias falsas      │
│                                                  │
│ ✓ PERSONALIZAÇÃO & RELEVÂNCIA                    │
│   └─ Respostas alinhadas ao perfil do cliente   │
│                                                  │
│ ✓ EXPERIÊNCIA & SATISFAÇÃO                       │
│   └─ Clareza, tom, helpfulness                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 2. Métricas Principais

### 2.1 PRECISÃO & ASSERTIVIDADE

#### Métrica 1: Taxa de Acurácia de Fatos
**Definição**: % de informações que são corretamente citadas vs. base de dados

**Como Medir**:
```
Acurácia = (Fatos Verificados Corretos / Total de Fatos Citados) × 100%

Meta: 95%+
```

**Exemplos**:
| Resposta | Verificação | Resultado |
|----------|------------|-----------|
| "Fundo ABC rende 8.5% ao ano" | produtos_financeiros.json | ✓ Correto (95%) |
| "CDB rende 15% ao ano" | CDB real é 10.5% | ✗ Incorreto (alucinação) |
| "Taxa média de Ações é 12%" | Não em base de dados | ⚠️ Estimativa (70%) |

**Como Implementar**:
```python
def avaliar_acuracia_fatos(resposta_agente, base_conhecimento):
    """
    Extrai fatos numéricos da resposta e valida
    """
    fatos = extrair_fatos_numericos(resposta_agente)
    corretos = 0
    
    for fato in fatos:
        if validar_contra_base(fato, base_conhecimento):
            corretos += 1
    
    acuracia = (corretos / len(fatos)) * 100 if fatos else 100
    return acuracia
```

#### Métrica 2: Relevância de Recomendações
**Definição**: % de produtos recomendados que fazem sentido para o cliente

**Como Medir**:
```
Relevância = (Produtos Alinhados com Perfil / Total Recomendado) × 100%

Meta: 85%+
```

**Validação**:
```python
def validar_relevancia_recomendacao(cliente, produto):
    """
    Valida se recomendação faz sentido
    """
    checks = {
        "perfil_compativel": cliente['perfil_risco'] in produto['perfil_recomendado'],
        "saldo_suficiente": cliente['saldo_atual'] >= produto['minimo_investimento'],
        "nao_duplicado": produto['tipo'] not in cliente['investimentos_atuais'],
        "nao_sobreendividado": cliente['saldo_devedor'] < cliente['renda_mensal'] * 5,
        "tempo_horizonte_ok": cliente['tempo_horizonte'] >= produto.get('prazo_minimo', 0)
    }
    return sum(checks.values()) / len(checks)
```

---

### 2.2 SEGURANÇA & CONFIABILIDADE

#### Métrica 3: Taxa de Alucinações (Hallucination Rate)
**Definição**: % de respostas que contêm informações fabricadas

**Como Medir**:
```
Taxa de Alucinação = (Respostas com Fatos Falsos / Total de Respostas) × 100%

Meta: <5% (objetivo: 0%)

Exemplo de Alucinação:
- "Novo Produto XYZ com 25% de retorno" (não existe em base)
- "Taxa de juros da Caixa é 3% agora" (não temos dado em tempo real)
```

**Detection**:
```python
def detectar_alucinacoes(resposta, base_conhecimento):
    """
    Busca claims não verificáveis na resposta
    """
    claims = extrair_claims_principais(resposta)
    alucinacoes = []
    
    for claim in claims:
        if not pode_verificar(claim, base_conhecimento):
            alucinacoes.append(claim)
    
    taxa_alucinacao = len(alucinacoes) / len(claims) * 100
    return taxa_alucinacao, alucinacoes
```

#### Métrica 4: Taxa de Disclaimers Apropriados
**Definição**: % de respostas com disclaimer quando necessário

**Situações que EXIGEM Disclaimer**:
```
Quando recomendar produtos com risco alto:
  ⚠️ "Fundos de Ações têm volatilidade alta"
  
Quando prometer retornos:
  ⚠️ "Retornos passados não garantem futuros"
  
Quando cliente está muito endividado:
  ⚠️ "Dado seu nível de dívida, recomendo precaução"
  
Quando sair do escopo de expertise:
  ⚠️ "Para questões tributárias, consulte especialista"
```

**Medição**:
```
Disclaimer Compliance = (Disclaimers Apropriados / Situações que Exigem) × 100%

Meta: 100%
```

---

### 2.3 PERSONALIZAÇÃO & RELEVÂNCIA

#### Métrica 5: Nível de Contextualização
**Definição**: Quanto a resposta usa contexto específico do cliente

**Escala**:
```
0 = Resposta genérica (não menciona cliente)
1 = Menciona 1 contexto (ex: renda)
2 = Menciona 2-3 contextos (renda + objetivo + gasto)
3 = Resposta altamente personalizada (nome, histórico, perfil completo)

Meta: Média 2.5+ pontos
```

**Exemplo Progressivo**:

| Nível | Resposta |
|-------|----------|
| 0 | "CDB é um investimento seguro que rende 10% ao ano." |
| 1 | "João, CDB rende 10% ao ano e seria bom para você." |
| 2 | "João, considerando sua renda de R$ 5.000 e objetivo de aposentadoria em 20 anos, CDB seria uma base segura para seu portfólio." |
| 3 | "João, vi que seu maior gasto é com Lazer (R$ 1.200), deixando economia limitada. Com economia de R$ 700/mês em CDB a 10%, em 5 anos teríamos R$ 42.804, alinhado com seu objetivo de aposentadoria." |

**Implementação**:
```python
def medir_contextalizacao(resposta, cliente):
    """
    Conta quantos elementos de contexto foram usados
    """
    contextos = {
        'nome': cliente['nome'] in resposta,
        'renda': str(cliente['renda_mensal']) in resposta,
        'objetivo': cliente['objetivo_principal'].lower() in resposta.lower(),
        'historico': cliente['investimentos_atuais'] in resposta,
        'perfil': cliente['perfil_risco'] in resposta,
        'gasto': cliente['gasto_mensal'] in resposta
    }
    
    score = sum(contextos.values()) / len(contextos)
    return score
```

#### Métrica 6: Cobertura de Intençã
**Definição**: % de respostas que endereçam completamente a intenção do cliente

**Como classificar**:
```
Intençã = Objetivo Real       | Avaliação
---------------------------------------
Aprender sobre investimentos  | Resposta educou?
Economizar dinheiro           | Ofereceu plano?
Calcular retorno              | Fez simulação?
Resolver dúvida               | Esclareceu-a?
Receber recomendação          | Deu opções?

Cobertura = (Respostas Completas / Total) × 100%

Meta: 88%+
```

---

### 2.4 EXPERIÊNCIA & SATISFAÇÃO

#### Métrica 7: Satisfação do Cliente
**Definição**: Score subjetivo de satisfação pós-interação

**Como Implementar**:
```
Após cada conversa, pergunte:

"Em uma escala 1-5, quão satisfeito você ficou com a resposta?
1 = Muito insatisfeito
5 = Muito satisfeito

Por quê?"

Nota Net Promoter Score (NPS):
- Promoters (5): Provavelmente recomendaria
- Passivos (4-3): Pode recomendar
- Detratores (1-2): Dificilmente recomendaria

NPS = (% Promoters - % Detratores) × 100
```

**Meta: NPS > 50 (excelente)**

#### Métrica 8: Clareza e Acessibilidade
**Definição**: Quão fácil é entender a resposta

**Critérios**:
```
Jargão: Quantas palavras técnicas sem explicação?
  Meta: < 2 termos técnicos não explicados

Estrutura: Resposta tem título, tópicos, conclusão?
  Meta: 90% estruturadas

Comprimento: Resposta é concisa? (não > 500 palavras)
  Meta: 100% das respostas < 250 palavras, exceto explicações

Exemplos: Usa números/exemplos reais do cliente?
  Meta: 85%+
```

**Medição Automatizada**:
```python
def medir_clareza(resposta):
    """
    Avalia clareza geral da resposta
    """
    termos_tecnicos = contar_jargao(resposta)
    tem_estrutura = validar_estrutura(resposta)
    num_palavras = len(resposta.split())
    tem_exemplos = detectar_exemplos(resposta)
    
    clarity_score = (
        (termos_tecnicos <= 2) * 25 +
        (tem_estrutura) * 25 +
        (num_palavras < 250) * 25 +
        (tem_exemplos) * 25
    ) / 100
    
    return clarity_score
```

---

## 3. Avaliação Qualitativa

### 3.1 Teste A/B de Prompts
Compare 2 versões do agente:

```
Versão A: Resposta mais técnica
Versão B: Resposta mais acessível

Envie para 100 clientes, meça:
- Qual teve maior NPS?
- Qual gerou mais follow-up?
- Qual teve maior conversão a investimento?
```

### 3.2 Teste de Edge Cases
Cenários desafiadores:

```
1. Cliente muito endividado
2. Cliente com dúvida fora do escopo (tributária)
3. Cliente pedindo garantia de lucro
4. Cliente desconfiado de segurança
5. Cliente com objetivo impossível

Avalie se agente:
- ✓ Reconheceu limitation
- ✓ Foi honesto
- ✓ Ofereceu alternativa
- ✓ Manteve empatia
```

### 3.3 Teste de Consistency
Faça mesma pergunta 5 vezes:

```
Pergunta: "Devo investir em Fundo ou CDB?"

Check:
- Todas as respostas chegam na mesma recomendação?
- Variação está dentro do esperado?
- Dados numéricos são idênticos?

Meta: 100% consistência em fatos, 95% em estrutura
```

---

## 4. Dashboard de Métricas

### Template de Monitoramento

```
┌─────────────────────────────────────────────────────────────┐
│             DASHBOARD AGENTE FINANCEIRO INTELIGENTE          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 📊 PRECISÃO & ASSERTIVIDADE                                 │
│   ├─ Taxa de Acurácia de Fatos:          95% ✓ META 95%   │
│   ├─ Relevância de Recomendações:        87% ✓ META 85%   │
│   └─ Validação de Elegibilidade:         92% ✓ META 90%   │
│                                                              │
│ 🛡️  SEGURANÇA & CONFIABILIDADE                              │
│   ├─ Taxa de Alucinações:                2%  ✓ META <5%   │
│   ├─ Disclaimers Apropriados:           100% ✓ META 100%  │
│   └─ Conformidade de Dados:              98% ✓ META 98%   │
│                                                              │
│ 🎯 PERSONALIZAÇÃO & RELEVÂNCIA                              │
│   ├─ Nível de Contextualização:          2.6 ✓ META 2.5   │
│   ├─ Cobertura de Intenção:              89% ✓ META 88%   │
│   └─ Menção de Contexto do Cliente:      91% ✓ META 85%   │
│                                                              │
│ 😊 EXPERIÊNCIA & SATISFAÇÃO                                 │
│   ├─ Satisfaction Score (NPS):            62  ✓ META >50   │
│   ├─ Clarity Score:                      0.88 ✓ META >0.85│
│   ├─ Time to Resolution:                 45s  ✓ META <60s │
│   └─ Recomendação (% que recomendaria): 78%  ✓ META >70%  │
│                                                              │
│ 📈 SCORE GERAL DO AGENTE:                8.7/10 ✓ EXCELENTE│
│                                                              │
│ Última Atualização: 2024-03-15 | Amostra: 250 interações   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Processo de Melhoria Contínua

### Ciclo Semanal

```
SEGUNDA: Análise de Métricas
  └─ Quais métricas caíram abaixo da meta?

TERÇA: Root Cause Analysis
  └─ Por que caíram? (prompt? dados? lógica?)

QUARTA: Hipóteses de Melhoria
  └─ Como corrigir? (novo prompt? novo dado?)

QUINTA: Teste A/B
  └─ Versão antiga vs. nova

SEXTA: Deploy de Melhores
  └─ Se nova versão > velha, ativa nova
```

### Exemplo Semanal Real

```
SEGUNDA:
  Métrica "Taxa de Alucinações" está em 8% (meta: <5%)

TERÇA:
  Root Cause: Agente inventa "produto novo" que não existe

QUARTA:
  Hipótese: Adicionar mais exemplos de "não sei" no prompt

QUINTA:
  A/B Test: 50% clientes versão antiga, 50% nova
  Resultado: Nova versão reduz alucinações para 2%

SEXTA:
  Deploy: Versão nova ativa para 100% dos clientes
```

---

## 6. Relatório de Avaliação

**Frequência**: Quinzenal

**Conteúdo**:
1. Resumo Executivo (1 página)
2. Métricas Principais (tabela)
3. Análise de Falhas (top 5 erros)
4. Mudanças Implementadas
5. Próximas Melhorias Propostas

**Exemplo**:
```markdown
## RELATÓRIO QUINZENAL - AGENTE FINANCEIRO INTELIGENTE
Período: 01-15 de Março, 2024

### RESUMO
- Score Geral: 8.7/10 (↑0.3 vs última semana)
- Interações: 1.240
- Taxa Retenção: 72%

### DESTAQUES
✓ Alucinação reduzida de 8% para 2%
✓ Satisfaction score subiu para 62 (NPS)
✗ Cobertura de Intenção caiu 2% (88% → 86%)

### AÇÕES PRÓXIMAS
1. Adicionar 5 exemplos novos de "não sei"
2. Revisar prompt para melhor detecção de intenção
3. A/B teste novo template de resposta
```

---

## Conclusão

O Agente Financeiro Inteligente será avaliado em 4 pilares:

| Pilar | Métrica Principal | Meta |
|-------|------------------|------|
| **Precisão** | Acurácia de Fatos | 95%+ |
| **Segurança** | Taxa de Alucinações | <5% |
| **Personalização** | Contextualização | 2.5+ |
| **Satisfação** | NPS | >50 |

Com essas métricas, garantimos que o agente não apenas funciona bem, mas melhora continuamente.
