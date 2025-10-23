# 📦 Batch Processing Guide

## Overview

The PDF Question Answering System now includes enhanced batch processing capabilities that allow you to efficiently process multiple PDF documents simultaneously and query across them.

## New Features

### 1. **Batch Upload and Processing**

Upload multiple PDF files at once and process them all with a single click.

**How to use:**
1. Click "Browse files" and select multiple PDFs (use Ctrl+Click or Cmd+Click)
2. Review the list of selected files
3. Click "🚀 Process All Files" button
4. Watch real-time progress as each file is processed
5. View summary statistics when complete

**Benefits:**
- Process dozens of documents in one session
- Real-time progress tracking for each file
- Automatic error handling and reporting
- Summary statistics (successful/failed)

### 2. **Multi-Document Query Mode**

Ask questions that search across multiple documents simultaneously.

**How to use:**
1. After processing documents, go to section "3. Ask Questions"
2. Select "Multiple Documents" mode
3. Choose to use all documents or select specific ones
4. Enter your question
5. Get answers that cite which document(s) contain the information

**Use cases:**
- "Which documents mention contract renewal terms?"
- "What are the common themes across all reports?"
- "Find all references to budget allocations"
- "Which document has the latest date?"

### 3. **Enhanced Statistics Dashboard**

View comprehensive statistics about all processed documents:
- Total number of documents
- Total pages across all documents
- Total characters extracted
- Individual document details

### 4. **Improved Progress Tracking**

**Batch Processing Features:**
- Overall progress bar showing completion percentage
- Per-file status updates
- Real-time error reporting
- Success/failure summary

## Comparison: Single vs Multi-Document Mode

| Feature | Single Document | Multiple Documents |
|---------|----------------|-------------------|
| **Speed** | Faster | Slightly slower |
| **Accuracy** | High precision | Good, with source citation |
| **Use Case** | Detailed analysis of one doc | Cross-document search |
| **Context** | Full document context | Limited context per doc |
| **Answer Format** | Direct answer | Answer with document references |

## Best Practices

### For Batch Processing

1. **Group similar documents**: Process related documents together for easier querying
2. **Check file sizes**: Large files take longer - consider processing in smaller batches
3. **Monitor progress**: Watch for any failed files and retry if needed
4. **Verify results**: Check the OCR output for at least one page per document

### For Multi-Document Queries

1. **Be specific**: Ask clear questions that can be answered from text
2. **Use document selection**: For targeted searches, select specific documents instead of all
3. **Expect citations**: The AI will mention which document(s) contain the answer
4. **Follow up**: Use single-document mode for deeper analysis of specific documents

## Performance Tips

### Processing Speed

**Factors affecting speed:**
- Number of pages per document
- Image quality and resolution
- Total number of documents
- Available system resources

**Optimization strategies:**
- Process during off-peak hours for large batches
- Split very large batches (50+ documents) into smaller groups
- Use compressed PDFs when possible
- Close other resource-intensive applications

### Query Performance

**For faster responses:**
- Use "gpt-4.1-nano" model for simple queries
- Limit multi-document queries to relevant documents only
- Keep questions concise and specific
- Use single-document mode when you know which document to search

## Example Workflows

### Workflow 1: Contract Analysis

**Scenario**: Analyze 20 vendor contracts

1. Upload all 20 PDF contracts
2. Click "Process All Files"
3. Wait for batch processing to complete
4. Switch to "Multiple Documents" mode
5. Ask: "Which contracts expire in 2025?"
6. Review answer with document citations
7. Switch to single-document mode for detailed analysis of specific contracts

### Workflow 2: Research Paper Review

**Scenario**: Review 10 academic papers

1. Upload all 10 papers
2. Batch process them
3. Multi-document query: "What methodologies are used across these papers?"
4. Multi-document query: "Which papers discuss machine learning?"
5. Select specific papers for detailed questions
6. Single-document query: "What are the limitations mentioned?"

### Workflow 3: Financial Report Comparison

**Scenario**: Compare quarterly reports

1. Upload Q1, Q2, Q3, Q4 reports
2. Process all at once
3. Multi-document query: "What is the revenue trend across quarters?"
4. Multi-document query: "Which quarter had the highest expenses?"
5. Single-document queries for specific details from each quarter

## Troubleshooting

### Issue: Batch processing stops midway

**Solutions:**
- Check error messages for specific failed files
- Verify file sizes are under 1 GB
- Ensure PDFs are not corrupted
- Try processing failed files individually

### Issue: Multi-document queries return incomplete answers

**Possible causes:**
- Too many documents selected (context limit exceeded)
- Question too broad or vague

**Solutions:**
- Reduce number of selected documents
- Make question more specific
- Use single-document mode for detailed analysis
- Break complex questions into multiple simpler ones

### Issue: Slow batch processing

**Solutions:**
- Process fewer documents at once
- Check system resources
- Use smaller/compressed PDFs
- Close other applications

## API Usage Considerations

### Cost Optimization

**For batch processing:**
- OCR is performed locally (no API cost)
- Only Q&A uses OpenAI API

**For queries:**
- Single-document queries: ~500-1000 tokens per query
- Multi-document queries: ~1000-2000 tokens per query
- Use "gpt-4.1-nano" for cost savings on simple queries

### Rate Limits

**Best practices:**
- Don't submit multiple queries simultaneously
- Wait for each query to complete
- For bulk queries, add small delays between them

## Advanced Features

### Document Selection Strategies

**Select all documents when:**
- Searching for specific information across entire corpus
- Comparing themes or patterns
- Finding which document contains specific data

**Select specific documents when:**
- You know which documents are relevant
- Working with a subset of related documents
- Reducing context size for better accuracy

### Query Optimization

**Good multi-document questions:**
- "Which documents mention [specific term]?"
- "Compare [metric] across all documents"
- "What is the latest date mentioned in any document?"
- "Which document has information about [topic]?"

**Questions better for single-document mode:**
- "Summarize this document"
- "What are all the details about [topic]?"
- "Explain the methodology in detail"
- "List all items mentioned"

## Future Enhancements

Potential features for future versions:
- Parallel processing for even faster batch operations
- Document comparison view
- Export results to CSV/Excel
- Saved query templates
- Document tagging and categorization
- Advanced filtering options

## Summary

The enhanced batch processing features make it easy to:
- ✅ Upload and process multiple PDFs simultaneously
- ✅ Track progress in real-time
- ✅ Query across multiple documents
- ✅ Get answers with source citations
- ✅ View comprehensive statistics
- ✅ Handle large document collections efficiently

For questions or issues, refer to the main README.md or open an issue on GitHub.

---

**Last updated:** October 23, 2025

