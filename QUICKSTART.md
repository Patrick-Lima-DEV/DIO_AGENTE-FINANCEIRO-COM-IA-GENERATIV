# 🚀 Guia de Início Rápido

Complete esta configuração em **5 minutos** para rodar Sofia Finance.

---

## ⚡ Instalação Rápida (Windows)

### 1️⃣ Clonar Repositório
```bash
cd C:\Users\<seu-usuario>\Área de Trabalho
git clone https://github.com/seu-usuario/lab-agente-financeiro.git
cd lab-agente-financeiro
```

### 2️⃣ Criar Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variáveis (Opcional)
```bash
copy .env.example .env
# Editar .env com suas API keys (se quiser usar LLM real)
```

### 5️⃣ Rodar Aplicação
```bash
streamlit run src/app.py
```

**Pronto!** A aplicação abrirá em `http://localhost:8501`

---

## ⚡ Instalação Rápida (Mac/Linux)

### 1️⃣ Clonar Repositório
```bash
cd ~/Desktop
git clone https://github.com/seu-usuario/lab-agente-financeiro.git
cd lab-agente-financeiro
```

### 2️⃣ Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variáveis (Opcional)
```bash
cp .env.example .env
# Editar .env com suas API keys
```

### 5️⃣ Rodar Aplicação
```bash
streamlit run src/app.py
```

---

## 🎯 Usando Sofia Finance

### Na Página de Chat

```
1. Clique em "💬 Chat com Sofia" no menu esquerdo
2. Veja a mensagem de boas-vindas
3. Digite sua pergunta:

   Exemplos:
   - "Tenho R$ 5.000, onde invisto?"
   - "Por que estou gastando muito?"
   - "Como economizar para uma meta?"
   - "O que é CDB?"
```

### Analisando Gastos

```
1. Clique em "📊 Análise de Gastos"
2. Veja:
   - Renda total, gastos e taxa de poupança
   - Gráficos de gastos por categoria
   - Tabla detalhada de transações
   - Recomendações automáticas
```

### Simulando Investimentos

```
1. Clique em "🎯 Simulador de Investimentos"
2. Preencha:
   - Valor Inicial: R$ 5.000
   - Taxa Anual: 8.5%
   - Período: 5 anos
3. Clique "▶️ Calcular"
4. Veja resultado e gráfico de crescimento
```

### Obtendo Recomendações

```
1. Clique em "📈 Recomendações Personalizadas"
2. Veja seu perfil resumido
3. Expanda cada produto para:
   - Ver compatibilidade
   - Taxa de rentabilidade
   - Simulação rápida
```

---

## 💡 Próximos Passos

### Ler Documentação
- [Documentação Completa](docs/01-documentacao-agente.md)
- [Base de Conhecimento](docs/02-base-conhecimento.md)
- [Prompts do Sistema](docs/03-prompts.md)

### Customizar para Sua Conta
1. Edite `data/perfil_investidor.json` com seus dados
2. Adicione suas transações em `data/transacoes.csv`
3. Reinicie Streamlit
4. Sofia now personalizada para você!

### Integrar LLM Real
1. Copie `.env.example` para `.env`
2. Adicione sua API key (OpenAI, Gemini ou Claude)
3. Uncomment a integração no código
4. Teste com queries mais complexas

### Fazer Deploy
- [Deploy no Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)
- [Deploy no Railway](https://railway.app/)
- [Deploy no Render](https://render.com/)

---

## ❓ Dúvidas Frequentes

### P: Preciso de API key para usar?
**R:** Não! MVP funciona 100% offline com dados simulados. API keys são opcionais para integrar LLM real.

### P: Posso usar meus dados reais?
**R:** Sim! Edite os CSVs/JSONs em `data/` com seus dados. Sofia vai personalizar para você.

### P: Qual é o custo?
**R:** Completamente grátis (MIT License). Se usar OpenAI, paga apenas pelo uso da API.

### P: Posso modificar o código?
**R:** Sim! Você pode modificar, estender e até comercializar (MIT License permite).

### P: Como contribuir?
**R:** Leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Instale dependências novamente
pip install -r requirements.txt
```

### "Port 8501 já em uso"
```bash
# Use porta diferente
streamlit run src/app.py --logger.level=debug --server.port 8502
```

### "Erro ao carregar dados"
```bash
# Verifique se pasta data/ existe e tem arquivos:
# - transacoes.csv
# - historico_atendimento.csv
# - perfil_investidor.json
# - produtos_financeiros.json
```

### "API Error - Invalid API key"
```bash
# Verifique se .env foi criado corretamente
# Valide API keys em suas contas (OpenAI, Google, etc)
```

---

## 📚 Documentos Importantes

| Documento | Conteúdo |
|-----------|----------|
| [README.md](README.md) | Visão geral do projeto |
| [docs/01-documentacao-agente.md](docs/01-documentacao-agente.md) | Arquitetura do agente |
| [docs/02-base-conhecimento.md](docs/02-base-conhecimento.md) | Como os dados funcionam |
| [docs/03-prompts.md](docs/03-prompts.md) | Como Sofia pensa |
| [docs/04-metricas.md](docs/04-metricas.md) | Como avaliar qualidade |
| [docs/05-pitch.md](docs/05-pitch.md) | Apresentação executiva |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como contribuir |

---

## 🎥 Vídeo Tutorial

*[Link para vídeo de início rápido em breve]*

---

## ✅ Checklist: Pronto para começar?

- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Aplicação rodando (`streamlit run src/app.py`)
- [ ] Consegue acessar http://localhost:8501
- [ ] Consegue fazer chat básico
- [ ] Leu ao menos a documentação do README

**Parabéns!** Você está pronto para usar Sofia Finance! 🚀

---

## 📞 Precisa de Ajuda?

- 📖 Leia a documentação completa em `docs/`
- 🐛 Abra uma issue: [GitHub Issues](https://github.com/seu-usuario/lab-agente-financeiro/issues)
- 💬 Pergunte: [GitHub Discussions](https://github.com/seu-usuario/lab-agente-financeiro/discussions)
- 📧 Email: seu-email@exemplo.com

---

**Boa sorte com Sofia Finance!** 💰✨

*Última atualização: Fevereiro de 2024*
