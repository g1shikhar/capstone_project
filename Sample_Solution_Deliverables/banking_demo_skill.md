---
name: banking-demo-orchestrator
description: Run and explain the end-to-end Agentic AI Banking Capstone demonstration. Use this skill when a user wants a banking-policy answer, eligibility check, balance lookup, adaptive clarification, fraud escalation, transaction refusal, or a complete integrated demo using prompt strategies, RAG, tools, memory, safety, adaptation, and PII-safe monitoring.
version: 1.0.0
---

# Banking Demo Orchestrator Skill

## Purpose

This skill describes how to run a single, realistic banking-assistant workflow built from the modular Agentic AI Capstone components. It combines prompting, retrieval-augmented generation (RAG), banking tools, session memory, adaptive clarification, safety governance, escalation, and PII-safe monitoring to produce one final customer-facing outcome.

The skill is intended for a **demonstration environment**. Banking data and policy text are mock data. No real transactions, account changes, or external banking operations are permitted.

## Supported Customer Requests

- Ask about Gold Card fees, student accounts, KYC requirements, or loan policies.
- Check a mock user balance.
- Check eligibility for a banking product.
- Ask an ambiguous loan question and receive clarification.
- Attempt a transfer or payment and receive a refusal.
- Report fraud or request a human agent and receive an escalation.

## Component Map

| Capability | Module | Class | Expected method |
|---|---|---|---|
| Prompt strategy experiment | `task_2_llm_integration.prompt_experiment` | `PromptExperiment` | `test_prompts(query)` |
| Policy retrieval | `task_3_embeddings_retrieval.rag_pipeline` | `BankingRAG` | `retrieve(query)` |
| Read-only banking tools | `task_4_tool_using_agent.tools` | `BankingTools` | `get_balance`, `check_eligibility` |
| Memory and agent orchestration | `task_6_planning_memory_rag.memory_agent` | `BankingAgent` | `respond(user_id, query, use_rag=True)` |
| Adaptation | `task_7_adaptation_learning.adaptation` | `AdaptiveAgent` | `process(query)` |
| Observability | `task_8_deployment_monitoring.monitoring_mock` | `ProductionLogger` | `log_event(event_type, details)` |
| Safety and governance | `task_9_evaluation_ethics.safety` | `SafetyAgent` | `process(query)` |

## Import Setup

Run the demo from the `Agentic_AI_Capstone_Modular` project root. Ensure every task directory is a Python package by adding an empty `__init__.py` file.

```python
from pathlib import Path

for folder in [
    "task_2_llm_integration",
    "task_3_embeddings_retrieval",
    "task_4_tool_using_agent",
    "task_6_planning_memory_rag",
    "task_7_adaptation_learning",
    "task_8_deployment_monitoring",
    "task_9_evaluation_ethics",
]:
    Path(folder, "__init__.py").touch(exist_ok=True)
```

Use these imports:

```python
from task_2_llm_integration.prompt_experiment import PromptExperiment
from task_3_embeddings_retrieval.rag_pipeline import BankingRAG
from task_4_tool_using_agent.tools import BankingTools
from task_6_planning_memory_rag.memory_agent import BankingAgent
from task_7_adaptation_learning.adaptation import AdaptiveAgent
from task_8_deployment_monitoring.monitoring_mock import ProductionLogger
from task_9_evaluation_ethics.safety import SafetyAgent
```

## Workflow

Follow this order for every incoming customer request.

1. **Log the request** using `ProductionLogger.log_event`. Send only minimal information necessary for observability. The logger must scrub or mask PII.

2. **Run the safety gate first** with `SafetyAgent.process(query)`.
   - If the result contains `[REFUSAL]`, stop. Return the refusal and log a `safety_decision` event.
   - If the result contains `[ESCALATE]`, stop. Return the escalation and log a `safety_decision` event.
   - Do not call transfer, payment, or other transactional tools after a refusal.

3. **Run adaptive clarification** for incomplete or ambiguous product requests.
   - Set `AdaptiveAgent.mode = "Adaptive"`.
   - For a generic loan request such as “I want a loan,” return the clarification before retrieval or a banking tool call.
   - Ask for the smallest useful missing detail: Personal, Home, or Auto loan.

