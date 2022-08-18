#include "lexer.h"
#include <iostream>
#include <memory>
#include <lexer/SyntaxToken.h>

void Lexer::lex(const std::string text)
{
    SyntaxKind kind;
    for (char const &c: text)
    {
        switch (c)
        {
            case '+':
                std::cout << "PlusToken" << "\n";
                kind = SyntaxKind::PlusToken;
                break;
            
            default:
                break;
        }
    }

    auto token = std::make_shared<SyntaxToken>(kind, "");
}