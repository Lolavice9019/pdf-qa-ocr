import streamlit as st
import tempfile
import os
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
from openai import OpenAI
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="PDF Question Answering com OCR",
    page_icon="📄",
    layout="wide"
)

# Inicializar modelos (com cache para evitar recarregamento)
@st.cache_resource
def load_ocr_model():
    """Carrega o modelo PaddleOCR"""
    return PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

@st.cache_resource
def load_qa_client():
    """Inicializa o cliente OpenAI para Question Answering"""
    try:
        client = OpenAI()
        return client
    except Exception as e:
        st.error(f"Erro ao inicializar cliente de QA: {e}")
        return None

def extract_text_from_pdf(pdf_file, ocr_model):
    """
    Extrai texto de um arquivo PDF usando OCR
    
    Args:
        pdf_file: Arquivo PDF carregado
        ocr_model: Modelo PaddleOCR inicializado
    
    Returns:
        tuple: (texto completo, lista de textos por página, lista de imagens)
    """
    try:
        # Converter PDF em imagens
        pdf_bytes = pdf_file.read()
        images = convert_from_bytes(pdf_bytes)
        
        all_text = []
        page_texts = []
        
        # Processar cada página
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, image in enumerate(images):
            status_text.text(f"Processando página {idx + 1} de {len(images)}...")
            
            # Salvar imagem temporária
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                image.save(tmp_file.name)
                
                # Aplicar OCR
                result = ocr_model.ocr(tmp_file.name, cls=True)
                
                # Extrair texto
                page_text = []
                if result and result[0]:
                    for line in result[0]:
                        if line[1]:
                            page_text.append(line[1][0])
                
                page_text_str = '\n'.join(page_text)
                page_texts.append(page_text_str)
                all_text.append(page_text_str)
                
                # Limpar arquivo temporário
                os.unlink(tmp_file.name)
            
            # Atualizar barra de progresso
            progress_bar.progress((idx + 1) / len(images))
        
        progress_bar.empty()
        status_text.empty()
        return '\n\n'.join(all_text), page_texts, images
    
    except Exception as e:
        st.error(f"Erro ao processar PDF: {e}")
        
        # Oferecer opções de recuperação
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Reprocessar", key=f"retry_{pdf_file.name}"):
                return extract_text_from_pdf(pdf_file, ocr_model)
        with col2:
            if st.button("⏭️ Ignorar erro", key=f"ignore_{pdf_file.name}"):
                return None, None, None
        with col3:
            if st.button("🚫 Pular página", key=f"skip_{pdf_file.name}"):
                return None, None, None
        
        return None, None, None

def answer_question(question, context, client, model_name="gpt-4.1-mini"):
    """
    Responde uma pergunta baseada no contexto usando modelo de linguagem
    
    Args:
        question: Pergunta do usuário
        context: Contexto extraído do PDF
        client: Cliente OpenAI
        model_name: Nome do modelo a usar
    
    Returns:
        str: Resposta encontrada
    """
    try:
        # Limitar contexto se muito grande (max ~6000 tokens para deixar espaço para resposta)
        max_context_chars = 20000
        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "\n\n[... contexto truncado devido ao tamanho ...]"
        
        # Criar prompt para QA
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente especializado em responder perguntas baseadas em documentos. Analise o contexto fornecido e responda a pergunta de forma precisa e concisa. Se a resposta não estiver no contexto, diga claramente que não foi possível encontrar a informação."
            },
            {
                "role": "user",
                "content": f"""Contexto do documento:
{context}

Pergunta: {question}

Por favor, responda à pergunta baseando-se apenas no contexto fornecido acima."""
            }
        ]
        
        # Fazer chamada à API
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        return answer
    
    except Exception as e:
        return f"Erro ao processar pergunta: {e}"

def save_ocr_log(filename, page_texts):
    """Salva o log de OCR em arquivo"""
    log_path = f"/home/ubuntu/ocr_logs/{filename}.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        for idx, text in enumerate(page_texts):
            f.write(f"=== Página {idx + 1} ===\n")
            f.write(text)
            f.write("\n\n")
    return log_path

