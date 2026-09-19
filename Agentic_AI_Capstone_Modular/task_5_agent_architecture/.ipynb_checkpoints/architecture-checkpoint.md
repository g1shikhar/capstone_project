# Agent Architecture

## High-Level Data Flow

```mermaid
graph TD
    User -->|Query| Router
    Router -->|Policy?| RAG
    Router -->|Eligibility?| Tools
    Router -->|Chat?| LLM
    
    RAG -->|Context| LLM
    Tools -->|Result| LLM
    LLM -->|Response| SafetyCheck
    SafetyCheck -->|Safe| User
```

## detailed Components
1. **Orchestrator**: LangChain Agent.
2. **Memory**: ConversationBuffer (Session-based).
3. **Guardrails**: Input/Output filtering.
