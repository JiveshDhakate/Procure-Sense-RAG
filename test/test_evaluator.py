import sys
import os
sys.path.append(os.path.abspath(".")) 
from app.agents.evaluator import EvaluatorAgent

def print_separator():
    print("=" * 60)

def test_urgent_query_prefers_faster():
    print_separator()
    print("TEST: Urgent query → Should prefer faster delivery")
    agent = EvaluatorAgent()

    query = "Urgent order for 10mm bolts within 3 days"
    offers = [
        {"supplier": "A", "unit_price": 0.6, "delivery_days": 10, "min_quantity": 100, "risk_note": ""},
        {"supplier": "B", "unit_price": 0.8, "delivery_days": 2, "min_quantity": 100, "risk_note": ""}
    ]

    result = agent.evaluate(query, offers)
    print(f"Query: {query}")
    print(f"Chosen Supplier: {result['supplier']}")
    print(f"Reason: {result['evaluation_reason']}")

def test_non_urgent_query_balances_price_delivery():
    print_separator()
    print("TEST: Non-urgent query → Should balance price vs delivery")
    agent = EvaluatorAgent()

    query = "Order 10mm bolts for next month"
    offers = [
        {"supplier": "A", "unit_price": 0.6, "delivery_days": 10, "min_quantity": 100, "risk_note": ""},
        {"supplier": "B", "unit_price": 0.8, "delivery_days": 5, "min_quantity": 100, "risk_note": ""}
    ]

    result = agent.evaluate(query, offers)
    print(f"Query: {query}")
    print(f"Chosen Supplier: {result['supplier']}")
    print(f"Reason: {result['evaluation_reason']}")

def test_missing_fields_penalty():
    print_separator()
    print("TEST: Offer with missing delivery_days should be penalized")
    agent = EvaluatorAgent()

    query = "10mm bolts, not urgent"
    offers = [
        {"supplier": "A", "unit_price": 0.6, "min_quantity": 100, "risk_note": ""},  # missing delivery
        {"supplier": "B", "unit_price": 0.8, "delivery_days": 5, "min_quantity": 100, "risk_note": ""}
    ]

    result = agent.evaluate(query, offers)
    print(f"Query: {query}")
    print(f"Chosen Supplier: {result['supplier']}")
    print(f"Reason: {result['evaluation_reason']}")

def test_risk_penalty_applied():
    print_separator()
    print("TEST: High-risk suppliers should be penalized")
    agent = EvaluatorAgent()

    query = "Regular order"
    offers = [
        {"supplier": "A", "unit_price": 0.6, "delivery_days": 10, "min_quantity": 100, "risk_note": "High risk supplier"},
        {"supplier": "B", "unit_price": 0.8, "delivery_days": 5, "min_quantity": 100, "risk_note": ""}
    ]

    result = agent.evaluate(query, offers)
    print(f"Query: {query}")
    print(f"Chosen Supplier: {result['supplier']}")
    print(f"Reason: {result['evaluation_reason']}")

def test_no_offers():
    print_separator()
    print("TEST: No offers passed → should return None")
    agent = EvaluatorAgent()

    query = "Order for 10mm bolts"
    offers = []

    result = agent.evaluate(query, offers)
    print(f"Query: {query}")
    print("Chosen Supplier: None" if result is None else f"Chosen: {result['supplier']}")

# Run all tests manually
if __name__ == "__main__":
    test_urgent_query_prefers_faster()
    test_non_urgent_query_balances_price_delivery()
    test_missing_fields_penalty()
    test_risk_penalty_applied()
    test_no_offers()
