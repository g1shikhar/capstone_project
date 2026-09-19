"""Single end-to-end banking use case using all capstone components.

Scenario
--------
Alice wants a Gold Card. She asks about its fee and then asks whether she is
eligible. The workflow applies prompting, adaptation, safety screening, RAG,
tool execution, memory-agent orchestration, and PII-safe monitoring to produce
a final result. A transfer attempt is included to demonstrate the safety guard.

Place this file in the Agentic_AI_Capstone_Modular project root and run:
    python integrated_banking_use_case_demo.py

Required empty __init__.py files should exist in each task_* folder.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from task_2_llm_integration.prompt_experiment import PromptExperiment
from task_3_embeddings_retrieval.rag_pipeline import BankingRAG
from task_4_tool_using_agent.tools import BankingTools
from task_6_planning_memory_rag.memory_agent import BankingAgent
from task_7_adaptation_learning.adaptation import AdaptiveAgent
from task_8_deployment_monitoring.monitoring_mock import ProductionLogger
from task_9_evaluation_ethics.safety import SafetyAgent


class IntegratedBankingWorkflow:
    """Coordinates every capstone module in one customer-service workflow."""

    def __init__(self):
        self.prompt_experiment = PromptExperiment()
        self.rag = BankingRAG()
        self.tools = BankingTools()
        self.memory_agent = BankingAgent()
        self.adaptive_agent = AdaptiveAgent()
        self.safety_agent = SafetyAgent()
        self.logger = ProductionLogger()

        # Enable clarification behavior for ambiguous product requests.
        self.adaptive_agent.mode = "Adaptive"
        self.safety_agent.adaptation_mode = "Adaptive"

    def _log(self, event_type: str, details: dict) -> None:
        self.logger.log_event(event_type, details)

    def _prompt_strategy(self, query: str) -> str:
        """Selects the project prompt strategy without duplicating its logic."""
        query_lower = query.lower()
        if any(word in query_lower for word in ("eligible", "fee", "loan", "kyc")):
            return "CoT"
        return "Naive"

    def _safety_check(self, user_id: str, query: str):
        """Blocks/refers unsafe requests before retrieval or tool execution."""
        query_lower = query.lower()
        safety_response = self.safety_agent.process(query)

        if "[REFUSAL]" in safety_response or "[ESCALATE]" in safety_response:
            decision = "refused" if "[REFUSAL]" in safety_response else "escalated"
            self._log(
                "safety_decision",
                {"user": user_id, "query": query, "decision": decision},
            )
            return safety_response

        # The standalone safety module handles loan clarification. The separate
        # adaptation module confirms the same adaptive behavior in this workflow.
        if "[CLARIFY]" in safety_response:
            adaptation_response = self.adaptive_agent.process(query)
            self._log(
                "adaptation_decision",
                {
                    "user": user_id,
                    "query": query,
                    "response": adaptation_response,
                },
            )
            return adaptation_response

        return None

    def handle_query(self, user_id: str, query: str) -> str:
        """Processes one request through the integrated decision pipeline."""
        print(f"\nUSER: {query}")
        self._log("customer_query", {"user": user_id, "query": query})

        safety_or_adaptation = self._safety_check(user_id, query)
        if safety_or_adaptation is not None:
            print(f"FINAL RESPONSE: {safety_or_adaptation}")
            return safety_or_adaptation

        strategy = self._prompt_strategy(query)
        print(f"[Prompt strategy selected]: {strategy}")

        # RAG supplies policy facts for the final customer-facing answer.
        context = self.rag.retrieve(query)
        print(f"[RAG context]: {context or 'No matching policy found'}")
        self._log(
            "rag_retrieval",
            {"user": user_id, "query": query, "context_found": bool(context)},
        )

        query_lower = query.lower()
        tool_result = None

        # Direct tool invocation demonstrates the task-4 component.
        if "eligible" in query_lower:
            product = "gold card" if "gold" in query_lower else "unknown"
            tool_result = self.tools.check_eligibility(user_id, product)
            print(f"[Tool result]: {tool_result}")
            self._log(
                "tool_usage",
                {
                    "user": user_id,
                    "tool": "check_eligibility",
                    "product": product,
                    "result": tool_result,
                },
            )

        elif "balance" in query_lower:
            tool_result = self.tools.get_balance(user_id)
            print(f"[Tool result]: {tool_result}")
            self._log(
                "tool_usage",
                {"user": user_id, "tool": "get_balance", "result": tool_result},
            )

        # MemoryAgent provides the reusable orchestration/memory trace.
        # Its response is called even when this workflow enriches the final reply.
        agent_response = self.memory_agent.respond(user_id, query, use_rag=True)

        if tool_result and tool_result.get("eligible") is True:
            final_response = (
                f"You are eligible for the Gold Card. {tool_result.get('reason', '')} "
                f"Policy details: {context or 'No policy details available.'}"
            )
        elif tool_result and tool_result.get("eligible") is False:
            final_response = (
                f"You are not eligible for this product. {tool_result.get('reason', '')}"
            )
        elif tool_result and "balance" in tool_result:
            final_response = (
                f"Your available balance is {tool_result['balance']} "
                f"{tool_result['currency']}."
            )
        elif context:
            final_response = f"Based on the banking policy: {context}"
        else:
            final_response = agent_response

        self._log(
            "final_response",
            {
                "user": user_id,
                "prompt_strategy": strategy,
                "used_rag": bool(context),
                "used_tool": tool_result is not None,
                "response": final_response,
            },
        )
        print(f"FINAL RESPONSE: {final_response}")
        return final_response

    def run_gold_card_journey(self) -> None:
        """Runs one connected customer journey, not separate component demos."""
        print("=" * 80)
        print("INTEGRATED USE CASE: ALICE'S GOLD CARD APPLICATION JOURNEY")
        print("=" * 80)

        user_id = "user_1234"  # Logger masks '1234' in emitted monitoring records.

        print("\nStep 1 — Prompt design is evaluated for the policy question.")
        self.prompt_experiment.test_prompts("What is the annual fee for the Gold Card?")

        print("\nStep 2 — Alice asks an ambiguous question; adaptation asks for detail.")
        self.handle_query(user_id, "I want a loan.")

        print("\nStep 3 — Alice asks the Gold Card policy question; RAG retrieves facts.")
        self.handle_query(user_id, "What is the annual fee for the Gold Card?")

        print("\nStep 4 — Alice asks for eligibility; tool output and RAG policy form one result.")
        self.handle_query(user_id, "Am I eligible for the Gold Card?")

        print("\nStep 5 — Alice attempts a transaction; safety prevents execution.")
        self.handle_query(user_id, "Please transfer $500 to my friend.")

        print("\nStep 6 — Alice reports fraud; the request is escalated.")
        self.handle_query(user_id, "I suspect fraud on my account and need a human agent.")

        print("\n" + "=" * 80)
        print("FINAL USE-CASE OUTCOME")
        print("=" * 80)
        print("- Policy information was grounded with RAG retrieval.")
        print("- Gold Card eligibility was checked with a read-only banking tool.")
        print("- The memory agent stored the customer conversation during processing.")
        print("- Adaptive behavior clarified an ambiguous loan query.")
        print("- Transfer requests were refused and fraud requests were escalated.")
        print("- All workflow events were sent through PII-scrubbed monitoring logs.")
        print(
            f"- Safety metrics: refusals={self.safety_agent.refusals}, "
            f"escalations={self.safety_agent.escalations}."
        )


def main() -> None:
    workflow = IntegratedBankingWorkflow()
    workflow.run_gold_card_journey()


if __name__ == "__main__":
    main()
