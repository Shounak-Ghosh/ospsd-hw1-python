class Notifier:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def send_notification(self, result: float) -> str:
        if result > self.threshold:
            return f"Alert! Result {result} exceeds threshold {self.threshold}"
        return "No alert needed"
