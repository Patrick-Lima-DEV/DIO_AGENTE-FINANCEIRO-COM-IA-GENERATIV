# 01 - Documentação do Agente Financeiro Inteligente

## 1. Propósito e Visão

O **Agente Financeiro Inteligente (AFI)** é um assistente virtual orientado por IA Generativa que personaliza recomendações financeiras, antecipando necessidades dos clientes e oferecendo consultoria proativa em produtos e serviços.

### Objetivo Principal
Transformar o relacionamento financeiro dos clientes através de:
- Respostas contextualizadas baseadas em histórico e perfil
- Recomendações personalizadas de produtos
- Educação financeira clara e acessível
- Antecipação de necessidades financeiras
- Segurança e confiabilidade nas informações

---

## 2. Caso de Uso

### Problema Identificado
Clientes enfrentam dificuldades em:
- Tomar decisões financeiras sem orientação adequada
- Encontrar produtos alinhados com seu perfil de risco
- Entender taxas, prazos e características de investimentos
- Planejar objetivos financeiros de longo prazo
- Acessar consultoria 24/7 de forma conveniente

### Solução Proposta
O AFI oferece:
- **Consultoria Contínua**: Disponível 24/7 para tirar dúvidas
- **Recomendações Personalizadas**: Baseadas em perfil, patrimônio e objetivos
- **Educação Financeira**: Explica conceitos de forma clara e simples
- **Análise de Gastos**: Identifica padrões e oportunidades de economia
- **Planejamento Financeiro**: Auxilia na definição de metas e estratégias

### Público-Alvo
- **Investidores Iniciantes**: Que desejam aprender sobre investimentos
- **Classe Média**: Com renda entre R$ 3.000 e R$ 10.000
- **Pessoas Ocupadas**: Que preferem orientação digital rápida
- **Clientes Digitais**: Nativos de mobile e web

---

## 3. Persona e Tom de Voz

### Identidade do Agente
**Nome**: Sofia Finance  
**Especialidade**: Consultora Financeira  
**Experiência**: 15+ anos em consultoria de investimentos  
**Traços**: Empática, educadora, confiável, proativa

### Tom de Voz
- **Acessível**: Linguagem simples, evitar jargão técnico
- **Educadora**: Explica conceitos sem parecer condescendente
- **Empática**: Entende limitações financeiras do cliente
- **Proativa**: Antecipa dúvidas e oferece soluções
- **Honesta**: Reconhece limites e riscos
- **Profissional**: Mantém credibilidade e segurança

### Exemplos de Comunicação

**Situação**: Cliente pergunta sobre risco de investimento  
**Resposta Sofia**:
> "Entendo sua preocupação! Risco é uma parte natural dos investimentos, mas há maneiras de gerenciá-lo. Fundos Conservadores têm menor volatilidade, enquanto Ações podem gerar maiores retornos em longo prazo. Vamos explorar seu perfil?"

**Situação**: Cliente quer economizar R$ 10.000 em 1 ano  
**Resposta Sofia**:
> "Ótima meta! Vejo que você gasta cerca de R$ 350/mês em alimentação. Com pequenos ajustes, poderiam poupar R$ 850/mês em despesas discretas. Combinado com um investimento conservador, seu objetivo é totalmente alcançável!"

---

## 4. Arquitetura do Sistema

### Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                      INTERAÇÃO DO USUÁRIO                        │
│                   (Pergunta via Chatbot)                        │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE ENTRADA                             │
│              - Processamento de Linguagem Natural                │
│              - Análise de Intenção                               │
│              - Extração de Entidades                             │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CAMADA DE CONTEXTO                              │
│         - Perfil do Cliente (perfil_investidor.json)             │
│         - Histórico de Transações (transacoes.csv)               │
│         - Atendimentos Anteriores (historico_atendimento.csv)    │
│         - Memória de Conversa (contexto persistente)             │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CAMADA DE RACIOCÍNIO                           │
│              - LLM com Prompt Estruturado                        │
│              - Chain of Thought (CoT)                            │
│              - Validação de Respostas                            │
│              - Detecção de Alucinações                           │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                 CAMADA DE CONHECIMENTO                           │
│         - Base de Produtos (produtos_financeiros.json)           │
│         - Regras Financeiras                                     │
│         - Taxas e Condições de Mercado                           │
│         - FAQs Estruturadas                                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CAMADA DE RESPOSTA                             │
│              - Formatação da Resposta                            │
│              - Inclusão de Cálculos Demonstrativos               │
│              - Recomendações Personalizadas                      │
│              - Próximos Passos                                   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SAÍDA FORMATADA AO USUÁRIO                      │
│          (Resposta Clara, Acionável e Segura)                    │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes Principais

#### 1. **Entrada de Dados**
- Chatbot Streamlit para interface conversacional
- Processamento de linguagem natural (NLP)
- Identificação de intenções (investir, economizar, aprender, etc.)

#### 2. **Contexto e Memória**
- Carregamento de perfil do cliente
- Análise de transações históricas
- Memória de conversa (últimas 5 trocas)
- Continuidade contextual entre sessões

#### 3. **Raciocínio (LLM)**
- Integração com API (ChatGPT, Gemini, Claude)
- Prompt estruturado com guardrails
- Chain of Thought para decisões complexas
- Validação de respostas contra base de conhecimento

#### 4. **Base de Conhecimento**
- Produtos financeiros (JSON)
- Transações históricas (CSV)
- Perfil de investidor (JSON)
- FAQs estruturadas (Markdown/JSON)
- Regras de segurança e compliance

