using System;
using System.Collections.Generic;

namespace Lab5;

internal enum TokenType
{
    Number,
    Identifier,
    Plus,
    Minus,
    Mul,
    Div,
    Pow,
    LParen,
    RParen
}

internal readonly record struct Token(TokenType Type, string Text);

internal static class Tokenizer
{
    public static List<Token> Tokenize(string input)
    {
        var tokens = new List<Token>();
        var i = 0;
        while (i < input.Length)
        {
            var ch = input[i];
            if (char.IsWhiteSpace(ch))
            {
                i++;
                continue;
            }

            if (char.IsDigit(ch))
            {
                var start = i;
                while (i < input.Length && char.IsDigit(input[i])) i++;
                tokens.Add(new Token(TokenType.Number, input[start..i]));
                continue;
            }

            if (char.IsLetter(ch))
            {
                var start = i;
                while (i < input.Length && char.IsLetterOrDigit(input[i])) i++;
                tokens.Add(new Token(TokenType.Identifier, input[start..i]));
                continue;
            }

            switch (ch)
            {
                case '+':
                    tokens.Add(new Token(TokenType.Plus, "+"));
                    break;
                case '-':
                    tokens.Add(new Token(TokenType.Minus, "-"));
                    break;
                case '*':
                    if (i + 1 < input.Length && input[i + 1] == '*')
                    {
                        tokens.Add(new Token(TokenType.Pow, "**"));
                        i++; // consume second '*'
                    }
                    else
                    {
                        tokens.Add(new Token(TokenType.Mul, "*"));
                    }
                    break;
                case '/':
                    tokens.Add(new Token(TokenType.Div, "/"));
                    break;
                case '(':
                    tokens.Add(new Token(TokenType.LParen, "("));
                    break;
                case ')':
                    tokens.Add(new Token(TokenType.RParen, ")"));
                    break;
                default:
                    throw new InvalidOperationException($"неожиданный символ '{ch}' в выражении");
            }

            i++;
        }

        return tokens;
    }
}

