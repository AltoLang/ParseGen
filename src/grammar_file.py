from enum import Enum
from definitions import *

class GrammarFile:
    def __init__(self, path: str) -> None:
        file = open(path, 'r')
        self.lines = file.readlines()

    def parse(self) -> None:
        current_region = None
        self.token_region = TokenRegion([])
        self.expression_region = ExpressionRegion([])

        for line in self.lines:
            index = self.lines.index(line) + 1
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

            if ':=' not in sterilized:
                    report_error(ErrorType.MalformedExpression, index)
                    return

            if current_region == RegionType.Tokens:
                # TokenName := @combine('1', '2')
                
                token_name = sterilized[0:sterilized.find(':=')]
                for t in self.token_region.tokens:
                    if t.name == token_name:
                        report_error(ErrorType.TokenAlreadyDefined, index)
                        return
                
                assignee = sterilized[(sterilized.find(':=') + 2):len(sterilized)]
                qualifier = self.get_token_qualifier(assignee, index)
                if qualifier == None:
                    return
                
                token = Token(token_name, qualifier)                
                self.token_region.tokens.append(token)
            
            elif current_region == RegionType.Expressions:
                # ExpressionName := <FirstToken> <SecondToken>

                expression_name = sterilized[0:sterilized.find(':=')]
                for e in self.expression_region.expressions:
                    if e.name == expression_name:
                        report_error(ErrorType.TokenAlreadyDefined, index)
                        return

                assignee = sterilized[(sterilized.find(':=') + 2):len(sterilized)]
                tokens = self.parse_expression_assignee(assignee, index)

                expression = Expression(expression_name, tokens)
                self.expression_region.expressions.append(expression)   
                         
            elif (current_region == None):
                report_error(ErrorType.NotParsingRegion, index)
                return

    def get_token_qualifier(self, assignee: str, index: int) -> Qualifier:
        parts = []
        combine = False
        if assignee[0] == "'" or assignee[0] == '"':
            parts = self.parse_assignee_list(assignee, index, 1)
        elif assignee[0] == '@':
            if ('(' not in assignee) or (')' not in assignee):
                report_error(ErrorType.WrongAssignee, index)
                return None

            function_name = assignee[1:assignee.find('(')]
            arguments_text = assignee[assignee.find('('):assignee.find(')')] \
                                .replace('(', '') \
                                .replace(')', '')
            
            arguments = self.parse_assignee_list(arguments_text, index, None)
            match function_name:
                case 'includes':
                    parts = arguments
                    combine = False
                    pass
                case 'combine':
                    parts = arguments
                    combine = True
                    pass
                case _:
                    report_error(ErrorType.UnknownFunction, index)
                    return
        else:
            report_error(ErrorType.WrongAssignee, index)
            return None

        q = Qualifier(parts, combine)
        return Qualifier

    def parse_expression_assignee(self, assignee: str, index: int) -> list[Token]:
        opened = False
        token_name = ""
        tokens = []

        for c in assignee:
            if c == '<':
                opened = True
                continue
            elif c == '>':
                matches = []
                for t in self.token_region.tokens:
                    if t.name == token_name:
                        matches.append(t)

                if len(matches) == 0:
                    report_error(ErrorType.UndefinedToken, index)
                    return None
                
                token = matches[0]
                tokens.append(token)

                opened = False
                token_name = ""
                continue

            if opened:
                token_name += c

        if opened:
            report_error(ErrorType.UnterminatedTokenReference, index)
            return None

        return tokens

    def parse_assignee_list(self, text: str, index: int, max_length: int) -> list:
        text = text.replace('"', "'")
        literals = []
        parts = text.split(',')

        for part in parts:
            if part[0] == "'":
                # literal
                if not part.count("'") == 2:
                    report_error(ErrorType.WrongAssignee, index)
                    return None

                literal = part.replace("'", '')
                literals.append(literal)
            elif part[0] == '<':
                # existing token    
                if (not '<' in part) or (not '>' in part) or (part.count('<') > 1) or (part.count('>') > 1):
                    report_error(ErrorType.WrongAssignee, index)
                    return None

                token_name = part.replace('<', '') \
                                 .replace('>', '')

                matching_tokens = []
                for t in self.token_region.tokens:
                    if t.name == token_name:
                        matching_tokens.append(t)

                if len(matching_tokens) == 0:
                    report_error(ErrorType.UndefinedToken, index)
                    return None
                
                token = matching_tokens[0]
                literals.append(token)
            else:
                report_error(ErrorType.WrongAssignee, index)
                return None
            
        if (not max_length == None) and len(parts) > max_length:
            report_error(ErrorType.WrongAssignee, index)
            return None

        return literals


class ErrorType(Enum):
    NotParsingRegion = 1
    NoAssignmentOperator = 2
    MalformedExpression = 3
    WrongAssignee = 4
    TokenAlreadyDefined = 5
    UnknownFunction = 6
    UndefinedToken = 7
    UnterminatedTokenReference = 8

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
        case ErrorType.TokenAlreadyDefined:
            print("Token Already Defined")
        case ErrorType.UnknownFunction:
            print("Unknown Function!")
        case ErrorType.UndefinedToken:
            print("Undefined Token")
        case ErrorType.UnterminatedTokenReference:
            print("Unterminated Token Reference")

    print("    - On line {}".format(line))