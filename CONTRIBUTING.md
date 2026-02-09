-dev
Meus aplicativos
Meu perfil
Explorar
Discutir
Criar aplicativo
Aplicativos de patrick-lima-dev
dio_agente-financeiro-com-ia-generativ ∙ main ∙ src/app.py

# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para Sofia Finance! Este documento fornece diretrizes e instruções para ajudar na contribuição.

## 📋 Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Denuncie comportamentos inadequados

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
git clone https://github.com/seu-usuario/lab-agente-financeiro.git
cd lab-agente-financeiro
```

### 2. Crie uma Branch
```bash
git checkout -b feature/sua-feature
# ou
git checkout -b bugfix/seu-bug
# ou
git checkout -b docs/sua-melhoria-docs
```

### 3. Faça suas Mudanças

Siga estas práticas:
- Escreva código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Atualize documentação conforme necessário
- Mantenha consistency de estilo

### 4. Commit das Mudanças
```bash
git commit -m "tipo(escopo): descrição

descrição detalhada aqui (opcional)

Closes #123"
```

**Tipos de commit**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças em documentação
- `style`: Formatação, sem mudança de lógica
- `refactor`: Refatoração de código
- `test`: Adição/atualização de testes
- `chore`: Tarefas auxiliares

### 5. Push para sua Fork
```bash
git push origin feature/sua-feature
```

### 6. Abra um Pull Request
- Descreva claramente as mudanças
- Referencie issues relacionadas
- Explique por que essas mudanças são necessárias
- Inclua screenshots/GIFs se aplicável

---

## 🏗️ Estrutura de Contribução

### Adicionando Nova Funcionalidade

1. **Abra uma issue** descrevendo a funcionalidade
2. **Aguarde feedback** dos mantenedores
3. **Implemente** seguindo o padrão do projeto
4. **Teste** localmente
5. **Submeta PR** com testes e documentação

### Corrigindo um Bug

1. **Abra uma issue** descrevendo o bug
2. **Inclua steps para reproduzir**
3. **Corrija** o bug
4. **Adicione teste** que falha sem a correção
5. **Submeta PR** com explicação

### Melhorando Documentação

1. **Edite diretamente** no GitHub ou localmente
2. **Mantenha consistência** com documentação existente
3. **Valide links** e formatação
4. **Submeta PR** para revisão

---

## ✅ Checklist pre-PR

- [ ] Fork foi atualizado com latest changes
- [ ] Branch foi criada a partir de `main`
- [ ] Código segue style guide do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Commit messages são descritivas
- [ ] Não há conflitos com `main`
- [ ] PR descreve claramente as mudanças

---

## 🧪 Rodando Testes Localmente

```bash
# Instalar dependências de teste
pip install -r requirements-dev.txt

# Rodar testes
pytest

# Com cobertura
pytest --cov=src

# Modo watch (rerun em mudanças)
ptw
```

---

## 📚 Estrutura do Projeto

```
lab-agente-financeiro/
├── src/
│   └── app.py              # Código principal
├── data/
│   └── *.csv, *.json       # Dados do agente
├── docs/
│   └── *.md                # Documentação
├── tests/                  # (A adicionar)
│   └── test_*.py
├── requirements.txt        # Dependências
└── README.md
```

---

## 🐛 Reportando Bugs

### Abra uma Issue com:
1. **Título descritivo** do bug
2. **Passos para reproduzir**
3. **Comportamento esperado** vs **observado**
4. **Screenshots/logs** se aplicável
5. **Informações do sistema** (OS, Python version, etc.)

### Exemplo:
```
Título: Chat não responde com nome do cliente

Passos:
1. Abrir app
2. Digitar mensagem sem contexto de cliente
3. Sofia não menciona o nome

Esperado:
Sofia menciona o nome do cliente na resposta

Observado:
Sofia responde de forma genérica

Ambiente:
- SO: Windows 11
- Python: 3.10
- Streamlit: 1.28
```

---

## 💡 Sugestões de Funcionalidades

### Áreas com Oportunidades

1. **Base de Conhecimento**
   - Adicionar novos produtos
   - Expandir FAQs
   - Melhorar exemplos

2. **Cálculos Financeiros**
   - Análises mais avançadas
   - Simulações com inflação
   - Projeções de longo prazo

3. **UI/UX**
   - Novos gráficos e visualizações
   - Melhor organização de dados
   - Temas customizáveis

4. **Integração LLM**
   - Suportar mais providers de LLM
   - Melhorar prompt engineering
   - Fine-tuning para domínio financeiro

5. **Persistência**
   - Banco de dados real
   - Autenticação de usuário
   - Histórico entre sessões

---

## 🎓 Convenções de Código

### Python Style
```python
# Use PEP 8
# - 4 espaços de indentação
# - Max 100 caracteres de linha
# - Docstrings em todas funções públicas

def calcular_retorno(valor_inicial, taxa_anual, anos):
    """
    Calcula retorno de investimento.
    
    Args:
        valor_inicial (float): Valor investido
        taxa_anual (float): Taxa anual (%)
        anos (int): Período em anos
    
    Returns:
        dict: {'valor_futuro': float, 'ganho': float}
    """
    valor_futuro = valor_inicial * ((1 + taxa_anual/100) ** anos)
    ganho = valor_futuro - valor_inicial
    
    return {
        "valor_futuro": round(valor_futuro, 2),
        "ganho": round(ganho, 2)
    }
```

### Docstrings
```python
def funcao_exemplo(parametro1, parametro2):
    """
    Uma linha descrevendo o que faz.
    
    Descrição mais longa se necessário, explicando
    o comportamento, casos especiais, etc.
    
    Args:
        parametro1: Descrição
        parametro2: Descrição
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Se algo der errado
    
    Examples:
        >>> resultado = funcao_exemplo("teste", 123)
        >>> resultado
        "resultado esperado"
    """
```

---

## 🔍 Processo de Revisão

1. **Verificação Automática** (linting, testes)
2. **Revisão de Código** (mantenedores)
3. **Feedback e Mudanças** (colaborador)
4. **Aprovação e Merge** (mantenedor)

---

## 📞 Dúvidas?

- Abra uma **GitHub Discussion**
- Crie uma **GitHub Issue**
- Entre em contato: [seu-email@exemplo.com]

---

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.

---

**Obrigado por contribuir para Sofia Finance!** 💰✨

