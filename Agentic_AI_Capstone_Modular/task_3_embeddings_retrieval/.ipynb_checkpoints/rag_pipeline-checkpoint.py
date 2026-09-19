
# Mock Knowledge Base
POLICY_DOCS = {
    "gold_card_fee": "Gold Credit Card: Annual Fee is $50. Waived if spend > $10k/year. Interest: 18% APR.",
    "student_account": "Student Account: Zero balance required. No monthly fees. Max daily withdrawal: $500.",
    "loan_eligibility": "Personal Loan: Requires Credit Score > 700 and Income > $50k. Max tenure 5 years.",
    "kyc_policy": "KYC: Valid ID (Passport/License) required. Address proof needed for generic accounts."
}

class BankingRAG:
    def retrieve(self, query):
        q = query.lower()
        results = []
        if "fee" in q and "gold" in q: results.append(POLICY_DOCS["gold_card_fee"])
        if "student" in q: results.append(POLICY_DOCS["student_account"])
        if "loan" in q: results.append(POLICY_DOCS["loan_eligibility"])
        if "kyc" in q or "id" in q: results.append(POLICY_DOCS["kyc_policy"])
        
        if not results: return None
        return "\n".join(results)
