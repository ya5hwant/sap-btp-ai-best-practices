# USE CASE 3: Customer Credit Check

## Quick Summary
Automated credit decision pipeline: Extract credit documents (KYC, CSF, payment history) → Validate consistency → Apply policy rules → Generate audit report. Emphasis on compliance, explainability, traceability.

---

## Customer Pain Point

**What you'd hear:**
"Our credit evaluation is manual and inconsistent. We receive documents from customers—KYC forms, CSF, vendor comments, payment history. One analyst says 'approve', another says 'deny'. We need:
- Consistent data extraction
- Validation across documents (does everything match?)
- Automated policy application
- Compliance audit trail"

**Business Impact:**
- Process time: 1 day (need: 2 hours)
- Inconsistency: ±20% variance between analysts
- Compliance risk: Audit trails incomplete

---

## Discovery Questions

1. **"Walk me through your current credit evaluation process."**
   - (Understand current state)
2. **"How many documents per credit application?"**
   - (3? 5? 10? Affects document handling strategy)
3. **"What's acceptable accuracy for automated extraction?"**
   - (95%? 99%? Affects need for human review)
4. **"Who makes the final approval decision—algorithm or human?"**
   - (Compliance question: AI assists vs. AI decides)
5. **"What policies govern credit decisions?"**
   - (Company-specific thresholds, compliance rules)
6. **"Do you have historical credit decisions to learn from?"**
   - (Labeled data for ML, or pure rule-based?)

---

## Your Approach

### Stage 1: Document Extraction
"I'd use **SAP Document AI** for structured documents:

```
Why SAP Document AI?
✓ Pre-trained on financial documents (KYC, CSF forms)
✓ High accuracy (95%+) on standard forms
✓ Confidence scores (I know which extractions are risky)
✓ Returns structured JSON with field-level confidence

For less structured docs:
- Use LLM vision for document understanding
- Fall back to manual OCR + extraction if needed
```

**What gets extracted:**
- KYC: Company name, RFC, address, director names, registration date
- CSF (Consolidated Statement of Financial): Revenue, expenses, net income, assets
- Vendor comments: Payment history, reliability, issues
- Payment history: Days late, payment rate"

### Stage 2: Validation (Cross-Document Consistency)
"This is critical—inconsistencies signal either fraud or poor data quality:

```
Validation checks:
✓ RFC number matches across KYC and CSF
✓ Company names match (spelling variations acceptable)
✓ Addresses consistent (HQ vs. operational)
✓ Director names appear in vendor history (trust signal)
✓ Dates make sense (registration before CSF, before now)
✓ Financial data plausible (revenue > expenses)
```

**Validation score:**
- 100%: All checks passed → proceed to scoring
- 70-100%: Most checks passed → flag for review
- <70%: Major inconsistencies → request new documents or deny"

### Stage 3: Credit Policy Engine
"Pure rule-based (no ML) because:

```
Why rules, not ML?
✓ Compliance requirement: Need explainability per decision
✓ Policy changes frequently: Easy to update rules
✓ Audit trail: Clear reasoning for every decision
✗ ML: Black-box, hard to explain to regulators
```

**Sample policy:**
```
IF CAL_Score >= 80:
  Recommendation = APPROVE
  Limit = UNLIMITED
  
ELIF CAL_Score >= 60 AND Payment_Score >= 75:
  Recommendation = APPROVE_WITH_CONDITIONS
  Limit = €50,000
  Conditions: Monthly reporting required
  
ELIF CAL_Score >= 40 AND Director_Approval_Available:
  Recommendation = ESCALATE_TO_DIRECTOR
  
ELSE:
  Recommendation = DENY
```"

### Stage 4: Scoring Layers
"I'd calculate multiple scores to feed the rules:

```
CAL Score (80-point scale):
  - 20pts: Company age (>10yrs: 20pts, <3yrs: 5pts)
  - 30pts: Financial health (revenue/expense ratio)
  - 20pts: Liquidity (cash position)
  - 10pts: Industry risk (some industries higher risk)

C3M Score (90-day performance):
  - 50pts: On-time payment rate
  - 25pts: Average payment delay
  - 25pts: Order fulfillment rate

Risk Score:
  - Composite of CAL + C3M + industry + geography
```"

