# USE CASE 12: Intelligent Negotiation Assistant (Procurement)

## Quick Summary
AI-assisted procurement negotiation: Analyzes supplier proposals, benchmarks against market prices, recommends negotiation tactics, generates counter-offers. Combines data analysis + LLM reasoning.

---

## Customer Pain Point

**What you'd hear:**
"When we negotiate with suppliers, we often don't have enough context. Is this price good? What did we pay last year? What's market rate? We need data-driven negotiation support."

**Business Impact:**
- Current savings rate: 5-10% on negotiations
- Target savings rate: 15-20%
- Procurement spend: €100M/year
- Opportunity: €5-10M additional savings

---

## Discovery Questions

1. **"Do you have historical supplier pricing?"** (Yes = can benchmark)
2. **"What's the negotiation timeline?"** (Days? Weeks?)
3. **"Are there compliance constraints?"** (Fixed price tiers? Volume discounts?)
4. **"What suppliers is this for?"** (Single vs. multiple)

---

## Your Approach

### Phase 1: Collect Proposal Data
"Supplier submits:
- Item list, quantities, prices
- Terms (payment, delivery, warranty)
- Volume discounts"

### Phase 2: Benchmark Analysis
"Compare to:
- Historical pricing from this supplier
- Pricing from competitors (market data)
- Industry benchmarks

Example:
```
This supplier quotes: €50/unit
- Last year from them: €48/unit (price increased 4%)
- Competitor average: €45/unit
- Market range: €40-55/unit

Insight: 'Slightly above market, but aligned with their history'
```"

### Phase 3: Negotiation Recommendations
"Generate tactics:

```
LLM prompt:
'We have a supplier quote.
Historical price: €48
Current quote: €50
Market average: €45

Recommend negotiation tactics:
- Immediate action (before counteroffering)?
- Target price for counteroffer?
- Best negotiation angle?
- Walk-away threshold?'

Output:
- 'Market average is €45, we should counteroffer €43'
- 'Their volume discount is weak—press them there'
- 'Payment terms: could we get better?'
- 'Walk-away if they don't go below €47'
```"

### Phase 4: Counter-Offer Generation
"Generate structured counter-offer:

```
Template:
'We appreciate your proposal for [ITEMS].
After comparing with market benchmarks,
we recommend the following adjustments:

Unit price: €50 → €45 (aligned with market)
Volume discount: Current [%] → [RECOMMENDED %]
Payment terms: [PROPOSED]
Delivery: [PROPOSED]

We believe this is fair and competitive.
Please review and let us know your thoughts.'
```"

---

## Key Architectural Decisions

### Decision 1: Data-Driven First

**What you'd say:**
"Always start with data:
1. Historical pricing (what did we pay?)
2. Market benchmarks (what's competitive?)
3. Terms analysis (payment, delivery)

Then use LLM for:
- Recommendation narrative
- Negotiation tactics
- Counter-offer wording

Why? Data grounds LLM's reasoning."

### Decision 2: Negotiator Tools, Not Auto-Negotiation

**What you'd say:**
"This is decision support, not automation:
- Procurement person still negotiates
- AI provides data + recommendations
- Human makes final decision

Why not auto-negotiate?
- Relationships matter
- Compliance requirements
- Business strategy"

---

## Implementation Walk-Through

```python
def analyze_supplier_proposal(proposal, supplier_id):
    # Step 1: Extract proposal data
    items = extract_line_items(proposal)
    terms = extract_terms(proposal)
    
    # Step 2: Benchmark
    historical = get_supplier_history(supplier_id)
    market_data = get_market_benchmarks(items)
    
    # Step 3: LLM recommendations
    recommendations = llm.generate(f'''
        Supplier {supplier_id} proposal analysis:
        
        Historical price: €{historical['avg_price']}
        Quoted price: €{proposal['avg_price']}
        Market average: €{market_data['avg']}
        
        Recommend:
        1. Price target for counteroffer
        2. Negotiation angles
        3. Walk-away threshold
        4. Terms to push
    ''')
    
    # Step 4: Generate counter-offer
    counter_offer = generate_counter_offer(
        proposal, 
        recommendations,
        market_data
    )
    
    return {
        'benchmark_analysis': market_data,
        'recommendations': recommendations,
        'counter_offer': counter_offer,
        'estimated_savings': calculate_savings(proposal, counter_offer)
    }
```

---

## Success Metrics

- Increase savings rate from 10% to 18% (8% improvement)
- €100M spend × 8% = €8M additional savings
- Negotiation time: Reduced by 20%

---

## Related Use Cases

- **Vendor Selection Optimization** (Similar: Supplier analysis, different goal)
