import os
import string
from enum import Enum
from operator import index

from numpy import full

class Qualifier:
    def __init__(self, parts: string, combine: bool) -> None:
        self.parts = parts
        self.combine = combine


class Token:
    def __init__(self, name: string, qualifier: Qualifier) -> None:
        self.name = name
        self.qualifier = qualifier


class RegionType(Enum):
    Tokens = 1
    Expressions = 2


class TokenRegion:
    def __init__(self, tokens: Token) -> None:
        self.tokens = tokens


class GrammarFile:
    def __init__(self, path: string) -> None:
        file = open(path, 'r')
        self.lines = file.readlines()

    def parse(self) -> None:
        current_region = None
        tokens = []

        for line in self.lines:
            sterilized = line.replace(' ', '')
            sterilized = sterilized.replace('\n', '')

            if sterilized == '':
                continue

            if sterilized == '.tokens:':
                current_region = RegionType.Tokens
                continue
            elif sterilized == '.expressions:':
                current_region = RegionType.Expressions
                continue

            if current_region == RegionType.Tokens:
                # TokenName := @combine('1', '2')

                if ':=' not in sterilized:
                    index = self.lines.index(line) + 1
                    report_error(ErrorType.MalformedExpression, index)
                    return
                
                token_name = sterilized[0:sterilized.find(':=')]
                assignee = sterilized[(sterilized.find(':=') + 2):len(sterilized)]
                qualifier = self.get_qualifier(assignee, line)
                if qualifier == None:
                    return
                
                token = Token(token_name, qualifier)
                tokens.append(token)
            elif current_region == RegionType.Expressions:
                continue
            elif (current_region == None):
                index = self.lines.index(line) + 1
                report_error(ErrorType.NotParsingRegion, index)
                return

    def get_qualifier(self, assignee: string, full_line: string) -> Qualifier:
        parts = []
        combine = False
        if assignee[0] == "'" or assignee[0] == '"':
            part = assignee.replace("'", '')
            part = part.replace('"', '')
            parts.append(part)
        elif assignee[0] == '@':
            if ('(' not in assignee) or (')' not in assignee):
                index = self.lines.index(full_line) + 1
                report_error(ErrorType.WrongAssignee, index)
                return None

            function_name = assignee[1:assignee.find('(')]
            match function_name:
                case 'includes':
                    pass
                case 'combine':
                    pass
                case _:
                    index = self.lines.index(full_line) + 1
                    report_error(ErrorType.UnknownFunction, index)
        else:
            index = self.lines.index(full_line) + 1
            report_error(ErrorType.WrongAssignee, index)
            return None

        q = Qualifier(parts, combine)
        return Qualifier


class ErrorType(Enum):
    NotParsingRegion = 1
    NoAssignmentOperator = 2
    MalformedExpression = 3
    WrongAssignee = 4
    UnknownFunction = 5

def report_error(type: ErrorType, line: int) -> None:
    match type:
        case ErrorType.NotParsingRegion:
            print("Not Parsing a Region!")
        case ErrorType.NoAssignmentOperator:
            print("Assignment operator missing!")
        case ErrorType.MalformedExpression:
            print("Malformed Expression!")
        case ErrorType.WrongAssignee:
            print("Wrong Assignee!")
        case ErrorType.UnknownFunction:
            print("Unknown Function!")

    print("    - On line {}".format(line))