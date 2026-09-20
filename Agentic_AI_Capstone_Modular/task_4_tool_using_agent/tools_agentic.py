"""Read-only banking tools exposed to the LLM agent through OpenAI function calling."""

from __future__ import annotations


class BankingTools:
    """Mock read-only banking tools. Transaction execution is intentionally blocked."""

    def __init__(self) -> None:
        self.accounts = {
            "user_123": {"balance": 5000.00, "currency": "USD"},
            "user_1234": {"balance": 5000.00, "currency": "USD"},
        }
        self.eligibility = {
            ("user_123", "gold card"): {"eligible": True, "reason": "Income exceeds the configured limit."},
            ("user_1234", "gold card"): {"eligible": True, "reason": "Income exceeds the configured limit."},
            ("user_123", "platinum card"): {"eligible": False, "reason": "Credit score is below 750."},
            ("user_1234", "platinum card"): {"eligible": False, "reason": "Credit score is below 750."},
        }

    def get_balance(self, user_id: str) -> dict:
        """Return a mock balance for an authenticated demo user."""
        account = self.accounts.get(user_id)
        if not account:
            return {"found": False, "message": "No demo account was found for this user."}
        return {"found": True, **account}

    def check_eligibility(self, user_id: str, product_type: str) -> dict:
        """Return a mock eligibility result for the requested product."""
        product = product_type.lower().strip()
        result = self.eligibility.get((user_id, product))
        if result:
            return {"product": product, **result}
        return {
            "product": product,
            "eligible": None,
            "message": "Eligibility is unavailable for this demo product or user.",
        }

    def transfer_money(self, user_id: str, amount: float) -> dict:
        """Always block transactions in the demo environment."""
        raise PermissionError(
            "Transaction blocked: this demonstration permits read-only banking tools only."
        )

    @staticmethod
    def openai_tool_schemas() -> list[dict]:
        """OpenAI-compatible schemas made available to the LLM agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_balance",
                    "description": "Get the authenticated demo user's current account balance. Use only when the user asks about their balance.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "check_eligibility",
                    "description": "Check the authenticated demo user's eligibility for a banking product such as Gold Card or Platinum Card.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_type": {
                                "type": "string",
                                "description": "The product to check, for example 'gold card'.",
                            }
                        },
                        "required": ["product_type"],
                        "additionalProperties": False,
                    },
                },
            },
        ]

    def execute_tool(self, name: str, arguments: dict, user_id: str) -> dict:
        """Dispatch a model-requested, allow-listed tool call."""
        if name == "get_balance":
            return self.get_balance(user_id)
        if name == "check_eligibility":
            return self.check_eligibility(user_id, arguments["product_type"])
        return {"error": f"Tool '{name}' is not allowed."}