### Stage 5: Reporting & Audit
"Every credit decision produces:

```
Output artifacts:
1. Executive Summary (2 pages)
   - Company name, scores, recommendation
   - Key factors driving decision
   - Next steps

2. Detailed Analysis (5+ pages)
   - All extracted data with confidence
   - Validation checks results
   - Policy rules applied
   - Comparable precedents

3. Audit Trail
   - Timestamp, user approver
   - Any manual overrides with reasoning
   - Document version numbers
   - Extraction confidence scores
```"

---

## Key Architectural Decisions

### Decision 1: Phased Approach (Extract → Validate → Score → Report)

**What you'd say:**
"I break this into stages because each stage can be tested independently:

1. **Extract**: Did we get the data right?
2. **Validate**: Is the data consistent?
3. **Score**: Is the score fair?
4. **Report**: Is the recommendation clear?

If validation fails, we know it's not an extraction problem. This modular design makes debugging easier and builds confidence through stages."

### Decision 2: Human Review Workflow

**What you'd say:**
"The system doesn't decide—it **recommends**. We implement three workflows:

```
High Confidence (>95% extraction + validation):
  → System recommends APPROVE/DENY
  → Analyst clicks approve (mostly automated)
  
Medium Confidence (70-95%):
  → System shows reasoning
  → Analyst reviews, makes decision
  
Low Confidence (<70%):
  → Request additional documents
  → OR escalate to manual review
```

This keeps humans in the loop while automating routine cases."

### Decision 3: Multi-Currency & Regional Policies

**What you'd say:**
"Different regions have different thresholds:
- Mexico: €100k base limit, 50% CAL required
- USA: €250k base limit, 60% CAL required
- EU: €500k base limit, 70% CAL required

I'd implement:
- Store limits in policy table (easy to update)
- Support region-specific policy versions
- Version control all policies (Git-based)
- A/B test new policies on historical data before deploying"

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Document extraction fails** | Pre-process PDFs (contrast enhance, deskew), fall back to manual OCR |
| **Validation rejects legitimate applications** | Flag for review instead of auto-reject, show what failed |
| **Policy too strict/lenient** | A/B test on historical data, quarterly calibration meetings |
| **Director override not tracked** | Log all overrides with reasoning, timestamp, approval |
| **Regulatory audit fails** | Implement complete audit trail: extractions + validation + policy application + approver |
| **Extraction confidence too low** | Accept lower confidence for trusted vendors, but note in audit trail |

---

## Success Metrics

**Speed:**
- Reduce from 1 day to 2 hours (7x faster)
- Automate 60% of decisions (no human needed)

**Consistency:**
- Approval rate variance <5% across analysts (vs. current ±20%)
- Policy adherence: 100% (vs. current 80%)

**Accuracy:**
- 95%+ match with manual extractions
- Default rate of approved customers <2% (vs. current 3%)

**Compliance:**
- 100% audit trail completeness
- Zero regulatory findings on credit decisions
- Full traceability: decision → documents → policy rules

**Financial:**
- Cost per decision: €2 (vs. €10 manual)
- 40-50% FTE savings in credit team

---

## Interview Tips

**If asked "Shouldn't we use ML to predict default risk?"**
- Answer: "Credit decisions are compliance-driven, not optimization-driven. We need to explain every decision to regulators. ML would be a black-box. However, we could use ML to **optimize** policy thresholds based on historical default rates. That's a secondary optimization after the primary rule-based system is working."

**If asked "How do you handle data quality issues?"**
- Answer: "Three-tier approach: 
  1) Validation layer catches inconsistencies
  2) Low-confidence flags trigger human review
  3) If extraction fails, request new documents from customer
  This prevents garbage in → garbage out."

**If asked "What about fraud?"**
- Answer: "Credit evaluation focuses on creditworthiness. Fraud detection is separate:
  - Cross-check documents with government registries (RFC, business license)
  - Flag unusual patterns (director changes, HQ changes)
  - Vendor comments as fraud signal
  - Would use anomaly detection model if historical fraud data available."

---

## Related Use Cases

- **Purchase Order Extractor** (Similar: Document extraction + validation)
- **AI PDF Information Extraction** (Similar: Document understanding, different goal)