def update_todo(filename, num_pages, question, answer):
    """Atualiza o arquivo todo.md com informações da consulta"""
    todo_path = "/home/ubuntu/todo.md"
    with open(todo_path, 'a', encoding='utf-8') as f:
        f.write(f"\n## {filename}\n")
        f.write(f"- **Páginas:** {num_pages}\n")
        f.write(f"- **Pergunta:** {question}\n")
        f.write(f"- **Resposta:** {answer}\n")
        f.write(f"- **Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

# Interface principal
st.title("📄 Sistema de Perguntas e Respostas com PDF")
st.markdown("""
Esta aplicação permite que você faça upload de documentos PDF, extraia o texto usando OCR (PaddleOCR) 
e faça perguntas sobre o conteúdo usando inteligência artificial avançada para Question Answering.

**Recursos:**
- ✅ Upload de múltiplos arquivos PDF (até 1 GB cada)
- ✅ Extração de texto via OCR com PaddleOCR
- ✅ Sistema de perguntas e respostas inteligente
- ✅ Visualização do texto extraído por página
- ✅ Logs automáticos de processamento
""")

# Carregar modelos
with st.spinner("Carregando modelos de OCR e QA..."):
    ocr_model = load_ocr_model()
    qa_client = load_qa_client()

if not qa_client:
    st.error("⚠️ Sistema de QA não disponível. Verifique as configurações.")
    st.stop()

# Upload de arquivos
st.header("1. Upload de Documentos PDF")
uploaded_files = st.file_uploader(
    "Selecione um ou mais arquivos PDF (até 1 GB cada)",
    type=['pdf'],
    accept_multiple_files=True
)

# Armazenar dados na sessão
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = {}

# Processar arquivos
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        # Verificar tamanho
        if file_size_mb > 1024:
            st.error(f"❌ Arquivo '{uploaded_file.name}' excede o limite de 1 GB ({file_size_mb:.2f} MB)")
            continue
        
        # Verificar se já foi processado
        if uploaded_file.name in st.session_state.processed_files:
            st.info(f"✅ Arquivo '{uploaded_file.name}' já foi processado anteriormente")
            continue
        
        # Avisar se arquivo é grande
        if file_size_mb > 100:
            st.warning(f"⚠️ Arquivo '{uploaded_file.name}' é grande ({file_size_mb:.2f} MB). O processamento pode demorar.")
            
            col1, col2 = st.columns(2)
            process_file = False
            
            with col1:
                if st.button(f"✅ Processar mesmo assim", key=f"process_{uploaded_file.name}"):
                    process_file = True
            with col2:
                if st.button(f"⏭️ Pular arquivo", key=f"skip_{uploaded_file.name}"):
                    st.info(f"Arquivo '{uploaded_file.name}' foi pulado.")
                    continue
        else:
            process_file = True
        
        if process_file:
            with st.spinner(f"Processando '{uploaded_file.name}' com OCR..."):
                # Reset file pointer
                uploaded_file.seek(0)
                full_text, page_texts, images = extract_text_from_pdf(uploaded_file, ocr_model)
                
                if full_text and page_texts:
                    # Salvar log
                    log_path = save_ocr_log(uploaded_file.name, page_texts)
                    
                    # Armazenar na sessão
                    st.session_state.processed_files[uploaded_file.name] = {
                        'full_text': full_text,
                        'page_texts': page_texts,
                        'num_pages': len(page_texts),
                        'log_path': log_path
                    }
                    
                    st.success(f"✅ '{uploaded_file.name}' processado com sucesso! ({len(page_texts)} páginas)")
                    st.balloons()
                else:
                    st.error(f"❌ Falha ao processar '{uploaded_file.name}'. Tente novamente ou use outro arquivo.")

# Exibir documentos processados
if st.session_state.processed_files:
    st.header("2. Documentos Processados")
    
    for filename, data in st.session_state.processed_files.items():
        with st.expander(f"📄 {filename} ({data['num_pages']} páginas)"):
            st.markdown(f"**Log de OCR salvo em:** `{data['log_path']}`")
            st.markdown(f"**Total de caracteres extraídos:** {len(data['full_text'])}")
            
            # Mostrar texto por página
            st.subheader("Visualização do OCR por Página")
            for idx, page_text in enumerate(data['page_texts']):
                with st.expander(f"Página {idx + 1}"):
                    st.text_area(
                        f"Texto extraído - Página {idx + 1}",
                        page_text,
                        height=200,
                        key=f"{filename}_page_{idx}",
                        disabled=True
                    )
    
    # Sistema de perguntas e respostas
    st.header("3. Fazer Perguntas")
    
    # Selecionar documento
    selected_file = st.selectbox(
        "Selecione o documento para fazer perguntas:",
        list(st.session_state.processed_files.keys())
    )
    
    if selected_file:
        context = st.session_state.processed_files[selected_file]['full_text']
        
        st.info(f"📊 Documento selecionado: **{selected_file}** ({st.session_state.processed_files[selected_file]['num_pages']} páginas)")
        
        # Campo de pergunta
        question = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual é o tema principal do documento?")
        
        # Opções avançadas
        with st.expander("⚙️ Opções Avançadas"):
            model_choice = st.selectbox(
                "Modelo de IA:",
                ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"],
                index=0
            )
        
        if st.button("🔍 Buscar Resposta", type="primary") and question:
            with st.spinner("Processando pergunta com IA..."):
                answer = answer_question(question, context, qa_client, model_choice)
                
                # Exibir resposta
                st.markdown("### 💡 Resposta:")
                st.success(answer)
                
                # Atualizar todo.md
                update_todo(
                    selected_file,
                    st.session_state.processed_files[selected_file]['num_pages'],
                    question,
                    answer
                )
                
                st.info("✅ Pergunta e resposta registradas em `/home/ubuntu/todo.md`")

else:
    st.info("👆 Faça upload de arquivos PDF para começar")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Desenvolvido com Streamlit, PaddleOCR e IA Avançada</strong></p>
    <p><em>Sistema de Question Answering para Documentos PDF</em></p>
</div>
""", unsafe_allow_html=True)

