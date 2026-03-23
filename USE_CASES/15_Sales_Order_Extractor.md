# USE CASE 15: Sales Order Extractor

## Quick Summary
Extract structured data from sales orders (email attachments, PDFs, scanned forms) using Document AI + LLM fallback. Returns order number, customer, items, quantities, prices for SAP import.

---

## Customer Pain Point

**What you'd hear:**
"Our sales team gets orders in various formats—emails, scanned forms, PDFs. Manual data entry into SAP is slow and error-prone. We need automated extraction and validation."

**Business Impact:**
- Current processing: 20 min per order
- Orders/day: 50
- Time loss: 16+ hours/day
- Opportunity: Save 80 hours/week

---

## Your Approach

**Similar to Use Case 8 (Purchase Order Extractor), but:**

- **Input**: Sales orders from customers (not POs from us)
- **Flow**: Extraction → Validation → SAP SD order creation
- **Key fields**: Customer name, items, quantities, requested delivery date
- **Output**: Integrated directly to SAP SD (sales & distribution)

### Architecture:

```
1. Order arrives (email, PDF, form)
2. Extract text/images
3. Use Document AI for layout-aware extraction
4. LLM fallback for ambiguous cases
5. Validate customer exists in SAP
6. Validate items exist
7. Create SD order automatically (if high confidence)
8. Route to review if lower confidence
```

---

## Key Difference from PO Extractor

- **PO**: We extract POs WE send to suppliers
- **Sales Order**: We extract orders FROM customers

Same technology, different data flow and business process.

---

## Implementation

```python
# Very similar to PO extraction
def extract_sales_order(document_path):
    # Document AI extraction
    extracted = document_ai.process(document_path)
    
    # Key fields for sales order
    order = {
        'customer_name': extracted.get('customer'),
        'customer_code': lookup_customer(extracted['customer']),
        'line_items': extracted.get('items', []),
        'requested_delivery': extracted.get('delivery_date'),
        'special_instructions': extracted.get('notes')
    }
    
    # Validate
    if order['customer_code']:  # Customer found
        create_sap_sd_order(order)
    else:
        queue_for_review(order)
    
    return order
```

---

## Success Metrics

- 80% automated order creation
- <1 minute processing per order
- Save 80+ hours/week
- 95%+ accuracy

---

## Related Use Cases

- **Purchase Order Extractor** (Similar: Document extraction, different flow)
