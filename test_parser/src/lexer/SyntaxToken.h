#pragma once
#include <string>

enum SyntaxKind
{
    IdentifierToken,
    VarKeyword,
    EqualsToken,
    PlusToken,
    NumberToken
};

struct SyntaxToken
{
    SyntaxToken(SyntaxKind pKind, std::string pText)
        : kind(pKind),
          text(pText)
    { }

    SyntaxKind kind;
    std::string text;
};