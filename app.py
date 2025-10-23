import streamlit as st
import tempfile
import os
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
from openai import OpenAI
from datetime import datetime

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

def extract_text_from_pdf(pdf_file, ocr_model):
    """
    Extract text from a PDF file using OCR
    
    Args:
        pdf_file: Uploaded PDF file
        ocr_model: Initialized PaddleOCR model
    
    Returns:
        tuple: (full text, list of texts per page, list of images)
    """
    try:
        # Convert PDF to images
        pdf_bytes = pdf_file.read()
        images = convert_from_bytes(pdf_bytes)
        
        all_text = []
        page_texts = []
        
        # Process each page
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, image in enumerate(images):
            status_text.text(f"Processing page {idx + 1} of {len(images)}...")
            
            # Save temporary image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                image.save(tmp_file.name)
                
                # Apply OCR
                result = ocr_model.ocr(tmp_file.name, cls=True)
                
                # Extract text
                page_text = []
                if result and result[0]:
                    for line in result[0]:
                        if line[1]:
                            page_text.append(line[1][0])
                
                page_text_str = '\n'.join(page_text)
                page_texts.append(page_text_str)
                all_text.append(page_text_str)
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
            
            # Update progress bar
            progress_bar.progress((idx + 1) / len(images))
        
        progress_bar.empty()
        status_text.empty()
        return '\n\n'.join(all_text), page_texts, images
    
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        
        # Offer recovery options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Reprocess", key=f"retry_{pdf_file.name}"):
                return extract_text_from_pdf(pdf_file, ocr_model)
        with col2:
            if st.button("⏭️ Ignore error", key=f"ignore_{pdf_file.name}"):
                return None, None, None
        with col3:
            if st.button("🚫 Skip page", key=f"skip_{pdf_file.name}"):
                return None, None, None
        
        return None, None, None

def answer_question(question, context, client, model_name="gpt-4.1-mini"):
    """
    Answer a question based on context using language model
    
    Args:
        question: User's question
        context: Context extracted from PDF
        client: OpenAI client
        model_name: Model name to use
    
    Returns:
        str: Answer found
    """
    try:
        # Limit context if too large (max ~6000 tokens to leave space for response)
        max_context_chars = 20000
        if len(context) > max_context_chars:
            context = context[:max_context_chars] + "\n\n[... context truncated due to size ...]"
        
        # Create prompt for QA
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
        
        # Make API call
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        return answer
    
    except Exception as e:
        return f"Error processing question: {e}"

def save_ocr_log(filename, page_texts):
    """Save OCR log to file"""
    log_path = f"/home/ubuntu/ocr_logs/{filename}.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
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
This application allows you to upload PDF documents, extract text using OCR (PaddleOCR), 
and ask questions about the content using advanced AI for Question Answering.

**Features:**
- ✅ Upload multiple PDF files (up to 1 GB each)
- ✅ Text extraction via OCR with PaddleOCR
- ✅ Intelligent question answering system
- ✅ View extracted text by page
- ✅ Automatic processing logs
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
    "Select one or more PDF files (up to 1 GB each)",
    type=['pdf'],
    accept_multiple_files=True
)

# Store data in session
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = {}

# Process files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        # Check size
        if file_size_mb > 1024:
            st.error(f"❌ File '{uploaded_file.name}' exceeds 1 GB limit ({file_size_mb:.2f} MB)")
            continue
        
        # Check if already processed
        if uploaded_file.name in st.session_state.processed_files:
            st.info(f"✅ File '{uploaded_file.name}' was already processed")
            continue
        
        # Warn if file is large
        if file_size_mb > 100:
            st.warning(f"⚠️ File '{uploaded_file.name}' is large ({file_size_mb:.2f} MB). Processing may take time.")
            
            col1, col2 = st.columns(2)
            process_file = False
            
            with col1:
                if st.button(f"✅ Process anyway", key=f"process_{uploaded_file.name}"):
                    process_file = True
            with col2:
                if st.button(f"⏭️ Skip file", key=f"skip_{uploaded_file.name}"):
                    st.info(f"File '{uploaded_file.name}' was skipped.")
                    continue
        else:
            process_file = True
        
        if process_file:
            with st.spinner(f"Processing '{uploaded_file.name}' with OCR..."):
                # Reset file pointer
                uploaded_file.seek(0)
                full_text, page_texts, images = extract_text_from_pdf(uploaded_file, ocr_model)
                
                if full_text and page_texts:
                    # Save log
                    log_path = save_ocr_log(uploaded_file.name, page_texts)
                    
                    # Store in session
                    st.session_state.processed_files[uploaded_file.name] = {
                        'full_text': full_text,
                        'page_texts': page_texts,
                        'num_pages': len(page_texts),
                        'log_path': log_path
                    }
                    
                    st.success(f"✅ '{uploaded_file.name}' processed successfully! ({len(page_texts)} pages)")
                    st.balloons()
                else:
                    st.error(f"❌ Failed to process '{uploaded_file.name}'. Please try again or use another file.")

# Display processed documents
if st.session_state.processed_files:
    st.header("2. Processed Documents")
    
    for filename, data in st.session_state.processed_files.items():
        with st.expander(f"📄 {filename} ({data['num_pages']} pages)"):
            st.markdown(f"**OCR log saved at:** `{data['log_path']}`")
            st.markdown(f"**Total characters extracted:** {len(data['full_text'])}")
            
            # Show text by page
            st.subheader("OCR View by Page")
            for idx, page_text in enumerate(data['page_texts']):
                with st.expander(f"Page {idx + 1}"):
                    st.text_area(
                        f"Extracted text - Page {idx + 1}",
                        page_text,
                        height=200,
                        key=f"{filename}_page_{idx}",
                        disabled=True
                    )
    
    # Question answering system
    st.header("3. Ask Questions")
    
    # Select document
    selected_file = st.selectbox(
        "Select the document to ask questions about:",
        list(st.session_state.processed_files.keys())
    )
    
    if selected_file:
        context = st.session_state.processed_files[selected_file]['full_text']
        
        st.info(f"📊 Selected document: **{selected_file}** ({st.session_state.processed_files[selected_file]['num_pages']} pages)")
        
        # Question field
        question = st.text_input("Enter your question:", placeholder="e.g., What is the main topic of the document?")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            model_choice = st.selectbox(
                "AI Model:",
                ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"],
                index=0
            )
        
        if st.button("🔍 Search Answer", type="primary") and question:
            with st.spinner("Processing question with AI..."):
                answer = answer_question(question, context, qa_client, model_choice)
                
                # Display answer
                st.markdown("### 💡 Answer:")
                st.success(answer)
                
                # Update todo.md
                update_todo(
                    selected_file,
                    st.session_state.processed_files[selected_file]['num_pages'],
                    question,
                    answer
                )
                
                st.info("✅ Question and answer logged in `/home/ubuntu/todo.md`")

else:
    st.info("👆 Upload PDF files to get started")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Built with Streamlit, PaddleOCR, and Advanced AI</strong></p>
    <p><em>PDF Document Question Answering System</em></p>
</div>
""", unsafe_allow_html=True)

