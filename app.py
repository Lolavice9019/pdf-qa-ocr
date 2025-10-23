import streamlit as st
from openai import OpenAI
import PyPDF2
import pdfplumber
import io
import json
import gzip
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
    try:
        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAI(api_key=api_key)
    except:
        pass
    return None

client = get_client()

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
        elif ext == 'py':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'json':
            try:
                json_data = json.loads(file_bytes.decode('utf-8'))
                return json.dumps(json_data, indent=2)
            except:
                return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'env':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'sh':
            return file_bytes.decode('utf-8', errors='ignore')
        elif ext == 'gz':
            try:
                decompressed = gzip.decompress(file_bytes)
                return decompressed.decode('utf-8', errors='ignore')
            except:
                return "Error: Unable to decompress .gz file"
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
    
    # Bulk Export Section
    st.header("📦 Bulk Export All Documents")
    
    # Combine all documents
    all_text = "\n\n==========\n\n".join([
        f"FILE: {name}\n\n{doc['text']}"
        for name, doc in st.session_state.documents.items()
    ])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📝 Download All as TXT",
            export_txt(all_text, "all_documents"),
            "all_documents.txt",
            "text/plain",
            key="bulk_txt"
        )
    with col2:
        bulk_json = json.dumps({
            "exported_at": datetime.now().isoformat(),
            "document_count": len(st.session_state.documents),
            "documents": [
                {
                    "filename": name,
                    "text": doc['text'],
                    "size": doc['size'],
                    "processed_at": doc['processed_at']
                }
                for name, doc in st.session_state.documents.items()
            ]
        }, indent=2).encode('utf-8')
        st.download_button(
            "📦 Download All as JSON",
            bulk_json,
            "all_documents.json",
            "application/json",
            key="bulk_json"
        )
    with col3:
        st.download_button(
            "🌐 Download All as HTML",
            export_html(all_text, "all_documents"),
            "all_documents.html",
            "text/html",
            key="bulk_html"
        )

else:
    st.info("👆 Upload documents to get started")

# Footer
st.divider()
st.caption("Universal Document Q&A System | Powered by OpenAI")

