class GoSmsApiException(Exception):
    status = None
    error = None
    reason = None

    def __init__(self, status=None, error=None, reason=None, *args, **kwargs):
        self.status = status
        self.error = error
        self.reason = reason
        super().__init__(*args, **kwargs)
