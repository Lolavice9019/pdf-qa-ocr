import streamlit as st
from openai import OpenAI
import PyPDF2
import pdfplumber
import io
import json
from datetime import datetime
from docx import Document
from pptx import Presentation
import openpyxl
from striprtf.striprtf import rtf_to_text
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub

st.set_page_config(
    page_title="Universal Document Q&A",
    page_icon="📄",
    layout="wide"
)

# Initialize OpenAI client
@st.cache_resource
def get_client():
    import os
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY to secrets.")
        return None
    return OpenAI(api_key=api_key)

client = get_client()

if not client:
    st.stop()

# Document extraction functions
def extract_pdf(file_bytes):
    """Extract text from PDF"""
    # Try pdfplumber first
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = "\n\n".join([page.extract_text() or "" for page in pdf.pages])
            if len(text.strip()) > 50:
                return text
    except:
        pass
    
    # Try PyPDF2
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        if len(text.strip()) > 50:
            return text
    except:
        pass
    
    return "Could not extract text from PDF"

def extract_docx(file_bytes):
    """Extract text from DOCX"""
    doc = Document(io.BytesIO(file_bytes))
    return "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_pptx(file_bytes):
    """Extract text from PPTX"""
    prs = Presentation(io.BytesIO(file_bytes))
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n\n".join(text)

def extract_xlsx(file_bytes):
    """Extract text from XLSX"""
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes))
    text = []
    for sheet in wb.worksheets:
        text.append(f"Sheet: {sheet.title}")
        for row in sheet.iter_rows(values_only=True):
            row_text = " | ".join([str(cell) if cell is not None else "" for cell in row])
            if row_text.strip():
                text.append(row_text)
    return "\n".join(text)

def extract_text(file_bytes, filename):
    """Universal text extraction"""
    ext = filename.lower().split('.')[-1]
    
    try:
        if ext == 'pdf':
            return extract_pdf(file_bytes)
        elif ext in ['docx', 'doc']:
            return extract_docx(file_bytes)
        elif ext in ['pptx', 'ppt']:
            return extract_pptx(file_bytes)
        elif ext in ['xlsx', 'xls']:
            return extract_xlsx(file_bytes)
        elif ext == 'txt':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'csv':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'md':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'rtf':
            return rtf_to_text(file_bytes.decode('utf-8', errors='ignore'))
        elif ext in ['html', 'htm']:
            soup = BeautifulSoup(file_bytes, 'html.parser')
            return soup.get_text()
        elif ext == 'epub':
            book = epub.read_epub(io.BytesIO(file_bytes))
            text = []
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text.append(soup.get_text())
            return "\n\n".join(text)
        else:
            return file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Export functions
def export_txt(text, filename):
    return text.encode('utf-8')

def export_json(text, filename):
    data = {
        "filename": filename,
        "extracted_at": datetime.now().isoformat(),
        "text": text,
        "character_count": len(text)
    }
    return json.dumps(data, indent=2).encode('utf-8')

def export_html(text, filename):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{filename}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <h1>{filename}</h1>
    <pre>{text}</pre>
</body>
</html>"""
    return html.encode('utf-8')

# Main UI
st.title("📄 Universal Document Q&A System")

st.markdown("""
### Features
- 📤 Upload any document type (PDF, DOCX, PPTX, XLSX, TXT, HTML, etc.)
- 🔍 Extract text automatically
- 💬 Ask questions about your documents
- 💾 Export in multiple formats (TXT, JSON, HTML)
""")

# File upload
uploaded_files = st.file_uploader(
    "Upload your documents",
    accept_multiple_files=True,
    type=['pdf', 'docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls', 'txt', 'csv', 'md', 'rtf', 'html', 'htm', 'epub']
)

if uploaded_files:
    # Store extracted documents
    if 'documents' not in st.session_state:
        st.session_state.documents = {}
    
    # Process files
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.documents:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                file_bytes = uploaded_file.read()
                text = extract_text(file_bytes, uploaded_file.name)
                st.session_state.documents[uploaded_file.name] = {
                    'text': text,
                    'size': len(file_bytes),
                    'processed_at': datetime.now().isoformat()
                }
    
    # Display processed documents
    st.success(f"✅ {len(st.session_state.documents)} document(s) processed")
    
    # Show document list
    with st.expander("📋 View Processed Documents"):
        for name, doc in st.session_state.documents.items():
            st.write(f"**{name}**")
            st.write(f"- Characters: {len(doc['text']):,}")
            st.write(f"- Size: {doc['size']:,} bytes")
            
            # Preview
            preview = doc['text'][:500] + "..." if len(doc['text']) > 500 else doc['text']
            st.text_area(f"Preview of {name}", preview, height=100, key=f"preview_{name}")
            
            # Export buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "💾 Download TXT",
                    export_txt(doc['text'], name),
                    f"{name}.txt",
                    "text/plain",
                    key=f"txt_{name}"
                )
            with col2:
                st.download_button(
                    "📦 Download JSON",
                    export_json(doc['text'], name),
                    f"{name}.json",
                    "application/json",
                    key=f"json_{name}"
                )
            with col3:
                st.download_button(
                    "🌐 Download HTML",
                    export_html(doc['text'], name),
                    f"{name}.html",
                    "text/html",
                    key=f"html_{name}"
                )
            st.divider()
    
    # Q&A Section
    st.header("💬 Ask Questions")
    
    # Select documents to query
    doc_names = list(st.session_state.documents.keys())
    if len(doc_names) > 1:
        selected_docs = st.multiselect(
            "Select documents to search",
            doc_names,
            default=doc_names
        )
    else:
        selected_docs = doc_names
    
    # Question input
    question = st.text_input("Ask a question about your documents:")
    
    if question and st.button("🔍 Get Answer"):
        with st.spinner("Thinking..."):
            # Combine selected documents
            combined_text = "\n\n---\n\n".join([
                f"Document: {name}\n\n{st.session_state.documents[name]['text']}"
                for name in selected_docs
            ])
            
            # Query OpenAI
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided documents. Always cite which document(s) you're referencing."},
                        {"role": "user", "content": f"Documents:\n\n{combined_text}\n\nQuestion: {question}"}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                answer = response.choices[0].message.content
                
                st.success("✅ Answer:")
                st.write(answer)
                
                # Save to history
                if 'qa_history' not in st.session_state:
                    st.session_state.qa_history = []
                st.session_state.qa_history.append({
                    'question': question,
                    'answer': answer,
                    'documents': selected_docs,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Show Q&A history
    if 'qa_history' in st.session_state and st.session_state.qa_history:
        with st.expander("📜 Q&A History"):
            for i, qa in enumerate(reversed(st.session_state.qa_history)):
                st.write(f"**Q{len(st.session_state.qa_history)-i}:** {qa['question']}")
                st.write(f"**A:** {qa['answer']}")
                st.caption(f"Documents: {', '.join(qa['documents'])}")
                st.divider()

else:
    st.info("👆 Upload documents to get started")

# Footer
st.divider()
st.caption("Universal Document Q&A System | Powered by OpenAI")

