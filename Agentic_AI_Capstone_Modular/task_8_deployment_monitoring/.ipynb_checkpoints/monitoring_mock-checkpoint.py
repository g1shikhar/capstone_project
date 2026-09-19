
import json
import time

class ProductionLogger:
    def log_event(self, event_type, details):
        log_entry = {
            "timestamp": time.time(),
            "event": event_type,
            "details": self.scrub_pii(details)
        }
        print(json.dumps(log_entry))

    def scrub_pii(self, data):
        # Mock PII scrubbing
        s = str(data)
        if "1234" in s:
            return s.replace("1234", "[MASKED]")
        return data

if __name__ == "__main__":
    logger = ProductionLogger()
    logger.log_event("tool_usage", {"user": "user_1234", "action": "balance_check"})
