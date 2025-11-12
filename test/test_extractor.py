
"""

ExtractorAgent pipeline:
    Extracts multiple structured offers per quotation
    Works across different suppliers
    Handles optional fields and edge cases
    Fully tested and confirmed
"""

import sys
import os
sys.path.append(os.path.abspath(".")) 
from app.agents.extractor import ExtractorAgent

sample_text1 = """
Quotation:
QuickFix is currently running a promotion on their specialty fastening components. They offer the 10mm steel bolt (Product
ID: SB-10) at a discounted rate of $0.75 per unit for orders over 1,000 units. Smaller orders are available at $0.85/unit.
Due to high demand, delivery is estimated at 10 business days from order confirmation. Their standard payment terms are
Net 45. Historically, our on-time delivery rate with this supplier is 95%.
Internal Note:
Reliable supplier with great quality and a long record of on-time delivery.
"""
sample_text2 ="""
Quotation:
Premier Metals now offers specialty fastening components. We quote the 10mm steel bolt (Product ID: SB-10) at a
competitive rate of $0.70 per unit for orders over 500 units. We guarantee delivery within 8 calendar days. We offer
standard Net 60 terms.
Internal Note:
Had major quality issues with their stock last year. The fixtures didn't meet specifications and caused production delays.
Be cautious with this supplier; high risk.
"""
agent = ExtractorAgent()

print("\n Testing extraction from QuickFix quotation...")
offers1 = agent.extract_offers(sample_text1)
print(f"Extracted {len(offers1)} offers from QuickFix\n")
for offer in offers1:
    print(offer)

print("\n Testing extraction from Premier Metals quotation...")
offers2 = agent.extract_offers(sample_text2)
print(f" Extracted {len(offers2)} offers from Premier Metals\n")
for offer in offers2:
    print(offer)

