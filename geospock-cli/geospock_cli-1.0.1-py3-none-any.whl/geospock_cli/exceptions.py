class CLIError(RuntimeError):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            if len(args) > 1:
                self.exit_code = args[1]
            else:
                self.exit_code = 1
        else:
            self.message = "Unknown error occurred"
