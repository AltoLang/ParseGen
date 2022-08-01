from operator import index
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
        current_region = None
        tokens = []

        for line in self.lines:
            sterilized = line.replace(' ', '')
            sterilized = sterilized.replace('\n', '')
            print(sterilized)

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
                print(token_name)
            elif current_region == RegionType.Expressions:
                continue
            elif (current_region == None):
                index = self.lines.index(line) + 1
                report_error(ErrorType.NotParsingRegion, index);
                return



class ErrorType(Enum):
    NotParsingRegion = 1
    NoAssignmentOperator = 2
    MalformedExpression = 3

def report_error(type, line):
    match type:
        case ErrorType.NotParsingRegion:
            print("Not Parsing a Region!")
        case ErrorType.NoAssignmentOperator:
            print("Assignment operator missing!")
        case ErrorType.MalformedExpression:
            print("Malformed Expression!")

    print("    - On line {}".format(line))