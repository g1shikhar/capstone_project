
class PromptExperiment:
    def __init__(self):
        self.prompts = {
            "Naive": "Answer the question directly.",
            "CoT": "Think step-by-step then answer.",
            "Clarify": "If ambiguous, ask for clarification."
        }
    
    def test_prompts(self, query):
        print(f"Query: {query}")
        for name, p in self.prompts.items():
            print(f"[\nPrompt: {name}]\nInstruction: {p}\nOutput: (Simulated response based on {name} strategy...)")

if __name__ == "__main__":
    exp = PromptExperiment()
    exp.test_prompts("I want to close my account")
