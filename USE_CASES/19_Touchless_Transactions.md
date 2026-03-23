# USE CASE 19: Touchless Transactions (GR & Invoice Workflows)

## Quick Summary
Automated 3-way-match (PO → GR → Invoice) processing using rule-based classification. Classify discrepancies into 7 scenarios. Auto-approve when within tolerance. Escalate exceptions.

---

## Customer Pain Complaint

**What you'd hear:**
"Our AP team spends days on 3-way matching. Goods receipt doesn't match PO, invoice has different amounts. 80% of matches are within tolerance but require manual review. We need automated approval for routine cases."

**Business Impact:**
- Current processing: 30 min per invoice
- Manual review rate: 80%
- Invoices/month: 5000
- Opportunity: Save 200+ hours/month

---

## Your Approach

### Phase 1: Data Collection
"Gather PO → GR → Invoice data"

### Phase 2: Comparison & Calculation
"Compare quantities and amounts:

```
PO quantity: 100 units @ €50 = €5000
GR quantity: 100 units
Invoice amount: €5000

Differences:
- Quantity variance: 0%
- Amount variance: 0%
- Price variance: €50 vs. invoice price
```"

### Phase 3: Rule-Based Classification
"Classify into scenarios:

```
SCENARIO 1: Perfect match
  PO Qty = GR Qty = Invoice Qty
  PO Amt = Invoice Amt
  → AUTO-APPROVE

SCENARIO 2: Within tolerance
  Qty variance ≤ 2%
  Amt variance ≤ 5%
  → AUTO-APPROVE (after review)

SCENARIO 3: Price variance only
  Qty matches, price higher than PO
  → FLAG for negotiation (renegotiate with vendor)

SCENARIO 4: Quantity variance
  GR qty > PO qty (overbilled)
  → REJECT invoice for excess quantity

SCENARIO 5: Missing GR
  Invoice received, no goods receipt
  → WAIT for GR (hold invoice)

SCENARIO 6: Major discrepancy
  Variance > 10%
  → ESCALATE to AP manager

SCENARIO 7: Duplicate invoice
  Same invoice number already processed
  → REJECT (fraud/error)
```"

### Phase 4: Action & Escalation
"Route by scenario:

```
Scenarios 1-2: Auto-approve (or auto-hold waiting for GR)
Scenarios 3-5: Route to appropriate team (negotiation, operations, etc.)
Scenario 6-7: Escalate to manager
```"

### Phase 5: Audit Trail
"Log every decision:

```
- Scenario classification
- Amounts compared
- Decision (approve/hold/reject)
- Approver + timestamp
```"

---

## Key Architectural Decisions

### Decision 1: Rules, Not ML

**What you'd say:**
"This is rule-based (not ML) because:

✓ Business logic is deterministic (tolerance thresholds)
✓ Compliance requires clear rules
✓ Easy to explain to auditors
✗ No training data needed
✗ Easy to maintain and update

ML would be overkill—rules are simpler and more transparent."

### Decision 2: 7 Scenarios

**Why exactly 7?**

```
1: Perfect match (rare, but best)
2: Within tolerance (most common, auto-approve)
3: Price variance (negotiation needed)
4: Qty variance (operations issue)
5: Missing GR (timing issue)
6: Major discrepancy (escalate)
7: Duplicate (fraud/error check)

These cover 99% of real scenarios.
Edge cases go to escalation.
```

---

## Implementation

```python
def classify_invoice_match(po, gr, invoice):
    """Classify into one of 7 scenarios"""
    
    # Calculate variances
    qty_variance_pct = abs(gr['qty'] - po['qty']) / po['qty'] * 100
    amt_variance_pct = abs(invoice['amt'] - po['amt']) / po['amt'] * 100
    
    # Scenario classification
    if gr is None:
        return 'SCENARIO_5_MISSING_GR'
    
    elif po['qty'] == gr['qty'] == invoice['qty'] and po['amt'] == invoice['amt']:
        return 'SCENARIO_1_PERFECT_MATCH'
    
    elif qty_variance_pct <= 2 and amt_variance_pct <= 5:
        return 'SCENARIO_2_WITHIN_TOLERANCE'
    
    elif gr['qty'] == po['qty'] and invoice['price'] > po['price']:
        return 'SCENARIO_3_PRICE_VARIANCE'
    
    elif gr['qty'] != po['qty']:
        return 'SCENARIO_4_QUANTITY_VARIANCE'
    
    elif qty_variance_pct > 10 or amt_variance_pct > 10:
        return 'SCENARIO_6_MAJOR_DISCREPANCY'
    
    elif is_duplicate(invoice):
        return 'SCENARIO_7_DUPLICATE'
    
    else:
        return 'SCENARIO_6_MAJOR_DISCREPANCY'  # Catch-all


def route_invoice(scenario, invoice):
    """Route invoice to appropriate team"""
    
    routes = {
        'SCENARIO_1_PERFECT_MATCH': ('AUTO_APPROVE', None),
        'SCENARIO_2_WITHIN_TOLERANCE': ('AUTO_APPROVE_HOLD', 'ap_team'),
        'SCENARIO_3_PRICE_VARIANCE': ('ROUTE_TO_NEGOTIATION', 'procurement'),
        'SCENARIO_4_QUANTITY_VARIANCE': ('ROUTE_TO_OPERATIONS', 'receiving'),
        'SCENARIO_5_MISSING_GR': ('WAIT_FOR_GR', None),
        'SCENARIO_6_MAJOR_DISCREPANCY': ('ESCALATE', 'ap_manager'),
        'SCENARIO_7_DUPLICATE': ('REJECT', None)
    }
    
    action, team = routes.get(scenario)
    
    # Create task
    task = {
        'invoice_id': invoice['id'],
        'scenario': scenario,
        'action': action,
        'assigned_to': team,
        'timestamp': now(),
        'audit_trail': [scenario]
    }
    
    return task
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Rule too strict, holds legitimate invoices** | Periodic calibration, track hold time |
| **Price variance undetected** | Compare PO unit price vs. invoice price |
| **Duplicate detection fails** | Hash invoice (number + vendor + amount) |
| **Escalation queue grows** | Monitor queue depth, adjust thresholds |

---

## Success Metrics

- Auto-approval rate: 60%+ (vs. current 0%)
- Processing time: <5 minutes (vs. 30 min)
- Invoice accuracy: >99%
- Save 150+ hours/month

---

## Related Use Cases

- **Purchase Order Extractor** (Upstream: PO creation)
- **Anomaly Detection** (Similar: Variance detection, different domain)
