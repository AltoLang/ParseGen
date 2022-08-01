from msilib.schema import Error
import os
from enum import Enum

class Qualifier:
    def __init__(self, parts, combine):
        self.parts = parts
        self.combine = combine


class Token:
    def __init__(self, name, qualifier):
        self.name = name
        self.qualifier = qualifier


class RegionType(Enum):
    Tokens = 1
    Expressions = 2


class TokenRegion:
    def __init__(self, tokens):
        self.tokens = tokens


class GrammarFile:
    def __init__(self, path):
        file = open(path, 'r')
        self.lines = file.readlines()

    def parse(self):
        index = 0
        current_region = None

        tokens = []
        while True:
            line = self.lines[index]
            sterilized = line.replace(' ', '')

            if sterilized == '.tokens:':
                current_region = RegionType.Tokens
            elif sterilized == '.expressions:':
                current_region = RegionType.Expressions

            if current_region == RegionType.Tokens:
                # TokenName := @combine('1', '2')
                pass
            elif current_region == RegionType.Expressions:
                pass
            elif (current_region == None):
                report_error(ErrorType.NotParsingRegion, index + 1);
                return

            index += 1


class ErrorType(Enum):
    NotParsingRegion = 1
    NoAssignmentOperator = 2

def report_error(type, line):
    match type:
        case ErrorType.NotParsingRegion:
            print("Not Parsing a Region!")
        case ErrorType.NoAssignmentOperator:
            print("Assignment operator missing!")

    print("    - At line {line}")