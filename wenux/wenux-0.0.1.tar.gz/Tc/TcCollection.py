class TcCollection(list):
    @staticmethod
    def _operation_check(operation):
        _allowed_operation = ["add", "reset", "change"]

        if not (operation in _allowed_operation):
            raise Exception("Invalid operation parameter")
        else:
            return
