from .logger import OperationLogger

def test_log_operation():
    logger = OperationLogger()
    logger.log_operation("2 + 3 = 5")
    assert len(logger.get_history()) == 1
    assert "2 + 3 = 5" in logger.get_history()[0]
