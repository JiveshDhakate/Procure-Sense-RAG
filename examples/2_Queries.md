# Supplier Query–Answer Set (Robust Evaluation)

This file contains **10 robust test cases** for the Spear RAG system, including valid matches and "No Offer" scenarios.  
Use them to validate retrieval accuracy, multi-criteria evaluation, and LLM summarization consistency.

---

### Query 1

Find the most cost-effective supplier for 6mm hex nuts who can deliver within a week.

**Recommended Supplier**  
Apex Fasteners

**Reasoning**  
The chosen supplier for 6mm hex nuts is Apex Fasteners, offering the product at a unit price of $0.25 for orders of 2,000 units or more. They guarantee delivery within 6 business days and provide Net 30 payment terms. Apex Fasteners is noted for being a highly reliable supplier with consistent quality control, although there is a minor risk of occasional shipping slowdowns during peak seasons. Additionally, they have implemented automated sorting to significantly reduce packing errors.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #2  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #3  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

---

### Query 2

I need a dependable supplier for M12 steel washers that provides technical support.

**Recommended Supplier**  
IronClad Components

**Reasoning**  
The evaluator has selected IronClad Components as the supplier for M12 steel washers, specifically product ID SW-12. The unit price is $0.40 for orders of 1,000 units or more, with a delivery time of 7 business days and payment terms of Net 45. IronClad Components is noted as a reliable vendor that provides strong after-sales support and on-site technical assistance for product fitment on large assembly lines, despite being slightly more expensive. This combination of reliability and support contributes to a low operational risk.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #2  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #3  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

---

### Query 3

I need 10mm steel bolts for a large order (over 1,000 units). Which supplier should I use?

**Recommended Supplier**  
QuickFix Industries

**Reasoning**  
The chosen supplier for the 10mm steel bolts is QuickFix Industries. They offer the product (Product ID: SB-10) at a unit price of $0.75 for orders of 1,000 units or more, with a delivery time of 10 business days. Their payment terms are Net 45. QuickFix Industries is noted as a reliable supplier with a strong history of quality and a 95% on-time delivery rate.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #2  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #3  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```
---

### Query 4

Who offers the shortest delivery time with medium or lower risk?

**Recommended Supplier**  
QuickFix Industries

**Reasoning**  
The chosen supplier is QuickFix Industries, which offers the 10mm steel bolt (Product ID: SB-10) at a unit price of $0.75 for orders of 1,000 units or more. They have a delivery time of 10 business days and standard payment terms of Net 45. QuickFix is noted as a reliable supplier with a strong track record of quality and a 95% on-time delivery rate, making them a suitable choice for meeting the requirement of the shortest delivery time with medium or lower risk.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #2  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #3  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #4  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

---

### Query 5

Which supplier has a history of poor product quality and should be avoided?

**Recommended Supplier**  
Premier Metals

**Reasoning**  
The evaluator has identified Premier Metals as a supplier for the 10mm steel bolt (Product ID: SB-10) at a unit price of $0.70 for a minimum order of 500 units, with a delivery time of 8 days and payment terms of Net 60. However, there is a significant risk associated with this supplier due to a history of major quality issues last year, where their products did not meet specifications and caused production delays. Caution is advised when considering this supplier due to the high risk of poor product quality.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #2  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #3  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

---

### Query 6

Recommend a supplier for bulk orders above 5,000 units offering durable products.

**Recommended Supplier**  
QuickFix Industries

**Reasoning**  
The evaluator has selected QuickFix Industries as the recommended supplier for bulk orders above 5,000 units. They offer a durable product, specifically the 10mm steel bolt (Product ID: SB-10), at a unit price of $0.75 for orders exceeding 1,000 units. QuickFix Industries has a reliable reputation, with a long history of on-time delivery, achieving a 95% on-time delivery rate. The estimated delivery time is 10 business days, and their payment terms are Net 45.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #2  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #3  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

---

### Query 7

I need 2mm steel bolts for a large order (over 1,000 units). Which supplier should I use?

**Recommended Supplier**  
No Offer

**Reasoning**  
No supplier matched the required product specifications or size. Therefore, no recommendation can be made from the evaluated offers.

**Offers Evaluated**  
Offer #1  
```
{
"supplier":"Premier Metals",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.7,
"delivery_days":8,
"risk_assessment":"High Risk (Major quality issues last year, be cautious)"
}
```
Offer #2  
```
{
"supplier":"QuickFix Industries",
"item":"10mm steel bolt (SB-10)",
"unit_price":0.75,
"delivery_days":10,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #3  
```
{
"supplier":"IronClad Components",
"item":"M12 steel washers (SW-12)",
"unit_price":0.4,
"delivery_days":7,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #4  
```
{
"supplier":"Apex Fasteners",
"item":"6mm hex nuts (HN-6)",
"unit_price":0.25,
"delivery_days":6,
"risk_assessment":"Low Risk (Reliable supplier, consistent on-time delivery)"
}
```
Offer #5  
```
{
"supplier":"Metro Rivet Works",
"item":"4mm aluminum pop rivets (AR-4)",
"unit_price":0.15,
"delivery_days":10,
"risk_assessment":"Unknown Risk (Insufficient data)"
}
```

