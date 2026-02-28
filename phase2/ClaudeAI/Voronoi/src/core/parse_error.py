from dataclasses import dataclass


@dataclass(frozen=True)
class ParseError(Exception):
    line_number: int
    raw_content: str
    reason: str

    def __str__(self) -> str:
        return f'Ligne {self.line_number}: "{self.raw_content}" — {self.reason}'
