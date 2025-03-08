from .notifier import Notifier

def test_send_notification():
    notifier = Notifier(threshold=10)
    assert notifier.send_notification(15) == "Alert! Result 15 exceeds threshold 10"
    assert notifier.send_notification(5) == "No alert needed"
