# 📄 Universal Document Q&A System

**Process ANY document type and ask questions using AI**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 🌟 Features

- ✅ **Universal Document Support** - PDF, DOCX, PPTX, XLSX, TXT, HTML, RTF, EPUB, Markdown, CSV
- ✅ **Intelligent Text Extraction** - Automatic method selection per file type
- ✅ **PDF Repair & OCR** - Handles corrupted PDFs with automatic repair
- ✅ **Batch Processing** - Process multiple files at once (up to 50 GB each)
- ✅ **AI-Powered Q&A** - Ask questions about your documents using GPT-4
- ✅ **Multi-Document Search** - Query across multiple documents simultaneously
- ✅ **8 Export Formats** - TXT, JSON, HTML, Markdown, DOCX, PDF, CSV, XML
- ✅ **Real-time Progress** - Track processing status for each file
- ✅ **Automatic Logging** - All extractions and Q&A saved automatically

## 🚀 Quick Start

### Option 1: Use Online (Easiest)

Visit the live demo: [Coming Soon - Deploy to Streamlit Cloud]

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/Lolavice9019/pdf-qa-ocr.git
cd pdf-qa-ocr

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the app
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Option 3: Deploy Permanently

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to:
- Streamlit Cloud (Recommended - FREE)
- Heroku
- Railway
- Google Cloud Run
- AWS EC2

## 📚 Supported File Types

### Office Documents
- **DOCX/DOC** - Microsoft Word
- **PPTX/PPT** - PowerPoint presentations  
- **XLSX/XLS** - Excel spreadsheets

### Text Formats
- **TXT** - Plain text
- **CSV** - Comma-separated values
- **RTF** - Rich Text Format
- **MD** - Markdown files

### Web & eBooks
- **HTML/HTM** - Web pages
- **EPUB** - eBooks

### PDF
- **PDF** - With automatic repair and OCR fallback

## 🎯 How It Works

1. **Upload** - Select one or more documents
2. **Process** - Automatic text extraction using the best method for each file type
3. **Export** - Download extracted text in 8 different formats
4. **Ask Questions** - Use AI to get answers from your documents

## 💡 Use Cases

- 📋 **Contract Analysis** - Extract and search contract terms
- 📊 **Research Papers** - Compare methodologies across papers
- 💼 **Business Reports** - Find trends across quarterly reports
- 📖 **Documentation** - Search technical documentation
- 🎓 **Academic Research** - Analyze multiple research papers
- 📝 **Legal Documents** - Extract key information from legal files

## 🔧 Technology Stack

- **Frontend:** Streamlit
- **OCR:** PaddleOCR
- **AI:** OpenAI GPT-4
- **PDF Processing:** pdfplumber, PyPDF2, pikepdf, pdf2image
- **Document Processing:** python-docx, python-pptx, openpyxl
- **Export:** fpdf2, BeautifulSoup, ebooklib

## 📊 Export Formats

After processing, export your documents in multiple formats:

| Format | Use Case |
|--------|----------|
| **TXT** | Plain text for any editor |
| **JSON** | Structured data with metadata |
| **HTML** | View in web browser |
| **Markdown** | Documentation format |
| **DOCX** | Microsoft Word |
| **PDF** | Portable document |
| **CSV** | Spreadsheet import |
| **XML** | Data exchange |

## 🔐 Security & Privacy

- ✅ All processing happens on your server
- ✅ Documents are not stored permanently
- ✅ API keys are never exposed in code
- ✅ Logs are stored locally only

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - How to deploy permanently
- [Batch Processing Guide](BATCH_PROCESSING_GUIDE.md) - Advanced batch features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- OCR powered by [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- AI powered by [OpenAI](https://openai.com/)

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Lolavice9019/pdf-qa-ocr/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Lolavice9019/pdf-qa-ocr/discussions)

## ⭐ Star This Project

If you find this useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for document processing enthusiasts**

