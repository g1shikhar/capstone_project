
class AdaptiveAgent:
    def __init__(self):
        self.mode = "Standard" # or Adaptive

    def process(self, query):
        if self.mode == "Adaptive" and "loan" in query.lower() and "personal" not in query.lower():
            return "[CLARIFY] Could you specify the type of loan?"
        if "loan" in query.lower():
            return "We offer loans."
        return "How can I help?"
