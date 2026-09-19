
class BankingTools:
    def get_balance(self, user_id):
        # Read-only
        if user_id == "user_123": return {"balance": 5000, "currency": "USD"}
        return None

    def check_eligibility(self, user_id, product_type):
        if product_type.lower() == "gold card":
            return {"eligible": True, "reason": "Income > limit"}
        if product_type.lower() == "platinum card":
            return {"eligible": False, "reason": "Credit Score < 750"}
        return {"error": "Unknown product"}
    
    def transfer_money(self, user_id, amount):
        raise PermissionError("Tool Blocked: Transactions not allowed.")
