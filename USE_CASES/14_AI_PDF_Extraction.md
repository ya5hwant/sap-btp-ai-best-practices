# USE CASE 14: AI PDF Information Extraction

## Quick Summary
Comprehensive document processing system using GPT-4 Vision and SAP AI SDK. Extract structured data from PDFs: text, tables, images. Support complex layouts. Returns JSON/CSV for downstream processing.

---

## Customer Pain Point

**What you'd hear:**
"We receive hundreds of PDFs daily—reports, contracts, forms. Extracting data manually is slow and error-prone. We need intelligent extraction that handles complex layouts."

**Business Impact:**
- Current extraction: 30 min per document
- Error rate: 10%
- Documents/month: 500
- Opportunity: Save 250 hours/month

---

## Your Approach

### Phase 1: Document Intake
"Accept PDF uploads, store temporarily"

### Phase 2: Layout Analysis
"Understand document structure:

```
- Header section (title, date, etc.)
- Table sections (structured data)
- Text sections (body content)
- Footer sections
```"

### Phase 3: Multi-Modal Extraction
"Use combination:

```
GPT-4 Vision: Complex layouts, images, handwriting
Structured extraction: Tables (OCR → CSV)
LLM: Natural language understanding
```"

### Phase 4: Data Validation
"Validate extracted data:

```
- Required fields present?
- Data types correct? (date format, numbers)
- Cross-field consistency? (total = sum of items)
```"

### Phase 5: Export
"Return structured JSON/CSV:

```json
{
  "extracted_fields": {
    "invoice_number": "INV-001",
    "date": "2024-03-22",
    "line_items": [...]
  },
  "confidence": 0.95,
  "errors": []
}
```"

---

## Implementation

```python
from anthropic import Anthropic
import base64

def extract_pdf_info(pdf_path):
    client = Anthropic()
    
    # Convert PDF to images (page by page)
    images = convert_pdf_to_images(pdf_path)
    
    extracted_data = {}
    
    for page_num, image in enumerate(images):
        # Encode image
        image_data = base64.b64encode(image).decode('utf-8')
        
        # Extract using vision LLM
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"""Extract all information from this document page ({page_num}):
                            - Headers, titles, dates
                            - Tables (return as JSON array)
                            - Text content
                            - Any structured fields
                            
                            Return as JSON."""
                        }
                    ],
                }
            ],
        )
        
        page_data = json.loads(response.content[0].text)
        extracted_data[f'page_{page_num}'] = page_data
    
    # Combine all pages
    combined = combine_pages(extracted_data)
    
    # Validate
    validate_extracted_data(combined)
    
    return combined
```

---

## Success Metrics

- 95%+ accuracy extraction
- 90% of documents fully automated
- Save 200+ hours/month

---

## Related Use Cases

- **Purchase Order Extractor** (Similar: Document extraction)
- **Customer Credit Check** (Similar: Document processing)
