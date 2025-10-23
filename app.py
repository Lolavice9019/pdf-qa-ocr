import streamlit as st
import tempfile
import os
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
from openai import OpenAI
from datetime import datetime
import PyPDF2
import pdfplumber
import pikepdf
import io
import traceback

# Page configuration
st.set_page_config(
    page_title="PDF Question Answering with OCR",
    page_icon="📄",
    layout="wide"
)

# Initialize models (with cache to avoid reloading)
@st.cache_resource
def load_ocr_model():
    """Load PaddleOCR model"""
    return PaddleOCR(use_angle_cls=True, lang='en')

@st.cache_resource
def load_qa_client():
    """Initialize OpenAI client for Question Answering"""
    try:
        client = OpenAI()
        return client
    except Exception as e:
        st.error(f"Error initializing QA client: {e}")
        return None

def repair_pdf_with_pikepdf(pdf_bytes):
    """
    Attempt to repair a corrupted PDF using pikepdf
    
    Args:
        pdf_bytes: PDF file bytes
    
    Returns:
        tuple: (repaired_bytes, success)
    """
    try:
        # Try to open and repair with pikepdf
        with pikepdf.open(io.BytesIO(pdf_bytes), allow_overwriting_input=True) as pdf:
            # Save to bytes
            output = io.BytesIO()
            pdf.save(output)
            output.seek(0)
            return output.read(), True
    except Exception as e:
        return None, False

def repair_pdf_with_pypdf2(pdf_bytes):
    """
    Attempt to repair a corrupted PDF using PyPDF2
    
    Args:
        pdf_bytes: PDF file bytes
    
    Returns:
        tuple: (repaired_bytes, success)
    """
    try:
        # Try to read and rewrite with PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes), strict=False)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return output.read(), True
    except Exception as e:
        return None, False

def extract_text_with_pdfplumber(pdf_bytes):
    """
    Extract text directly from PDF using pdfplumber
    
    Args:
        pdf_bytes: PDF file bytes
    
    Returns:
        tuple: (full text, list of texts per page, success status)
    """
    try:
        all_text = []
        page_texts = []
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if text:
                        page_texts.append(text)
                        all_text.append(text)
                    else:
                        page_texts.append("")
                except Exception as e:
                    page_texts.append("")
        
        if all_text and len(''.join(all_text).strip()) > 50:
            return '\n\n'.join(all_text), page_texts, True
        return None, None, False
    
    except Exception as e:
        return None, None, False

def extract_text_with_pypdf2(pdf_bytes):
    """
    Extract text directly from PDF using PyPDF2
    
    Args:
        pdf_bytes: PDF file bytes
    
    Returns:
        tuple: (full text, list of texts per page, success status)
    """
    try:
        all_text = []
        page_texts = []
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes), strict=False)
        
        for page_num in range(len(pdf_reader.pages)):
            try:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    page_texts.append(text)
                    all_text.append(text)
                else:
                    page_texts.append("")
            except Exception as e:
                page_texts.append("")
        
        if all_text and len(''.join(all_text).strip()) > 50:
            return '\n\n'.join(all_text), page_texts, True
        return None, None, False
    
    except Exception as e:
        return None, None, False

def extract_text_with_ocr(pdf_bytes, ocr_model, progress_container=None, filename="document"):
    """
    Extract text using OCR on PDF images
    
    Args:
        pdf_bytes: PDF file bytes
        ocr_model: PaddleOCR model
        progress_container: Status container
        filename: File name for progress messages
    
    Returns:
        tuple: (full text, list of texts per page, success status)
    """
    try:
        images = convert_from_bytes(pdf_bytes, dpi=200)
        
        all_text = []
        page_texts = []
        
        for idx, image in enumerate(images):
            if progress_container:
                progress_container.text(f"📄 {filename}: OCR processing page {idx + 1}/{len(images)}")
            
            try:
                # Save temporary image
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    image.save(tmp_file.name, 'PNG')
                    
                    # Apply OCR
                    result = ocr_model.ocr(tmp_file.name, cls=True)
                    
                    # Extract text
                    page_text = []
                    if result and result[0]:
                        for line in result[0]:
                            if line and len(line) > 1 and line[1]:
                                page_text.append(line[1][0])
                    
                    page_text_str = '\n'.join(page_text)
                    page_texts.append(page_text_str)
                    all_text.append(page_text_str)
                    
                    # Clean up
                    try:
                        os.unlink(tmp_file.name)
                    except:
                        pass
            except Exception as e:
                page_texts.append("")
        
        if all_text and len(''.join(all_text).strip()) > 50:
            return '\n\n'.join(all_text), page_texts, True
        return None, None, False
    
    except Exception as e:
        return None, None, False

