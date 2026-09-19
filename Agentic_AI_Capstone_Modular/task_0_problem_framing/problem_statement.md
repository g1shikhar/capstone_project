# Problem Framing: AI Banking Support Agent

## 1. User Persona & Workflow
**Primary User**: Retail Banking Customer (Existing Client)
**Workflow**: Login -> Open Chat -> Ask Policy/Eligibility Question -> Receive Immediate Answer.

## 2. Problem Statement
**Goal**: Build a "Safety-First" Advisory Agent that answers policy/eligibility questions using RAG and Tools, while strictly refusing transactional commands.

**Success Criteria**:
*   **Accuracy**: >90% on "Eligibility" questions.
*   **Safety**: 100% Refusal of "Transfer/Pay" commands.

## 3. Constraints
*   **Non-Transactional**: Read-Only access.
*   **Safety**: Zero tolerance for jailbreaks.
