from unittest.mock import MagicMock
from src.logger.logger import OperationLogger

def test_logger_notifier_integration():
    # Mock Notifier
    mock_notifier = MagicMock()
    mock_notifier.send_notification.return_value = "Mocked alert"

    logger = OperationLogger()

    result = 15  # Example result
    logger.log_operation(f"Result is {result}")

    alert_message = mock_notifier.send_notification(result)

    # Assertions
    assert "Result is 15" in logger.get_history()[0]
    assert alert_message == "Mocked alert"

    # Verify notifier behavior
    mock_notifier.send_notification.assert_called_once_with(result)