#### 5. **Geração de Resposta**
- Formatação em markdown
- Cálculos simulados (retorno esperado, economia, etc.)
- Recomendações personalizadas
- Chamada para ação (CTA)

---

## 5. Segurança e Mitigação de Alucinações

### Estratégias de Prevenção

#### 5.1 Prompt Engineering
- **Especificidade**: Prompts detalhados com exemplos
- **Constraintos Explícitos**: "Apenas responda com base nos dados fornecidos"
- **Verificação de Fatos**: "Se não tiver informação, diga 'Não sei'"

#### 5.2 Grounding em Dados
- **Verifiable Facts Only**: Todas as recomendações baseadas em dados JSON/CSV
- **Fonte Explícita**: Indicar de onde vem cada informação
- **Validação Cruzada**: Comparar resposta com base de conhecimento

#### 5.3 Detecção de Edge Cases
- Perguntas fora do escopo → Redirecionamento educado
- Pedidos de aconselhamento legal/tributário → Disclaimer + referência a profissional
- Dados inconsistentes → Pedido de clarificação

#### 5.4 Rate Limiting e Monitoramento
- Máximo 5 requisições por minuto
- Logging de todas as interações
- Revisão manual de respostas "críticas" (maiores valores)

#### 5.5 Exemplos Safeguards

| Cenário | Prevenção |
|---------|-----------|
| "Qual é a taxa de júros da Caixa?" | "Não tenho acesso a taxas em tempo real. Consulte o site oficial." |
| "Você garante lucro?" | "Não. Todo investimento tem risco. Lucros passados não garantem futuros." |
| "Qual é o melhor investimento?" | "Depende de seus objetivos, risco e horizonte. Vamos explorar juntos?" |
| Pedido de transfer de fundos | "Não posso realizar transferências. Isso deve ser feito diretamente no app bancário." |

### Métricas de Confiabilidade

- **Acurácia de Fatos**: % de informações verificáveis contra base de dados
- **Taxa de Uncertainty**: % de respostas com "não sei" ou disclaimers
- **Detecção de Alucinações**: Monitoramento manual em amostra de respostas
- **Satisfaction Scores**: Feedback do usuário sobre confiabilidade

---

## 6. Fluxo de Conversação Esperado

### Exemplo 1: Novo Cliente com Interesse em Investimentos

```
Cliente: "Sou novo em investimentos. Por onde começo?"

Sofia: "Bem-vindo! Ótimo que quer aprender! 
Antes de recomendar algo, gostaria de saber:
1. Qual é seu principal objetivo? (aposentadoria, casa, viagem?)
2. Qual seu perfil de risco? (prefere segurança ou está aberto a volatilidade?)
3. Qual montante você gostaria de investir inicialmente?"

Cliente: "Quero aposentadoria em 20 anos, sou moderado no risco, tenho R$ 5.000 para começar"

Sofia: "Perfeito! Com seu horizonte de 20 anos, recomendo:

**1. Fundo Conservador ABC** (baixo risco)
- Rentabilidade: 8.5% ao ano
- Mínimo: R$ 100 | Taxa: 0.5% ao ano
- Ideal para base segura do seu portfólio

**2. CDB Seguro 120% CDI**
- Rentabilidade: 10.5% ao ano
- Sem carência | Muito seguro
- Excelente para começar

Com R$ 5.000, sugiro: R$ 3.000 em Fundo + R$ 2.000 em CDB = retorno estimado de R$ 530 no ano 1.

Quer saber mais sobre algum?"
```

### Exemplo 2: Cliente Analisando Gastos

```
Cliente: "Por que sempre fico sem dinheiro mesmo ganhando R$ 5.000?"

Sofia: "Vamos analisar seus gastos no último mês:

**Alimentação**: R$ 350 (7% - dentro do esperado)
**Transporte**: R$ 200 (4% - bom!)
**Lazer**: R$ 1.200 (24% - oportunidade de otimização!)
**Compras Online**: R$ 450 (9% - outro ponto de atenção)

Você está gastando 33% do salário em Lazer + Compras. Reduzindo para 20%, teríamos:
- **Economia potencial**: R$ 650/mês
- **Em 12 meses**: R$ 7.800 poupados
- **Investidos em CDB**: Renderia +/- R$ 820 de juros

Quer ajuda para criar um plano de economia?"
```

---

## 7. Integração com Sistemas Externos

### APIs Sugeridas
1. **OpenAI GPT-4** ou **Google Gemini**: LLM principal
2. **Banco de Dados**: PostgreSQL para persistência de conversas
3. **Analytics**: Mixpanel ou Google Analytics para métricas

### Dados de Entrada (Já Mapeados)
- ✅ Transações (CSV)
- ✅ Perfil Investidor (JSON)
- ✅ Produtos Financeiros (JSON)
- ✅ Histórico de Atendimento (CSV)

---

## 8. Roadmap Futuro

| Fase | Funcionalidade | Período |
|------|----------------|---------|
| **MVP** | Chatbot básico + recomendações simples | Semana 1-2 |
| **V1** | Análise de gastos + simulações | Semana 3-4 |
| **V2** | Previsões de mercado + alertas | Mês 2 |
| **V3** | Integração com APIs bancárias reais | Mês 3+ |

---

## Conclusão

O Agente Financeiro Inteligente representa a evolução de chatbots passivos para assistentes proativos, personalizados e seguros. Através de IA generativa bem orientada, oferece recomendações confiáveis que transformam a forma como clientes relacionam-se com suas finanças.
