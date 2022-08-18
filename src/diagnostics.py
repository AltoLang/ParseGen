from enum import Enum

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