# USE CASE 9: AI Capability Matcher

## Quick Summary
Semantic matching of products to customer requirements using embeddings + vector search. Extract customer needs → Generate embedding → Search HANA vector table → Rank by relevance → Recommend products.

---

## Customer Pain Point

**What you'd hear:**
"Our sales team spends hours matching customer requirements to products. We have 10k+ products across different categories. Customers describe needs in natural language, and our team has to manually search through catalogs. We need intelligent matching."

**Business Impact:**
- Current matching time: 1 hour per customer
- Success rate: 60% (sometimes miss better products)
- Opportunity: Speed up + improve recommendation quality

---

## Discovery Questions

1. **"How are products currently structured?"** (Database? Categories? Attributes?)
2. **"What product metadata exists?"** (Specs, use cases, customer reviews?)
3. **"How many products?"** (1000? 10k? 100k?)
4. **"What's the matching process?"** (Text-based search? Category browsing?)
5. **"Should recommendations be exact matches or similar alternatives?"**

---

## Your Approach

### Phase 1: Product & Metadata Preparation
"Load all products with rich metadata:

```
Product:
- ID, name, category, description
- Specifications (technical details)
- Use cases (what it's used for)
- Customer reviews (what users say about it)
- Industry vertical (automotive, finance, etc.)

Combine into searchable text:
product_text = f'''
{name}
{description}
{', '.join(use_cases)}
Industry: {', '.join(verticals)}
Specs: {', '.join(specs)}
'''
```"

### Phase 2: Embedding Generation
"Convert product text to embeddings:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Free, fast, good quality

# Generate embeddings for all products
for product in products:
    embedding = model.encode(product['text'])  # 384-dim vector
    save_to_hana_vector_table(product['id'], embedding)
    
# Result: HANA table with columns: product_id, embedding, metadata
```

Why sentence-transformers?
- Free (no API costs)
- Fast (can run locally)
- Good quality (trained on sentence pairs)
- Offline (no external dependencies)"

### Phase 3: Customer Need Extraction
"Extract customer requirements:

```
Customer: 'We need a solution for real-time order processing'

Extract needs:
- Use case: 'real-time order processing'
- Industry: (inferred from context)
- Priority: (real-time = speed critical)
- Scale: (how many orders?)
```"

### Phase 4: Vector Search
"Search HANA vector table for similar products:

```sql
-- Cosine similarity search in HANA
SELECT 
    product_id,
    product_name,
    COSINE_SIMILARITY(customer_embedding, product_embedding) AS similarity
FROM hana_vector_products
WHERE COSINE_SIMILARITY(customer_embedding, product_embedding) > 0.5
ORDER BY similarity DESC
LIMIT 5
```

Why HANA?
- Native vector search (O(1) lookup with indexing)
- Scales to 1M+ products
- Integration with product metadata
- Can combine with SQL filters"

### Phase 5: Re-ranking & Recommendation
"Combine multiple signals:

```
Pure similarity: 50% weight
Company fit: 20% weight (industry match)
Review score: 20% weight (customer satisfaction)
Available inventory: 10% weight

Final score = 0.5 * similarity + 0.2 * industry_fit + 0.2 * reviews + 0.1 * availability

Result: Top 5 ranked recommendations
```"

---

## Key Architectural Decisions

### Decision 1: sentence-transformers vs. OpenAI Embeddings

**What you'd say:**
"I'd use **sentence-transformers** because:

✓ Free (no API costs)
✓ Offline (no latency, no privacy concerns)
✓ Fast (milliseconds per embedding)
✓ Good quality (trained specifically for sentence similarity)

OpenAI embeddings:
- Better quality (+5-10%)
- Cost: €0.02 per 1M tokens
- For 10k products: negligible cost
- But sentence-transformers is sufficient for most use cases"

### Decision 2: HANA Vector Search

**What you'd say:**
"I'd use **HANA Vector Tables** because:

✓ Native integration with SAP
✓ Fast indexing (can handle 1M+ vectors)
✓ Can combine with SQL filters (e.g., 'only in stock')
✓ Scalable to enterprise scale

Alternatives:
- Weaviate: Open source, good but external system
- Pinecone: Cloud, easy but expensive and external
- HANA: Already have it, integrated"

### Decision 3: Re-ranking Strategy

**What you'd say:**
"Multi-stage search:

1. **Vector search**: Return top 100 by similarity (fast, coarse-grained)
2. **Filter**: Remove out-of-stock, incompatible specs
3. **Re-rank**: Combine 5 signals (similarity + fit + reviews + price + availability)
4. **Diversify**: Avoid similar products (show different solutions)
5. **Explain**: Show why each product recommended"

---

## Implementation Walk-Through

### Code Skeleton

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Step 1: Generate product embeddings (batch)
model = SentenceTransformer('all-MiniLM-L6-v2')

for product in get_all_products():
    product_text = f"{product['name']} {product['description']}"
    embedding = model.encode(product_text)
    
    # Save to HANA vector table
    hana.insert('product_vectors', {
        'product_id': product['id'],
        'embedding': embedding.tobytes(),  # Store as binary
        'name': product['name'],
        'category': product['category']
    })

# Step 2: Extract customer need
customer_request = "We need real-time order processing for e-commerce"
customer_embedding = model.encode(customer_request)

# Step 3: Vector search in HANA
query = f"""
SELECT 
    product_id, name, category,
    COSINE_SIMILARITY('{customer_embedding}', embedding) AS similarity
FROM product_vectors
WHERE COSINE_SIMILARITY('{customer_embedding}', embedding) > 0.5
ORDER BY similarity DESC
LIMIT 10
"""

candidates = hana.execute(query)

# Step 4: Re-ranking
recommendations = []
for product in candidates:
    score = (
        0.5 * product['similarity'] +  # Vector similarity
        0.2 * industry_match_score(product) +  # Industry fit
        0.2 * product['review_score'] / 5.0 +  # Reviews
        0.1 * product['in_stock_percentage']  # Availability
    )
    recommendations.append({
        'product_id': product['product_id'],
        'name': product['name'],
        'score': score,
        'reason': [
            f"Similarity: {product['similarity']:.1%}",
            f"Industry: {product['category']}",
            f"Rating: {product['review_score']}/5"
        ]
    })

# Sort and return top 5
recommendations.sort(key=lambda x: x['score'], reverse=True)
return recommendations[:5]
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Poor embedding quality** | Use sentence-transformers model, fine-tune on domain data if needed |
| **Recommendations too similar** | Diversify output (show different use cases) |
| **Vector outdated** | Refresh embeddings monthly or when product changes |
| **Product metadata incomplete** | Use LLM to auto-generate descriptions if missing |
| **User doesn't understand recommendations** | Show reasoning (why this product?) |

---

## Success Metrics

**Matching Quality:**
- 95% recommendation accuracy (customer agrees it's relevant)
- 80% of recommended products result in sale

**Speed:**
- 5-10 seconds to generate recommendations (vs. 1 hour manual)

**Adoption:**
- 70%+ of sales team uses matcher

**Financial:**
- Increase close rate by 10% (better product matching)
- Save 50+ hours/week in sales team time

---

## Related Use Cases

- **Product Catalog Search** (Similar: Semantic search in catalog)
- **Email Agent** (Similar: NLP-based need extraction)
