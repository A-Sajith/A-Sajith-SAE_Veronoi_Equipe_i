class ParseError(ValueError):
    def __init__(self, message: str, *, line_number: int | None = None, line_text: str | None = None) -> None:
        full_message = message
        if line_number is not None:
            full_message = f"Ligne {line_number}: {full_message}"
        if line_text is not None:
            full_message = f"{full_message} (contenu: {line_text!r})"
        super().__init__(full_message)
        self.line_number = line_number
        self.line_text = line_text


class VoronoiComputationError(RuntimeError):
    pass
