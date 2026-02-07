# 🚀 Guia de Deployment - MetaFinance

## Deploy no Streamlit Cloud

### Pré-requisitos
- Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- Repositório GitHub com o código
- API Key do Google Gemini

---

## 📝 Passo a Passo

### 1️⃣ Sincronizar com GitHub
```bash
git add .
git commit -m "Deploy para Streamlit Cloud"
git push origin main
```

### 2️⃣ Deploy na Streamlit Cloud
1. Acesse https://share.streamlit.io
2. Clique em "New app"
3. Selecione seu repositório GitHub
4. Configure:
   - **Repository**: `Patrick-Lima-DEV/DIO_AGENTE-FINANCEIRO-COM-IA-GENERATIV`
   - **Branch**: `main`
   - **Main file path**: `src/app.py`

### 3️⃣ Configurar Secrets (IMPORTANTE ⚠️)

Após o deploy inicial, **configure a API Key**:

1. Vá para o painel da aplicação
2. Clique em "Settings" (engrenagem) → "Secrets"
3. Adicione:
```toml
GOOGLE_API_KEY = "sua_chave_aqui"
```

💡 **NUNCA envie .env para o GitHub!** Streamlit Secrets é a forma segura de passar variáveis sensíveis.

---

## 🔐 Variáveis de Ambiente

| Variável | Local (dev) | Cloud (prod) |
|----------|-----------|------------|
| `GOOGLE_API_KEY` | `.env` | Streamlit Secrets |

---

## ✅ Verificar Se Está Funcionando

Após configurar Secrets, a aplicação deve mostrar:
```
🟢 IA Gemini ativa
```

Se ainda mostrar:
```
🟡 IA offline — respostas padrão
```

Faça isso:
1. Verifique se a API Key foi adicionada corretamente em Secrets
2. Reinicie a aplicação (Settings → Reboot app)
3. Aguarde 2-3 minutos para a aplicação recarregar

---

## 🐛 Troubleshooting

### Problema: "IA offline" mesmo após configurar Secrets
**Solução:**
- Verifique se a API Key está **exatamente correta**
- Teste localmente: `python test_api.py`
- Reinicie a aplicação no Streamlit Cloud
- Aguarde de 5-10 minutos para propagação

### Problema: Erro de CORS ou conexão
**Solução:**
- Verifique conexão de internet
- Confirme que API Key tem acesso ao modelo `gemini-2.5-flash`
- Teste em https://aistudio.google.com com a mesma chave

### Problema: Quer voltar para desenvolvimento local
**Solução:**
```bash
# Criar .env local
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env

# Rodar localmente
python -m streamlit run src/app.py
```

---

## 📊 Monitoramento

Acesse o dashboard da aplicação para:
- Ver uso de recursos
- Verificar logs
- Monitor de tráfego
- Performance

URL: `https://synapsedevfinanceiro.streamlit.app/`

---

## 💡 Dicas

✨ **Recomendações:**
1. Teste localmente com `.env` antes de fazer push
2. Atualize a API Key a cada 6 meses (rotação de segurança)
3. Monitore custos de API no Google Cloud Console
4. Use Streamlit Secrets, nunca commit `.env`

🔄 **Atualizações:**
- Qualquer push para `main` recarrega a app automaticamente
- Mudanças aparecem em 1-5 minutos
- Logs disponíveis em Settings → Manage app → View logs

---

**Precisando de ajuda?** Verifique os logs:
1. Settings → Manage app → View logs
2. Procure por mensagens de erro
3. Teste localmente: `python test_api.py`
