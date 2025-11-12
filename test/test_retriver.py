import os
import sys
from dotenv import load_dotenv

# Make app/ importable
sys.path.append(os.path.abspath("."))

# Load OpenAI API key from .env
load_dotenv()

from app.agents.extractor import ExtractorAgent
from app.agents.retriever import RetrieverAgent

def test_vector_store_workflow():
    print("\n Running vector store test...\n")

    # Full Sample Quotation from QuickFix
    quickfix_text = """
    Quotation:
    QuickFix is currently running a promotion on their specialty fastening components. 
    They offer the 10mm steel bolt (Product ID: SB-10) at a discounted rate of $0.75 per unit for orders over 1,000 units. 
    Smaller orders are available at $0.85/unit. 
    Due to high demand, delivery is estimated at 10 business days from order confirmation. 
    Their standard payment terms are Net 45. 
    Historically, our on-time delivery rate with this supplier is 95%.
    Internal Note:
    Reliable supplier with great quality and a long record of on-time delivery.
    """

    # Full Sample Quotation from Premier Metals
    premier_text = """
    Quotation:
    Premier Metals now offers specialty fastening components. 
    We quote the 10mm steel bolt (Product ID: SB-10) at a competitive rate of $0.70 per unit for orders over 500 units. 
    We guarantee delivery within 8 calendar days. 
    We offer standard Net 60 terms.
    Internal Note:
    Had major quality issues with their stock last year. 
    The fixtures didn't meet specifications and caused production delays. 
    Be cautious with this supplier; high risk.
    """

    # Step 1: Extract offers
    extractor = ExtractorAgent()
    quickfix_offers = extractor.extract_offers(quickfix_text)
    print(f"QuickFix extracted: {len(quickfix_offers)} offers")

    premier_offers = extractor.extract_offers(premier_text)
    print(f"Premier Metals extracted: {len(premier_offers)} offers")

    all_offers = quickfix_offers + premier_offers
    print(f"\nTotal offers extracted: {len(all_offers)}\n")

    if not all_offers:
        print("No offers extracted. Skipping vector store test.")
        return

    # Step 2: Store offers in vector database
    store = RetrieverAgent()
    store.add_offers(all_offers)

    # Step 3: Perform semantic search
    query = "I need 10mm steel bolts deliverable within 9 days"
    results = store.search(query)

    print(f"\nSearch Results for: \"{query}\"\n")
    for i, offer in enumerate(results, 1):
        print(f"Match {i}:")
        print(f"Supplier: {offer.supplier}")
        print(f"Item: {offer.item}")
        print(f"Unit Price: {offer.unit_price}")
        print(f"Delivery: {offer.delivery_days} days")
        print(f"Risk Note: {offer.risk_note}")
        print("-" * 50)

if __name__ == "__main__":
    test_vector_store_workflow()
