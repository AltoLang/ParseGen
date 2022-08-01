from enum import Enum

class Qualifier:
    def __init__(self, parts: list[str], combine: bool) -> None:
        self.parts = parts
        self.combine = combine


class Token:
    def __init__(self, name: str, qualifier: Qualifier) -> None:
        self.name = name
        self.qualifier = qualifier


class Expression:
    def __init__(self, name: str, ordered_tokens: list[Token]) -> None:
        self.name = name
        self.ordered_tokens = ordered_tokens


class RegionType(Enum):
    Tokens = 1
    Expressions = 2


class TokenRegion:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens


class ExpressionRegion:
    def __init__(self, expressions: list[Expression]) -> None:
        self.expressions = expressions