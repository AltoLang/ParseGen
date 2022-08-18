import grammar_file
import emit

file = grammar_file.GrammarFile("../sample.grammar")
file.parse()

emit.emit(file)