from definitions import *
from grammar_file import *

## walk grammar file
def emit(file: GrammarFile) -> None:
    for token in file.token_region.tokens:
        print("Found token definition: " + token.name)
    
    for expression in file.expression_region.expressions:
        print("Found expression definition: " + expression.name)