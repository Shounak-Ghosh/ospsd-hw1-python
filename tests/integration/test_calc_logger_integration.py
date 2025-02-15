import src.logger as logger

def test_calc_logger_integration(mocker):
    mock_notifier = mocker.Mock()
    result = add(5, 3)
    logger.log_operation(f"5+3={result}")
    assert "5+3=8" in logger.history[-1]
