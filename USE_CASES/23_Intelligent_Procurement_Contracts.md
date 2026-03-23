# USE CASE 23: Intelligent Procurement Assistant with Contracts

## Quick Summary
Contract-aware procurement: Extract and validate contracts, link to commodities, track contract terms (pricing, renewals), auto-flag when contract terms violated in orders.

---

## Customer Pain Point

**What you'd hear:**
"We have contracts with suppliers with specific terms—pricing, volume discounts, exclusions. When orders come in, we don't consistently apply the contract terms. We need to enforce contracts automatically."

**Business Impact:**
- Current contract compliance: 70%
- Lost revenue from missed discounts: €500k/year
- Target: 95% compliance

---

## Your Approach

### Phase 1: Contract Extraction & Storage
"Extract from contract documents:

```
- Supplier name, contract ID
- Contract period (start, end, renewal)
- Pricing: Base price, volume discounts, exclusions
- Terms: Payment, delivery, warranties
- Special conditions
```"

### Phase 2: Contract Master Data
"Build HANA table:

```
contract_id | supplier | commodity | unit_price | volume_threshold | discount
-----------+-----------+-----------+----------+------------------+----------
C001      | Vendor A  | Steel     | 100      | 1000            | 5%
C001      | Vendor A  | Steel     | 95       | 5000            | 10%
```"

### Phase 3: Order Processing with Contract Validation
"When order created:

```
1. Lookup supplier contract
2. Check if item in contract
3. Verify pricing aligns with contract
4. Apply discounts automatically
5. Flag if order violates contract terms
```"

### Phase 4: Contract Term Tracking
"Monitor expiration:

```
Contract C001 expires: 2024-06-30 (90 days away)
Alert: 'Contract with Vendor A expiring soon. Start renegotiation.'
```"

### Phase 5: Contract Compliance Reporting
"Report on compliance:

```
- % orders using contract pricing
- Actual discount taken vs. eligible
- Cost variance (should have saved more)
```"

---

## Implementation

```python
def validate_order_against_contract(order, supplier_id):
    # Look up contract
    contract = get_contract(supplier_id)
    
    if not contract:
        return {'status': 'NO_CONTRACT', 'warning': 'No contract found'}
    
    compliance = {'status': 'COMPLIANT', 'adjustments': []}
    
    for item in order['line_items']:
        # Check if item in contract
        contract_line = contract['line_items'].get(item['product_id'])
        
        if not contract_line:
            compliance['adjustments'].append({
                'product': item['product_id'],
                'issue': 'NOT_IN_CONTRACT',
                'action': 'FLAG for approval'
            })
            continue
        
        # Check pricing
        contract_price = contract_line['unit_price']
        order_price = item['unit_price']
        
        if order_price > contract_price:
            compliance['adjustments'].append({
                'product': item['product_id'],
                'issue': 'OVERPRICE',
                'order_price': order_price,
                'contract_price': contract_price,
                'action': 'Apply contract price'
            })
            item['unit_price'] = contract_price  # Auto-correct
        
        # Check volume discounts
        volume = item['quantity']
        for tier in contract_line['volume_tiers']:
            if volume >= tier['threshold'] and tier['discount'] > 0:
                compliance['adjustments'].append({
                    'product': item['product_id'],
                    'discount_applied': tier['discount']
                })
                item['unit_price'] *= (1 - tier['discount'])
    
    return compliance
```

---

## Success Metrics

- Contract compliance: 95%+
- Cost savings from discount compliance: €500k+/year
- Contract administration time: Reduced 60%

---

## Related Use Cases

- **Intelligent Procurement Assistant** (Similar: Commodity extraction)
- **Purchase Order Extractor** (Similar: Contract validation)