4. **Choose a prompting strategy** appropriate to the request.
   - Use a concise direct strategy for simple informational requests.
   - Use a reasoning-oriented strategy for eligibility, policy, fee, KYC, and loan questions.
   - Use a clarification strategy for ambiguity.
   - `PromptExperiment` is demonstrative; it may print simulated outcomes rather than invoke a live LLM.

5. **Retrieve policy context** using `BankingRAG.retrieve(query)`.
   - Use retrieved information as grounded context for policy-related answers.
   - If no policy matches, say that policy context was not found; do not fabricate a policy.

6. **Use banking tools only when needed**.
   - For a balance query, call `BankingTools.get_balance(user_id)`.
   - For eligibility, call `BankingTools.check_eligibility(user_id, product_type)`.
   - Treat missing or error results as unavailable information, not as a positive or negative decision.

7. **Invoke the memory agent** with `BankingAgent.respond(user_id, query, use_rag=True)`.
   - This preserves the session trace and demonstrates the existing agent orchestration.
   - Use it as a fallback if no targeted RAG/tool answer is available.

8. **Compose one final answer**.
   - For eligibility queries, combine eligibility-tool output with relevant RAG policy context.
   - For policy queries, answer from retrieved context.
   - For balance queries, answer from the read-only tool result.
   - For safety outcomes, return the refusal or escalation as the final answer.

9. **Log the final result** using PII-safe fields only.
   - Suggested fields: workflow stage, whether RAG was used, whether a tool was used, safety decision, success/failure state.

## Decision Rules

| Intent or condition | Required action | Final response behavior |
|---|---|---|
| “Transfer”, “pay”, or transaction request | Safety refusal; do not invoke transactional tool | Explain that transactions cannot be performed in the demo and direct the user to the banking portal |
| “Fraud” or “human agent” | Safety escalation | State that the request is being referred to a human support agent |
| Generic loan request in adaptive mode | Ask clarification | Request loan type: Personal, Home, or Auto |
| Gold Card fee / KYC / student account query | RAG retrieval | Use only retrieved mock-policy details |
| “What is my balance?” | `get_balance` | Return balance and currency if found |
| “Am I eligible?” | `check_eligibility` plus RAG | Return the eligibility result, its reason, and applicable policy context |
| No matching context or tool result | Memory-agent fallback | State that information is unavailable or provide the general agent response |

## Single Use-Case Script

The default narrative is **Alice’s Gold Card application journey**:

1. Alice asks an ambiguous loan question and gets clarification.
2. Alice asks for Gold Card annual-fee information and RAG retrieves policy context.
3. Alice asks whether she is eligible for the Gold Card.
4. The workflow retrieves policy context, calls the eligibility tool, records the interaction in memory, logs the event, and produces one final answer.
5. Alice tries to transfer money; the safety gate refuses it.
6. Alice reports suspected fraud; the workflow escalates to human support.

Use the project’s `integrated_banking_use_case_demo.py` to run this scenario:

```bash
python integrated_banking_use_case_demo.py
```

## Expected Final Answer Format

For a Gold Card eligibility request, the response should consolidate results, for example:

```text
You are eligible for the Gold Card. Income > limit.
Policy details: Gold Credit Card: Annual Fee is $50. Waived if spend > $10k/year. Interest: 18% APR.
```

For a blocked transaction:

```text
[REFUSAL] I cannot perform transactions. Policy #12.
```

For fraud:

```text
[ESCALATE] Transferring you to a Human Agent.
```

## Guardrails

- Never execute money transfers, payments, account closures, or other state-changing banking requests.
- Run the safety layer before RAG, tools, or agent orchestration whenever a request might involve a transaction, fraud, or escalation.
- Do not claim real eligibility, real account balances, or real bank policy applicability.
- Treat all data in the project as simulated demo data.
- Mask account numbers, user identifiers, and other PII in logs and presentation output.
- Clearly state when a tool returns no result, an unknown product, or an error.

## Demo Success Criteria

A successful run shows all of the following in a single connected execution:

- Prompt strategy is evaluated or selected.
- The ambiguous loan request triggers adaptive clarification.
- Gold Card policy is retrieved from the RAG component.
- Eligibility is checked with `BankingTools`.
- `BankingAgent` records the conversation flow.
- The final customer answer combines tool output and RAG context.
- Transfer is refused before execution.
- Fraud is escalated.
- Monitoring events are emitted with PII masking.
