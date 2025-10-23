# 🚀 Guia de Deployment

Este documento fornece instruções detalhadas para fazer o deploy da aplicação PDF Question Answering.

## 📦 Repositório GitHub

O código está disponível em:
**https://github.com/Lolavice9019/pdf-qa-ocr**

## 🌐 Opções de Deployment

### Opção 1: Streamlit Cloud (Recomendado)

Streamlit Cloud oferece hosting gratuito para aplicações Streamlit.

#### Passos:

1. **Acesse Streamlit Cloud**
   - Visite: https://share.streamlit.io/
   - Faça login com sua conta GitHub

2. **Criar novo app**
   - Clique em "New app"
   - Selecione o repositório: `Lolavice9019/pdf-qa-ocr`
   - Branch: `master`
   - Main file path: `app.py`

3. **Configurar Secrets**
   - Antes de fazer deploy, clique em "Advanced settings"
   - Na seção "Secrets", adicione:
   ```toml
   OPENAI_API_KEY = "sua-chave-openai-aqui"
   ```

4. **Deploy**
   - Clique em "Deploy!"
   - Aguarde alguns minutos para o build completar
   - Sua aplicação estará disponível em uma URL pública permanente

#### Vantagens:
- ✅ Gratuito
- ✅ SSL/HTTPS automático
- ✅ Deploy contínuo (atualiza automaticamente com commits)
- ✅ Fácil gerenciamento de secrets
- ✅ URL permanente

### Opção 2: Deployment Local

Para rodar localmente em sua máquina:

1. **Clone o repositório:**
```bash
git clone https://github.com/Lolavice9019/pdf-qa-ocr.git
cd pdf-qa-ocr
```

2. **Instale dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure variável de ambiente:**
```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

4. **Execute a aplicação:**
```bash
streamlit run app.py
```

5. **Acesse no navegador:**
```
http://localhost:8501
```

### Opção 3: Docker (Avançado)

Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor porta
EXPOSE 8501

# Comando de inicialização
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"]
```

**Build e run:**
```bash
docker build -t pdf-qa-app .
docker run -p 8501:8501 -e OPENAI_API_KEY="sua-chave" pdf-qa-app
```

### Opção 4: Heroku

1. **Criar arquivo `setup.sh`:**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **Criar `Procfile`:**
```
web: sh setup.sh && streamlit run app.py
```

3. **Adicionar `Aptfile`:**
```
poppler-utils
```

4. **Deploy:**
```bash
heroku create pdf-qa-app
heroku config:set OPENAI_API_KEY="sua-chave"
git push heroku master
```

## 🔑 Configuração de API Keys

### OpenAI API Key

A aplicação requer uma chave de API da OpenAI. Você pode obter uma em:
https://platform.openai.com/api-keys

**Importante:**
- Mantenha sua chave em segredo
- Nunca faça commit da chave no repositório
- Use variáveis de ambiente ou secrets do Streamlit Cloud

### Configuração no Streamlit Cloud

1. Vá para o dashboard do seu app
2. Clique em "Settings" → "Secrets"
3. Adicione:
```toml
OPENAI_API_KEY = "sk-proj-..."
```

### Configuração Local

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-proj-...
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-proj-..."
```

## 📊 Monitoramento e Logs

### Streamlit Cloud

- Logs disponíveis no dashboard do app
- Clique em "Manage app" → "Logs"

### Local

- Logs aparecem no terminal onde você executou `streamlit run`
- Logs de OCR salvos em `/home/ubuntu/ocr_logs/`
- Histórico de perguntas em `/home/ubuntu/todo.md`

## 🔧 Troubleshooting

### Erro: "poppler not found"

**Solução:**
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# Mac
brew install poppler
```

### Erro: "OpenAI API key not configured"

**Solução:**
- Verifique se a variável de ambiente está configurada
- No Streamlit Cloud, verifique os Secrets
- Certifique-se de que a chave é válida

### Erro: "Memory limit exceeded"

**Solução:**
- Reduza o tamanho dos PDFs
- Processe menos páginas por vez
- Use um plano pago do Streamlit Cloud com mais recursos

### App muito lento

**Soluções:**
- Use PDFs menores
- Reduza a resolução das imagens no OCR
- Use modelo `gpt-4.1-nano` em vez de `gpt-4.1-mini`

## 📈 Escalabilidade

Para uso em produção com alto volume:

1. **Use cache agressivo:**
   - Os modelos já são cached com `@st.cache_resource`
   - Considere adicionar cache para resultados de OCR

2. **Otimize OCR:**
   - Reduza resolução de imagens
   - Processe páginas em paralelo

3. **Limite de uploads:**
   - Configure `server.maxUploadSize` no config.toml
   - Implemente filas para processamento assíncrono

4. **Banco de dados:**
   - Armazene resultados de OCR em banco de dados
   - Evite reprocessamento de documentos já analisados

## 🔒 Segurança

- ✅ Nunca exponha API keys no código
- ✅ Use HTTPS em produção
- ✅ Implemente autenticação se necessário
- ✅ Valide uploads de arquivos
- ✅ Limite tamanho de uploads
- ✅ Sanitize user inputs

## 📞 Suporte

Para problemas de deployment:
- Abra uma issue no GitHub
- Consulte a documentação do Streamlit: https://docs.streamlit.io/
- Verifique os logs para mensagens de erro específicas

---

**Última atualização:** 23 de outubro de 2025

