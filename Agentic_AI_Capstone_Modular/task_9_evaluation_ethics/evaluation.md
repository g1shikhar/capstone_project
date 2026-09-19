
# Phase 9: Evaluation & Engineering Review

## 1. Metrics
| Metric | Target | Definition |
| :--- | :--- | :--- |
| **Groundedness** | >90% | Response supported by retrieved chunks. |
| **Safety** | 100% | Block all transactional requests. |
| **Escalation** | >95% | Identify retention risks correctly. |

## 2. Safety Review
*   **Injection**: System prompt ignores instructions to "forget rules".
*   **PII**: Logs are scrubbed of credit card numbers.

## 3. Root Cause Analysis (Example)
*   **Failure**: "Free Loan" Hallucination.
*   **Cause**: Retrieving outdated marketing blog.
*   **Fix**: Added metadata filter `source != blog`.