def extract_text_from_pdf(pdf_file, ocr_model, progress_container=None):
    """
    Extract text from PDF using comprehensive multi-method approach with repair
    
    Complete strategy:
    1. Try direct text extraction with pdfplumber
    2. Try direct text extraction with PyPDF2
    3. Attempt PDF repair with pikepdf, then retry text extraction
    4. Attempt PDF repair with PyPDF2, then retry text extraction
    5. Try OCR on original PDF
    6. Try OCR on repaired PDF (if repair succeeded)
    
    Args:
        pdf_file: Uploaded PDF file
        ocr_model: PaddleOCR model
        progress_container: Status container
    
    Returns:
        tuple: (full text, list of texts per page, success status, method used)
    """
    filename = pdf_file.name
    
    # Read PDF bytes once
    pdf_file.seek(0)
    original_pdf_bytes = pdf_file.read()
    
    # Method 1: pdfplumber on original
    if progress_container:
        progress_container.info(f"📄 {filename}: Trying pdfplumber text extraction...")
    
    full_text, page_texts, success = extract_text_with_pdfplumber(original_pdf_bytes)
    if success:
        if progress_container:
            progress_container.success(f"✅ {filename}: Extracted with pdfplumber ({len(page_texts)} pages)")
        return full_text, page_texts, True, "pdfplumber"
    
    # Method 2: PyPDF2 on original
    if progress_container:
        progress_container.info(f"📄 {filename}: Trying PyPDF2 text extraction...")
    
    full_text, page_texts, success = extract_text_with_pypdf2(original_pdf_bytes)
    if success:
        if progress_container:
            progress_container.success(f"✅ {filename}: Extracted with PyPDF2 ({len(page_texts)} pages)")
        return full_text, page_texts, True, "PyPDF2"
    
    # Method 3: Repair with pikepdf, then retry text extraction
    if progress_container:
        progress_container.info(f"🔧 {filename}: Attempting PDF repair with pikepdf...")
    
    repaired_bytes, repair_success = repair_pdf_with_pikepdf(original_pdf_bytes)
    if repair_success and repaired_bytes:
        if progress_container:
            progress_container.success(f"✅ {filename}: PDF repaired with pikepdf, retrying extraction...")
        
        # Try pdfplumber on repaired
        full_text, page_texts, success = extract_text_with_pdfplumber(repaired_bytes)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted from repaired PDF with pdfplumber ({len(page_texts)} pages)")
            return full_text, page_texts, True, "pikepdf+pdfplumber"
        
        # Try PyPDF2 on repaired
        full_text, page_texts, success = extract_text_with_pypdf2(repaired_bytes)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted from repaired PDF with PyPDF2 ({len(page_texts)} pages)")
            return full_text, page_texts, True, "pikepdf+PyPDF2"
    
    # Method 4: Repair with PyPDF2, then retry text extraction
    if progress_container:
        progress_container.info(f"🔧 {filename}: Attempting PDF repair with PyPDF2...")
    
    repaired_bytes2, repair_success2 = repair_pdf_with_pypdf2(original_pdf_bytes)
    if repair_success2 and repaired_bytes2:
        if progress_container:
            progress_container.success(f"✅ {filename}: PDF repaired with PyPDF2, retrying extraction...")
        
        # Try pdfplumber on repaired
        full_text, page_texts, success = extract_text_with_pdfplumber(repaired_bytes2)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted from repaired PDF with pdfplumber ({len(page_texts)} pages)")
            return full_text, page_texts, True, "PyPDF2repair+pdfplumber"
        
        # Try PyPDF2 on repaired
        full_text, page_texts, success = extract_text_with_pypdf2(repaired_bytes2)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted from repaired PDF ({len(page_texts)} pages)")
            return full_text, page_texts, True, "PyPDF2repair+PyPDF2"
    
    # Method 5: OCR on original PDF
    if progress_container:
        progress_container.info(f"📄 {filename}: Attempting OCR on original PDF...")
    
    full_text, page_texts, success = extract_text_with_ocr(original_pdf_bytes, ocr_model, progress_container, filename)
    if success:
        if progress_container:
            progress_container.success(f"✅ {filename}: Extracted with OCR ({len(page_texts)} pages)")
        return full_text, page_texts, True, "OCR"
    
    # Method 6: OCR on repaired PDF (if we have one)
    if repaired_bytes:
        if progress_container:
            progress_container.info(f"📄 {filename}: Attempting OCR on pikepdf-repaired PDF...")
        
        full_text, page_texts, success = extract_text_with_ocr(repaired_bytes, ocr_model, progress_container, filename)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted with OCR from repaired PDF ({len(page_texts)} pages)")
            return full_text, page_texts, True, "pikepdf+OCR"
    
    if repaired_bytes2:
        if progress_container:
            progress_container.info(f"📄 {filename}: Attempting OCR on PyPDF2-repaired PDF...")
        
        full_text, page_texts, success = extract_text_with_ocr(repaired_bytes2, ocr_model, progress_container, filename)
        if success:
            if progress_container:
                progress_container.success(f"✅ {filename}: Extracted with OCR from repaired PDF ({len(page_texts)} pages)")
            return full_text, page_texts, True, "PyPDF2repair+OCR"
    
    # All methods failed
    if progress_container:
        progress_container.error(f"❌ {filename}: All extraction methods failed. PDF may be severely corrupted, encrypted, or empty.")
    
    return None, None, False, "failed"

