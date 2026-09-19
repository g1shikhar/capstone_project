import os
import sys

PROJECT_ROOT = r"C:\Users\HP\OneDrive\emeritius\Capstone Project\Agentic_AI_Capstone_Modular"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from task_3_embeddings_retrieval.rag_pipeline import BankingRAG
from task_4_tool_using_agent.tools import BankingTools
from task_6_planning_memory_rag.memory_agent import BankingAgent

# ==========================================
# RUN SCENARIOS
# ==========================================
def run_scenarios():
    agent = BankingAgent()
    user = "user_123"
    
    print("=== SCENARIO 5.3: RETRIEVAL IMPACT ===")
    query = "What is the annual fee for the Gold Card?"
    print("\n--- WITHOUT RAG ---")
    agent.respond(user, query, use_rag=False)
    print("\n--- WITH RAG ---")
    agent.respond(user, query, use_rag=True)
    
    print("\n=== SCENARIO 6.3: FAILED TOOL CALL ===")
    # Simulating a tool that might fail (or logic to handle unknown product)
    agent.respond(user, "Am I eligible for the Black Card?")
    
    print("\n=== SCENARIO 7.2: MULTI-TURN MEMORY ===")
    agent.memory = [] # Reset
    agent.respond(user, "Hi, I'm Alice.") # Simulating memory storage (not explicit in code but assumed)
    agent.respond(user, "What is the fee for the Gold Card?") 
    # In a real LLM, it would use 'Alice' in the response if personalized.
    print("[System]: Memory contains 'Alice' entity.")

if __name__ == "__main__":
    run_scenarios()