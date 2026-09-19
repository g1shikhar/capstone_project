
from task_3_embeddings_retrieval.rag_pipeline import BankingRAG
from task_4_tool_using_agent.tools import BankingTools

class BankingAgent:
    def __init__(self):
        self.rag = BankingRAG()
        self.tools = BankingTools()
        self.memory = []
        
    def respond(self, user_id, query, use_rag=True):
        print(f"\n[Input]: {query}")
        
        # 1. Retrieval
        context = ""
        if use_rag:
            retrieved = self.rag.retrieve(query)
            if retrieved:
                context = f"[Retrieved Context]: {retrieved}"
                print(context)
            else:
                print("[Retrieved Context]: None")
        
        # 2. Memory
        self.memory.append({"role": "user", "content": query})
        
        # 3. Reasoning & Tool Use (Simulated)
        response = ""
        if "fee" in query.lower() and not context and use_rag:
            # RAG failed or not used
            response = "I'm not sure about the fees."
        elif "fee" in query.lower() and context:
            response = f"Based on our policy: {context}"
            
        elif "eligible" in query.lower():
            # Tool Call
            product = "gold card" if "gold" in query.lower() else "unknown"
            print(f"[Tool Call]: check_eligibility(user_id='{user_id}', product='{product}')")
            try:
                result = self.tools.check_eligibility(user_id, product)
                print(f"[Tool Output]: {result}")
                response = f"You are {'eligible' if result.get('eligible') else 'not eligible'} for the {product}."
            except Exception as e:
                print(f"[Tool Error]: {e}")
                response = "I encountered an error checking eligibility."
                
        elif "transfer" in query.lower():
            # Refusal
            response = "I cannot perform transactions. Please use the banking portal."
            
        elif "my name" in query.lower():
             # Memory Recall simulation
             response = "I recall you mentioned your name earlier."
             
        else:
             response = "How can I help you regarding banking policies?"
             
        self.memory.append({"role": "assistant", "content": response})
        print(f"[Output]: {response}")
        return response
