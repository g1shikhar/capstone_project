
class BankingBaseline:
    """Rule-based Banking Assistant (Mock)."""
    
    def classify(self, query):
        q = query.lower()
        if 'transfer' in q or 'pay' in q: return 'transfer'
        if 'loan' in q or 'card' in q: return 'product'
        if 'balance' in q: return 'account'
        return 'unknown'

    def handle(self, query):
        cat = self.classify(query)
        if cat == 'transfer':
            return "To make a transfer, go to the 'Payments' tab and select 'Transfer'."
        if cat == 'product':
            # Hardcoded product info without eligibility checks
            return "We offer Personal Loans (12%) and Credit Cards. Apply at branch."
        if cat == 'account':
            return "Please log in to view your balance."
        return "I can help with Transfers, Products, and Accounts."

if __name__ == "__main__":
    agent = BankingBaseline()
    print("Test: 'I want a loan' ->", agent.handle("I want a loan"))
