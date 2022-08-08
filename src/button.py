from text import Text


class Button(Text):
    def __init__(self, *args, active=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.active = active
