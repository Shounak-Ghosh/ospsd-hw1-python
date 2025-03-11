from src.logger.logger import OperationLogger
from src.notifier.notifier import Notifier

def test_logger_notifier_integration():
    logger = OperationLogger()
    notifier = Notifier(threshold=10)

    result = 15
    logger.log_operation(f"Result is {result}")
    
    alert_message = notifier.send_notification(result)
    
    assert "Result is 15" in logger.get_history()[0]
    assert alert_message == "Alert! Result 15 exceeds threshold 10"
