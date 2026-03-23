# USE CASE 7: Intelligent Procurement Assistant

## Quick Summary
Automated commodity code extraction and validation from procurement contracts using pattern matching + LLM. Validates extracted codes against UNSPSC/CPV standards. Streamlit interface for manual correction.

---

## Customer Pain Point

**What you'd hear:**
"Our procurement team manually processes contracts to extract commodity codes. It's time-consuming and inconsistent. We need to automatically extract UNSPSC codes, validate them, and flag ambiguous cases for review."

**Business Impact:**
- Current processing: 1 hour per contract
- Contracts per month: 200
- Opportunity: Save 150 hours/month = 1 FTE

---

## Discovery Questions

1. **"What formats are contracts in?"** (PDF, DOCX, images?)
2. **"How complex are the codes?"** (UNSPSC 8-digit? Industry-specific?)
3. **"Accuracy requirements?"** (95%? 99%?)
4. **"What happens after extraction?"** (Imported to SAP? Used for reporting?)
5. **"Do you have a commodity codebook?"** (Yes → can validate; No → harder to validate)

---

## Your Approach

### Phase 1: Text Extraction
"Extract text from contracts:

```python
# PDF extraction
import PyPDF2
pdf_reader = PyPDF2.PdfReader('contract.pdf')
text = ''
for page in pdf_reader.pages:
    text += page.extract_text()

# DOCX extraction
from docx import Document
doc = Document('contract.docx')
text = '\\n'.join([para.text for para in doc.paragraphs])

# Result: Full contract text
```"

### Phase 2: Pattern-Based Matching (MVP)
"80% of cases can be solved with pattern matching:

```
UNSPSC codes: Look for 8-digit sequences in specific contexts
CPV codes: Look for 8-digit sequences with dashes

Pattern:
- Commodity Code: <8 digits>
- UNSPSC: <8 digits>
- Code: <8 digits>

Regular expression:
```python
import re
COMMODITY_PATTERN = r'(?:commodity code|code|UNSPSC)[\\s:]*([0-9]{8})'
matches = re.findall(COMMODITY_PATTERN, text, re.IGNORECASE)
```

Why patterns first?
- Fast (microseconds)
- Accurate (95%+ for standard formats)
- No ML training needed
- Easy to maintain"

### Phase 3: Contextual Validation
"Validate extracted codes:

```
Is code in known UNSPSC database? (Yes → Valid)
Does context match expected commodity? (Yes → High confidence)
Is code plausible? (Check digit validation if applicable)

Example:
- Extracted: 12345678
- Check: Is this a plausible UNSPSC? (No → Flag as uncertain)
- Check: Does context mention 'software'? Code matches SW category? (Yes → Validated)
```"

### Phase 4: LLM for Ambiguous Cases
"20% of cases need LLM reasoning:

```python
# If pattern matching < 80% confidence
if confidence < 0.8:
    llm_result = llm.extract(f'''
        Extract commodity codes from this contract snippet:
        {contract_context}
        
        Return JSON with:
        - codes: [list of extracted codes]
        - description: what goods/services
        - confidence: 0-1
    ''')
```

Why LLM only for edge cases?
- Reduces LLM cost
- Maintains speed (most cases fast)
- LLM errors won't cascade"

### Phase 5: Streamlit UI
"Interactive review interface:

```python
import streamlit as st

uploaded_file = st.file_uploader('Upload Contract', type=['pdf', 'docx'])
if uploaded_file:
    extracted_data = extract_contract_data(uploaded_file)
    
    st.write('Extracted Commodity Codes:')
    for code in extracted_data['commodity_codes']:
        # Editable text input
        new_code = st.text_input(
            f'Code {code[\"code\"]}',
            value=code['code'],
            key=f'code_{code[\"id\"]}'
        )
        
        # Confidence badge
        st.write(f'Confidence: {code[\"confidence\"]:.0%}')
        
        # Description
        st.write(f'Description: {code[\"description\"]}')
    
    if st.button('Export'):
        export_to_csv(extracted_data)
```"

---

## Key Architectural Decisions

### Decision 1: Pattern-First Approach

**What you'd say:**
"I'd start with patterns because:

1. **Speed**: 0.01s vs. 2s for LLM
2. **Accuracy**: 95%+ for standard formats
3. **Cost**: Essentially free (no LLM calls)
4. **Maintainability**: Easy to update patterns

Only use LLM for the 20% of edge cases where patterns fail."

### Decision 2: Fuzzy Matching for Validation

**What you'd say:**
"For ambiguous codes, use fuzzy matching:

```python
from fuzzywuzzy import fuzz

extracted = 'Commodity Code 12345678'
standard = '12345678'  # From known database

score = fuzz.token_set_ratio(extracted, standard)
# If score > 85% → Accept
# If 60-85% → Flag for review
# If <60% → Reject
```"

### Decision 3: Progressive Validation

**What you'd say:**
"I'd validate progressively:

1. **Pattern match** → Code found?
2. **Database lookup** → Code in UNSPSC?
3. **Context match** → Does description match commodity type?
4. **Confidence score** → Combine all signals

Example:
- Pattern found: +50%
- Code in database: +30%
- Context matches: +20%
- Final: 90%+ confidence → Flag = green"

---

## Implementation Walk-Through

### Code Skeleton

```python
from fuzzywuzzy import fuzz
import re

def extract_commodity_codes(contract_text):
    # Step 1: Pattern matching
    pattern = r'(?:commodity|code|UNSPSC)[\\s:]*([0-9]{8})'
    pattern_matches = re.findall(pattern, contract_text, re.IGNORECASE)
    
    results = []
    for code in pattern_matches:
        # Step 2: Database lookup
        is_valid = code_database.contains(code)
        
        # Step 3: Context validation
        context = extract_context_around_code(contract_text, code)
        context_score = validate_context(code, context)
        
        # Step 4: Confidence score
        confidence = 0.5 if is_valid else 0.3
        confidence += context_score * 0.5
        
        results.append({
            'code': code,
            'confidence': confidence,
            'context': context,
            'status': 'validated' if confidence > 0.8 else 'needs_review'
        })
    
    # Step 5: LLM for low-confidence cases
    for result in results:
        if result['confidence'] < 0.7:
            llm_analysis = llm.refine(result['context'])
            result['llm_confidence'] = llm_analysis['confidence']
            result['status'] = 'llm_reviewed'
    
    return results
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Pattern misses valid codes** | Combine multiple patterns, manual search option |
| **LLM extracts wrong code** | Validate against database, flag for review |
| **Context validation too strict** | Allow user override with audit trail |
| **Performance on large contracts** | Stream processing, pagination |

---

## Success Metrics

**Accuracy:**
- 95%+ accuracy on standard formats
- <5% false positive rate

**Speed:**
- Average extraction: 1 minute (vs. 10 minutes manual)
- 95% of contracts require no manual correction

**Adoption:**
- 80% of contracts automated

**Cost:**
- Save 150 hours/month = €5k+/month

---

## Related Use Cases

- **Purchase Order Extractor** (Similar: Document extraction)
- **AI PDF Information Extraction** (Similar: Vision-based extraction)
