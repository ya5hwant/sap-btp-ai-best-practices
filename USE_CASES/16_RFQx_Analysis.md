# USE CASE 16: RFQx Document Analysis Utilities

## Quick Summary
Advanced RFQ (Request for Quotation) analysis system using multi-page Streamlit interface. Upload supplier quotations, extract structured data, compare suppliers, generate recommendations. Knowledge graph visualization.

---

## Customer Pain Point

**What you'd hear:**
"When we issue RFQs to suppliers, we get quotations back in various formats and structures. Comparing 10+ suppliers manually is tedious. We need intelligent analysis and comparison."

**Business Impact:**
- Current RFQ analysis: 8 hours per project
- RFQ projects/month: 20
- Opportunity: Save 160 hours/month

---

## Your Approach

### Phase 1: Project Setup
"Create RFQ project, define items to source"

### Phase 2: Process Supplier Documents
"Upload supplier quotations:

```
- Extract: Supplier name, quoted prices, terms, delivery
- Validate: Prices reasonable? Terms compliant?
- Structure: Normalize into comparable format
```"

### Phase 3: Supplier Comparison
"Generate comparison matrix:

```
Supplier 1 | Supplier 2 | Supplier 3
-----------+-----------+----------
Price: $50 | $45       | $48
Lead time: | 2 weeks   | 3 weeks
...
```"

### Phase 4: Knowledge Graph
"Visualize relationships:

```
Supplier → Offers → Product
  ↓           ↓
Rating    Price/Quality

Interactive network showing:
- Which suppliers offer which products
- Price/quality tradeoffs
- Risk factors
```"

### Phase 5: AI Recommendations
"LLM generates narrative:

```
'Supplier B offers best value—lowest price + shortest lead time.
Risk: Smaller company, less track record.
Recommendation: Use Supplier B for 60% volume, 
Supplier A (trusted) for 40% as backup.'
```"

---

## Implementation

```python
import streamlit as st
import pandas as pd

# Page 1: Project Setup
if page == "Project Setup":
    st.write("Create RFQ Project")
    project_name = st.text_input("Project name")
    items = st.text_area("Items to source (one per line)")

# Page 2: Process Suppliers
elif page == "Process Suppliers":
    uploaded_file = st.file_uploader("Upload supplier quote", type=['pdf', 'xlsx'])
    if uploaded_file:
        extracted = extract_rfq(uploaded_file)
        st.write(extracted)
        st.button("Add to project")

# Page 3: Compare Suppliers
elif page == "Compare Suppliers":
    comparison_df = generate_comparison_matrix()
    st.dataframe(comparison_df)
    st.download_button("Download comparison", comparison_df.to_csv())

# Page 4: Recommendations
elif page == "Recommendations":
    recommendations = llm.analyze_rfq_results(suppliers, items)
    st.write(recommendations)
```

---

## Success Metrics

- 80% faster RFQ analysis
- Better supplier selection (cost + quality)
- Improved supplier performance tracking

---

## Related Use Cases

- **AI Capability Matcher** (Similar: Product-supplier matching)
- **Intelligent Negotiation** (Similar: Supplier analysis)
