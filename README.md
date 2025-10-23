# 📄 Sistema de Perguntas e Respostas com PDF

Sistema inteligente de Question Answering para documentos PDF utilizando OCR (PaddleOCR) para extração de texto e modelos de IA avançados para responder perguntas sobre o conteúdo dos documentos.

## 🎯 Funcionalidades

- **Upload de múltiplos PDFs**: Suporte para upload de vários arquivos PDF simultaneamente (até 1 GB cada)
- **Extração de texto via OCR**: Utiliza PaddleOCR para extrair texto de documentos digitalizados ou imagens
- **Question Answering inteligente**: Responde perguntas sobre o conteúdo dos documentos usando modelos de IA de última geração
- **Visualização por página**: Permite visualizar o texto extraído de cada página individualmente
- **Logs automáticos**: Registra todas as perguntas e respostas em arquivos de log
- **Interface amigável**: Interface web moderna e intuitiva construída com Streamlit

## 🚀 Tecnologias Utilizadas

- **Streamlit**: Framework para criação da interface web
- **PaddleOCR**: Sistema de OCR de alta precisão
- **OpenAI API**: Modelos de linguagem avançados para Question Answering
- **pdf2image**: Conversão de páginas PDF em imagens
- **Python 3.11**: Linguagem de programação

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Chave de API OpenAI configurada como variável de ambiente `OPENAI_API_KEY`
- Poppler (para conversão de PDF em imagens)

### Instalação do Poppler

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Baixe o Poppler do [repositório oficial](https://github.com/oschwartz10612/poppler-windows/releases/)

## 🔧 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a variável de ambiente com sua chave OpenAI:
```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

## 💻 Como Usar

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. Acesse a aplicação no navegador (geralmente em `http://localhost:8501`)

3. **Upload de documentos:**
   - Clique em "Browse files" para selecionar um ou mais arquivos PDF
   - Aguarde o processamento do OCR (pode levar alguns minutos para documentos grandes)

4. **Fazer perguntas:**
   - Selecione o documento processado na lista
   - Digite sua pergunta no campo de texto
   - Clique em "🔍 Buscar Resposta"
   - A resposta será exibida logo abaixo

5. **Visualizar texto extraído:**
   - Expanda o documento na seção "Documentos Processados"
   - Navegue pelas páginas para ver o texto extraído via OCR

## 📁 Estrutura de Arquivos

```
pdf_qa_app/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências do projeto
├── README.md             # Esta documentação
└── .streamlit/           # Configurações do Streamlit (opcional)
```

**Arquivos gerados durante o uso:**

- `/home/ubuntu/ocr_logs/`: Logs de texto extraído por documento
- `/home/ubuntu/todo.md`: Registro de perguntas e respostas

## ⚙️ Configurações Avançadas

### Modelos de IA Disponíveis

A aplicação suporta os seguintes modelos:
- `gpt-4.1-mini` (padrão) - Equilíbrio entre velocidade e qualidade
- `gpt-4.1-nano` - Mais rápido e econômico
- `gemini-2.5-flash` - Alternativa do Google

### Limites de Tamanho

- **Tamanho máximo por arquivo**: 1 GB
- **Aviso para arquivos grandes**: Arquivos acima de 100 MB exibem confirmação antes do processamento
- **Contexto máximo**: 20.000 caracteres (truncado automaticamente se necessário)

## 🔍 Critérios de Sucesso

✅ PDF carregado com sucesso  
✅ Texto extraído corretamente via OCR  
✅ Resposta coerente e localizada no contexto extraído  
✅ Upload funcional com múltiplos arquivos e limite ajustável (até 1 GB)  
✅ Logs salvos automaticamente  
✅ Interface responsiva e intuitiva  

## 🛠️ Solução de Problemas

### Erro ao processar PDF

**Opções disponíveis:**
- **Reprocessar**: Tenta processar o arquivo novamente
- **Ignorar erro**: Pula o arquivo com erro
- **Pular página**: Ignora apenas a página problemática

### Documento muito grande

**Opções disponíveis:**
- **Processar mesmo assim**: Continua o processamento (pode demorar)
- **Pular arquivo**: Não processa o arquivo

### Erro "OCR model not found"

Execute:
```bash
pip install paddleocr paddlepaddle --upgrade
```

### Erro "OpenAI API key not found"

Certifique-se de que a variável de ambiente está configurada:
```bash
echo $OPENAI_API_KEY
```

## 📊 Logs e Rastreamento

Todas as operações são registradas em:

1. **Logs de OCR**: `/home/ubuntu/ocr_logs/{nome_arquivo}.txt`
   - Contém o texto extraído de cada página
   - Organizado por página

2. **Log de Atividades**: `/home/ubuntu/todo.md`
   - Nome dos arquivos processados
   - Número de páginas por documento
   - Perguntas feitas
   - Respostas retornadas
   - Data e hora de cada operação

## 🎨 Personalização

### Alterar idioma do OCR

No arquivo `app.py`, linha 19:
```python
return PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
```

Altere `lang='en'` para:
- `'pt'` - Português
- `'es'` - Espanhol
- `'fr'` - Francês
- etc.

### Alterar modelo padrão de QA

No arquivo `app.py`, na função `answer_question`, altere o parâmetro `model_name`.

## 📝 Licença

Este projeto é fornecido como está, sem garantias.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Suporte

Para problemas ou dúvidas, abra uma issue no repositório do projeto.

---

**Desenvolvido com ❤️ usando Streamlit, PaddleOCR e IA Avançada**

