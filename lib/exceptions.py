class ButtonAlreadyExists(Exception):
    """This class is used to raise custom exceptions when a button already exists."""
    def __init__(self, message : str) -> None:
        self.message = message
        super().__init__(self.message)

        