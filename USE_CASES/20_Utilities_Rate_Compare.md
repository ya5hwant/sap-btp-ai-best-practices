# USE CASE 20: Utilities Rate Compare & Export

## Quick Summary
Compare utility tariffs (electricity, gas, water) across suppliers/time periods. Analyze usage patterns, project costs, recommend optimal plans. Export reports.

---

## Customer Pain Point

**What you'd hear:**
"We have utility contracts from multiple suppliers. Understanding and comparing rates is complex. We want to optimize our utility spending and find better deals."

**Business Impact:**
- Current comparison: Manual, quarterly reviews
- Potential savings: 10-15% on utility spend
- Annual utility spend: €5M
- Opportunity: €500k+/year

---

## Your Approach

### Phase 1: Data Collection
"Upload utility bills/tariff documents:

```
- Supplier name, tariff name
- Rate structure (fixed + variable)
- Usage periods (peak, off-peak)
- Surcharges, taxes, discounts
```"

### Phase 2: Rate Parsing
"Extract rate from complex documents:

```
'Fixed charge: €50/month
Variable: €0.15/kWh for 0-500 kWh
         €0.12/kWh for 501-2000 kWh
         €0.10/kWh for >2000 kWh'

Parsed:
{
  'fixed': 50,
  'tiers': [
    {'start': 0, 'end': 500, 'rate': 0.15},
    {'start': 501, 'end': 2000, 'rate': 0.12},
    {'start': 2001, 'end': null, 'rate': 0.10}
  ]
}
```"

### Phase 3: Usage Analysis
"Analyze historical usage:

```
- Average monthly usage
- Peak vs. off-peak usage
- Seasonal patterns
- Trend over time
```"

### Phase 4: Cost Projection
"Project costs under different tariffs:

```
Historical usage: 1200 kWh/month
Tariff A: €50 fixed + €0.15/kWh = €50 + €180 = €230/month
Tariff B: €30 fixed + €0.18/kWh = €30 + €216 = €246/month
Tariff C: €0 fixed + €0.16/kWh = €0 + €192 = €192/month

Recommendation: Tariff C saves €38/month = €456/year
```"

### Phase 5: Reporting
"Generate comparison reports:

```
- Side-by-side tariff comparison
- Annual cost projection
- Savings opportunity
- Switch recommendation
```"

---

## Implementation

```python
import streamlit as st
import pandas as pd

# Upload tariff documents
uploaded_files = st.file_uploader("Upload tariff docs", accept_multiple_files=True)

tariffs = []
for file in uploaded_files:
    # Extract rate from document
    rate_data = extract_tariff_rate(file)
    tariffs.append(rate_data)

# Historical usage
usage_df = st.file_uploader("Upload usage history (CSV)", type=['csv'])
usage_data = pd.read_csv(usage_df)

# Project costs
def project_cost(monthly_usage, tariff):
    fixed = tariff['fixed']
    variable_cost = 0
    
    for tier in tariff['tiers']:
        usage_in_tier = min(monthly_usage - sum_of_prior_tiers, tier['end'] - tier['start'])
        variable_cost += usage_in_tier * tier['rate']
    
    return fixed + variable_cost

# Compare
comparison = []
avg_usage = usage_data['usage'].mean()

for tariff in tariffs:
    annual_cost = project_cost(avg_usage, tariff) * 12
    comparison.append({
        'Supplier': tariff['supplier'],
        'Annual Cost': annual_cost,
        'Savings vs. Current': annual_cost - comparison[0]['Annual Cost']
    })

# Display
st.write("Tariff Comparison")
st.dataframe(comparison)

# Export
st.download_button("Download report", comparison.to_csv())
```

---

## Success Metrics

- Identify 10-15% savings opportunity
- Reduce tariff analysis time by 80%
- Automated bill validation

---

## Related Use Cases

- **Utilities Tariff Mapping** (Similar: Tariff processing)
