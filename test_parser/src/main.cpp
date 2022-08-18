#include <string>
#include <iostream>
#include <lexer/lexer.h>

int main()
{
    const std::string text = "var test = 1 + 2";

    Lexer lexer;
    lexer.lex(text);

    return 0;
}