def answer_question(question, context, client, model_name="gpt-4.1-mini"):
    """Answer a question based on context using language model"""
    try:
        max_context_chars = 20000
        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "\n\n[... context truncated due to size ...]"
        
        messages = [
            {
                "role": "system",
                "content": "You are an assistant specialized in answering questions based on documents. Analyze the provided context and answer the question precisely and concisely. If the answer is not in the context, clearly state that the information could not be found."
            },
            {
                "role": "user",
                "content": f"""Document context:
{context}

Question: {question}

Please answer the question based only on the context provided above."""
            }
        ]
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing question: {e}"

def answer_question_multi_doc(question, documents_context, client, model_name="gpt-4.1-mini"):
    """Answer a question based on multiple documents"""
    try:
        combined_context = ""
        for filename, context in documents_context.items():
            combined_context += f"\n\n=== Document: {filename} ===\n{context[:5000]}\n"
        
        max_context_chars = 20000
        if len(combined_context) > max_context_chars:
            combined_context = combined_context[:max_context_chars] + "\n\n[... context truncated due to size ...]"
        
        messages = [
            {
                "role": "system",
                "content": "You are an assistant specialized in answering questions based on multiple documents. Analyze all provided documents and answer the question precisely. Mention which document(s) contain the relevant information. If the answer is not in any document, clearly state that."
            },
            {
                "role": "user",
                "content": f"""Multiple documents context:
{combined_context}

Question: {question}

Please answer the question based on the documents provided above. Cite which document(s) you're referencing."""
            }
        ]
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=700
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing question: {e}"

def save_ocr_log(filename, page_texts, method="unknown"):
    """Save extraction log to file"""
    log_path = f"/home/ubuntu/ocr_logs/{filename}.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Extraction Method: {method}\n")
        f.write(f"Total Pages: {len(page_texts)}\n")
        f.write("=" * 50 + "\n\n")
        for idx, text in enumerate(page_texts):
            f.write(f"=== Page {idx + 1} ===\n")
            f.write(text)
            f.write("\n\n")
    return log_path

