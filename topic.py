class Topic:

    def __init__(self, path : str, on_value : str, off_value : str) -> None:
        self.path = path
        self.on_value = on_value
        self.off_value = off_value