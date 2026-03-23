# USE CASE 8: Purchase Order Extractor

## Quick Summary
Automated PO extraction from supplier documents using Document AI + LLM fallback. Extracts: PO number, vendor, items, quantities, prices, delivery date. Validates structure and escalates errors.

---

## Customer Pain Point

**What you'd hear:**
"Purchase orders arrive in different formats—some scanned, some PDF, some handwritten. Manual data entry is error-prone and slow. We need to extract key data automatically and integrate with SAP."

**Business Impact:**
- Current processing: 15 min per PO
- Error rate: 5% (rework: €50 per correction)
- POs per month: 1000
- Opportunity: Save 250 hours/month = €40k+ (accounting for rework)

---

## Discovery Questions

1. **"What formats do POs arrive in?"** (PDF, scanned, EDI, email attachment?)
2. **"Any vendor consistency?"** (Same vendors repeatedly? Same format per vendor?)
3. **"Accuracy requirements?"** (95%? 99%? How critical are errors?)
4. **"Where does extracted data go?"** (SAP BTP procurement? ERP? Database?)
5. **"Special handling needed?"** (Multi-currency? Different units? Complex line items?)

---

## Your Approach

### Phase 1: Document Intake & Preprocessing
"Handle various input formats:

```
PDF: Extract text/images
Scanned image: Apply OCR preprocessing (contrast, deskew)
Email: Parse attachment, extract from body if present
EDI: Parse structured format directly

Preprocessing:
- Contrast enhancement (scanned documents)
- Deskew (rotated images)
- Resolution check (too low → request original)
```"

### Phase 2: Structured Data Extraction
"Use Document AI for layout-aware extraction:

```
SAP Document AI (Premium Edition):
- Pre-trained on financial documents
- High accuracy on standard PO templates
- Returns confidence scores per field
- Handles multi-page documents

Extracted fields:
- PO header: Number, date, vendor name, vendor code
- Billing/delivery addresses
- Line items: Product code, description, quantity, unit price, total
- Terms: Payment terms, delivery date, special instructions
```"

### Phase 3: Validation & Enrichment
"Validate extracted data:

```
Header validation:
- PO number format (expected pattern)
- Date is reasonable (not future date)
- Vendor exists in master data

Line item validation:
- Quantities positive
- Prices reasonable (within expected range)
- Total = Sum of line totals

Enrichment:
- Lookup vendor code by name (if missing)
- Lookup product code by description
- Calculate tax if missing
```"

### Phase 4: LLM Fallback
"For complex/ambiguous cases:

```python
if extraction_confidence < 0.8:
    # Use LLM as fallback
    llm_result = llm.extract_po(f'''
        Extract PO from this document:
        {document_text_or_image}
        
        Return JSON:
        {{
          'po_number': '',
          'vendor_name': '',
          'line_items': [{{
            'product_code': '',
            'quantity': 0,
            'unit_price': 0
          }}],
          'delivery_date': '',
          'total_amount': 0
        }}
    ''')
```

Why Document AI + LLM combo?
- Document AI: Fast, accurate on standard formats
- LLM: Flexible for unusual formats
- Together: Covers 99% of cases"

### Phase 5: Integration & Error Handling
"Push to SAP:

```
High confidence (>95%):
- Auto-create PO in SAP
- Send confirmation to vendor
- Mark in system as processed

Medium confidence (80-95%):
- Create draft PO
- Flag for analyst review
- Route to review queue

Low confidence (<80%):
- Request human input
- Show extraction with editable fields
- Analyst confirms before creating PO

Errors:
- Vendor not in master data → Create vendor record
- Product not found → Create placeholder
- Currency missing → Ask user
```"

---

## Key Architectural Decisions

### Decision 1: Document AI vs. Open Source

**What you'd say:**
"I'd choose SAP Document AI (Premium) because:

✓ Pre-trained specifically on financial documents
✓ 95%+ accuracy on standard formats
✓ Returns confidence scores
✓ SAP integration built-in

Open source alternatives (LayoutLM, Donut):
- Would work but require fine-tuning
- Less mature SAP integration
- Trade-off: More control vs. more work"

### Decision 2: Queue-Based Processing

**What you'd say:**
"For high volume (1000+ POs/month):

1. Document arrives → Store in S3
2. Trigger extraction job (async queue)
3. Extract data (takes 5-10 seconds)
4. Validate & enrich (takes 2-3 seconds)
5. Create SAP PO or route to review
6. Send confirmation email

Why queue?
- Non-blocking: User doesn't wait
- Scalable: Process in parallel
- Recoverable: Failed jobs can retry"

### Decision 3: Error Escalation

**What you'd say:**
"Multi-tier escalation:

```
Low confidence → Manual review queue
Vendor not found → Create new vendor (with approval)
Product not found → Use LLM to suggest existing product
Currency mismatch → Flag + ask user
Date format ambiguous → Show options to user
```"

---

## Implementation Walk-Through

### Code Skeleton

```python
from google.cloud import documentai_v1
import json

def extract_purchase_order(document_path):
    # Initialize Document AI
    client = documentai_v1.DocumentProcessorServiceClient()
    processor_name = client.processor_path(
        PROJECT_ID, LOCATION, PROCESSOR_ID
    )
    
    # Read document
    with open(document_path, 'rb') as f:
        image = f.read()
    
    # Process with Document AI
    document = documentai_v1.Document(raw_document={'content': image})
    request = documentai_v1.ProcessRequest(
        name=processor_name,
        raw_document=document.raw_document
    )
    response = client.process_document(request=request)
    document = response.document
    
    # Extract structured data
    extracted = {
        'po_number': document.text[0:20],  # Simplified
        'vendor_name': '',
        'line_items': [],
        'total_amount': 0
    }
    
    # Parse document entities
    for entity in document.entities:
        if entity.type_ == 'po_number':
            extracted['po_number'] = entity.normalized_value.text
        elif entity.type_ == 'vendor':
            extracted['vendor_name'] = entity.normalized_value.text
        elif entity.type_ == 'line_item':
            extracted['line_items'].append({
                'product': entity.properties[0].normalized_value.text,
                'quantity': float(entity.properties[1].normalized_value.text),
                'price': float(entity.properties[2].normalized_value.text)
            })
    
    # Validate
    validation_result = validate_po(extracted)
    
    # Enrich (lookup vendor, product codes)
    enriched = enrich_with_master_data(extracted)
    
    # Integrate with SAP
    if validation_result['confidence'] > 0.95:
        create_sap_po(enriched)
    else:
        queue_for_review(enriched, validation_result)
    
    return enriched
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Extraction fails on unusual format** | Fallback to LLM, manual review queue |
| **Vendor/product not in master data** | Auto-create with approval workflow |
| **Duplicate PO creation** | Check for existing PO before creating |
| **Currency/unit mismatch** | Validate against company supported currencies |
| **Price outliers** | Flag if >20% deviation from average supplier price |

---

## Success Metrics

**Speed:**
- Automated extraction: 80% of POs
- Latency: <1 minute end-to-end

**Accuracy:**
- 95%+ accurate extraction
- <1% incorrect PO creation rate

**Cost:**
- Save 200+ hours/month (€12k+/month)
- Rework reduction: 80%

**User Adoption:**
- 90% confidence in automated POs
- <5% manual override rate

---

## Related Use Cases

- **Sales Order Extractor** (Similar: Document extraction, different document type)
- **Customer Credit Check** (Similar: Document validation and enrichment)