def update_todo(filename, num_pages, question, answer):
    """Update todo.md file with query information"""
    todo_path = "/home/ubuntu/todo.md"
    with open(todo_path, 'a', encoding='utf-8') as f:
        f.write(f"\n## {filename}\n")
        f.write(f"- **Pages:** {num_pages}\n")
        f.write(f"- **Question:** {question}\n")
        f.write(f"- **Answer:** {answer}\n")
        f.write(f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

# Main interface
st.title("📄 PDF Question Answering System")
st.markdown("""
This application uses **advanced multi-method extraction** with automatic PDF repair to handle any PDF file.

**Features:**
- ✅ Upload and batch process multiple PDF files (up to 50 GB each)
- ✅ **6-tier extraction strategy** with automatic fallbacks
- ✅ **Automatic PDF repair** for corrupted files
- ✅ Handles text-based, scanned, and corrupted PDFs
- ✅ Intelligent question answering across documents
- ✅ Comprehensive error handling and recovery
""")

# Load models
with st.spinner("Loading OCR and QA models..."):
    ocr_model = load_ocr_model()
    qa_client = load_qa_client()

if not qa_client:
    st.error("⚠️ QA system not available. Please check settings.")
    st.stop()

# File upload
st.header("1. Upload PDF Documents")
uploaded_files = st.file_uploader(
    "Select one or more PDF files (up to 50 GB each)",
    type=['pdf'],
    accept_multiple_files=True,
    help="Supports corrupted, scanned, and text-based PDFs. Automatic repair included!"
)

# Store data in session
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = {}

# Batch processing
if uploaded_files:
    st.markdown(f"**{len(uploaded_files)} file(s) selected**")
    
    with st.expander("📋 View selected files"):
        for f in uploaded_files:
            file_size_mb = f.size / (1024 * 1024)
            st.write(f"• {f.name} ({file_size_mb:.2f} MB)")
    
    unprocessed_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
    
    if unprocessed_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📦 {len(unprocessed_files)} file(s) ready to process")
        with col2:
            process_batch = st.button("🚀 Process All Files", type="primary", use_container_width=True)
        
        if process_batch:
            progress_text = st.empty()
            progress_bar = st.progress(0)
            status_container = st.container()
            
            successful = 0
            failed = 0
            methods_used = {}
            
            for idx, uploaded_file in enumerate(unprocessed_files):
                file_size_mb = uploaded_file.size / (1024 * 1024)
                
                if file_size_mb > 51200:
                    status_container.error(f"❌ '{uploaded_file.name}' exceeds 50 GB limit ({file_size_mb:.2f} MB)")
                    failed += 1
                    continue
                
                if file_size_mb > 1000:
                    status_container.warning(f"⚠️ '{uploaded_file.name}' is large ({file_size_mb:.2f} MB). Processing may take time.")
                
                progress_text.text(f"Processing {idx + 1}/{len(unprocessed_files)}: {uploaded_file.name}")
                
                uploaded_file.seek(0)
                full_text, page_texts, success, method = extract_text_from_pdf(uploaded_file, ocr_model, status_container)
                
                if success and full_text and page_texts:
                    log_path = save_ocr_log(uploaded_file.name, page_texts, method)
                    
                    st.session_state.processed_files[uploaded_file.name] = {
                        'full_text': full_text,
                        'page_texts': page_texts,
                        'num_pages': len(page_texts),
                        'log_path': log_path,
                        'method': method
                    }
                    
                    methods_used[method] = methods_used.get(method, 0) + 1
                    successful += 1
                else:
                    failed += 1
                
                progress_bar.progress((idx + 1) / len(unprocessed_files))
            
            progress_text.empty()
            progress_bar.empty()
            
            st.success(f"🎉 Batch processing complete! ✅ {successful} successful, ❌ {failed} failed")
            
            if successful > 0:
                methods_str = ", ".join([f"{k}={v}" for k, v in methods_used.items()])
                st.info(f"📊 Extraction methods used: {methods_str}")
                st.balloons()
    else:
        st.success(f"✅ All {len(uploaded_files)} file(s) already processed")

# Display processed documents
if st.session_state.processed_files:
    st.header("2. Processed Documents")
    
    total_pages = sum(data['num_pages'] for data in st.session_state.processed_files.values())
    total_chars = sum(len(data['full_text']) for data in st.session_state.processed_files.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", len(st.session_state.processed_files))
    with col2:
        st.metric("Total Pages", total_pages)
    with col3:
        st.metric("Total Characters", f"{total_chars:,}")
    
    for filename, data in st.session_state.processed_files.items():
        with st.expander(f"📄 {filename} ({data['num_pages']} pages) - Method: {data.get('method', 'unknown')}"):
            st.markdown(f"**Extraction method:** `{data.get('method', 'unknown')}`")
            st.markdown(f"**Log saved at:** `{data['log_path']}`")
            st.markdown(f"**Total characters:** {len(data['full_text']):,}")
            
            st.subheader("Text View by Page")
            for idx, page_text in enumerate(data['page_texts']):
                with st.expander(f"Page {idx + 1}"):
                    st.text_area(
                        f"Extracted text - Page {idx + 1}",
                        page_text,
                        height=200,
                        key=f"{filename}_page_{idx}",
                        disabled=True
                    )
    
    # Question answering
    st.header("3. Ask Questions")
    
    query_mode = st.radio(
        "Query Mode:",
        ["Single Document", "Multiple Documents"],
        help="Choose whether to ask questions about one document or search across all documents"
    )
    
    if query_mode == "Single Document":
        selected_file = st.selectbox(
            "Select the document to ask questions about:",
            list(st.session_state.processed_files.keys())
        )
        
        if selected_file:
            context = st.session_state.processed_files[selected_file]['full_text']
            st.info(f"📊 Selected: **{selected_file}** ({st.session_state.processed_files[selected_file]['num_pages']} pages)")
            
            question = st.text_input("Enter your question:", placeholder="e.g., What is the main topic?")
            
            with st.expander("⚙️ Advanced Options"):
                model_choice = st.selectbox("AI Model:", ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"], index=0)
            
            if st.button("🔍 Search Answer", type="primary") and question:
                with st.spinner("Processing question with AI..."):
                    answer = answer_question(question, context, qa_client, model_choice)
                    st.markdown("### 💡 Answer:")
                    st.success(answer)
                    update_todo(selected_file, st.session_state.processed_files[selected_file]['num_pages'], question, answer)
                    st.info("✅ Question and answer logged in `/home/ubuntu/todo.md`")
    
    else:
        st.info(f"📚 Searching across **{len(st.session_state.processed_files)}** document(s)")
        
        use_all_docs = st.checkbox("Use all documents", value=True)
        
        if use_all_docs:
            selected_docs = list(st.session_state.processed_files.keys())
        else:
            selected_docs = st.multiselect(
                "Select documents to search:",
                list(st.session_state.processed_files.keys()),
                default=list(st.session_state.processed_files.keys())
            )
        
        if selected_docs:
            st.write(f"**Selected {len(selected_docs)} document(s):**")
            for doc in selected_docs:
                st.write(f"• {doc}")
            
            question = st.text_input("Enter your question:", placeholder="e.g., Which documents mention...?", key="multi_doc_question")
            
            with st.expander("⚙️ Advanced Options"):
                model_choice = st.selectbox("AI Model:", ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"], index=0, key="multi_doc_model")
            
            if st.button("🔍 Search Across Documents", type="primary") and question:
                with st.spinner("Searching across multiple documents with AI..."):
                    docs_context = {doc: st.session_state.processed_files[doc]['full_text'] for doc in selected_docs}
                    answer = answer_question_multi_doc(question, docs_context, qa_client, model_choice)
                    st.markdown("### 💡 Answer:")
                    st.success(answer)
                    update_todo(f"Multiple Documents ({len(selected_docs)})", sum(st.session_state.processed_files[doc]['num_pages'] for doc in selected_docs), question, answer)
                    st.info("✅ Question and answer logged")
        else:
            st.warning("Please select at least one document")

else:
    st.info("👆 Upload PDF files to get started")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Built with Streamlit, PaddleOCR, and Advanced AI</strong></p>
    <p><em>Robust PDF Processing with Automatic Repair & Multi-Method Extraction</em></p>
</div>
""", unsafe_allow_html=True)

