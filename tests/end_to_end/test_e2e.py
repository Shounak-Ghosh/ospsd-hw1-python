from src.calculator import add
from src.logger.logger import OperationLogger
from src.notifier.notifier import Notifier

def test_end_to_end():
    logger = OperationLogger()
    notifier = Notifier(threshold=10)

    # Perform calculation and log it.
    result = add(7, 8)
    logger.log_operation(f"7 + 8 = {result}")

    # Send notification if needed.
    alert_message = notifier.send_notification(result)

    # Assertions for E2E flow.
    history = logger.get_history()
    
    assert len(history) == 1
    assert "7 + 8 = 15" in history[0]
    
    assert alert_message == "Alert! Result 15 exceeds threshold 10"
