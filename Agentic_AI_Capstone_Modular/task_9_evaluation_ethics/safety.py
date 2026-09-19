
class SafetyAgent:
    def __init__(self):
        self.refusals = 0
        self.escalations = 0
        self.adaptation_mode = "Standard" # Adaptation Mechanism
    
    def process(self, query):
        q = query.lower()
        
        # 9.1 Refusal Logic
        if "transfer" in q or "pay" in q:
            self.refusals += 1
            return "[REFUSAL] I cannot perform transactions. Policy #12."
        
        # 9.2 Escalation Logic
        if "fraud" in q or "human" in q:
            self.escalations += 1
            return "[ESCALATE] Transferring you to a Human Agent."
        
        # 8.2 Adaptation (Clarification Policy)
        if self.adaptation_mode == "Adaptive" and "loan" in q and "personal" not in q:
             return "[CLARIFY] Could you specify the type of loan (Personal, Home, Auto)?"
             
        if "loan" in q:
             return "We offer loans."
             
        return "How can I help?"
