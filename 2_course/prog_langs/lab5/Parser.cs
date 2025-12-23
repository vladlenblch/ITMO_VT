using System;
using System.Collections.Generic;
using System.Globalization;

namespace Lab5;

internal static class ShuntingYard
{
    public static List<Token> ToRpn(List<Token> tokens)
    {
        var output = new List<Token>();
        var stack = new Stack<Token>();

        foreach (var token in tokens)
        {
            switch (token.Type)
            {
                case TokenType.Number:
                case TokenType.Identifier:
                    output.Add(token);
                    break;
                case TokenType.Plus:
                case TokenType.Minus:
                case TokenType.Mul:
                case TokenType.Div:
                case TokenType.Pow:
                    while (stack.Count > 0 && IsOperator(stack.Peek()) &&
                           (Precedence(stack.Peek()) > Precedence(token) ||
                           (Precedence(stack.Peek()) == Precedence(token) && IsLeftAssociative(token.Type))))
                    {
                        output.Add(stack.Pop());
                    }
                    stack.Push(token);
                    break;
                case TokenType.LParen:
                    stack.Push(token);
                    break;
                case TokenType.RParen:
                    while (stack.Count > 0 && stack.Peek().Type != TokenType.LParen)
                        output.Add(stack.Pop());
                    if (stack.Count == 0 || stack.Pop().Type != TokenType.LParen)
                        throw new InvalidOperationException("несогласованные скобки");
                    break;
                default:
                    throw new InvalidOperationException("неподдерживаемый токен в разборе");
            }
        }

        while (stack.Count > 0)
        {
            var t = stack.Pop();
            if (t.Type is TokenType.LParen or TokenType.RParen)
                throw new InvalidOperationException("несогласованные скобки");
            output.Add(t);
        }

        return output;
    }

    private static bool IsOperator(Token t) =>
        t.Type is TokenType.Plus or TokenType.Minus or TokenType.Mul or TokenType.Div or TokenType.Pow;

    private static int Precedence(Token t) => t.Type switch
    {
        TokenType.Plus or TokenType.Minus => 1,
        TokenType.Mul or TokenType.Div => 2,
        TokenType.Pow => 3,
        _ => 0
    };

    private static bool IsLeftAssociative(TokenType type) =>
        type is TokenType.Plus or TokenType.Minus or TokenType.Mul or TokenType.Div;
}

internal static class AstBuilder
{
    public static Node Build(List<Token> rpn)
    {
        var stack = new Stack<Node>();
        foreach (var token in rpn)
        {
            switch (token.Type)
            {
                case TokenType.Number:
                    var value = long.Parse(token.Text, CultureInfo.InvariantCulture);
                    stack.Push(new ConstantNode(value));
                    break;
                case TokenType.Identifier:
                    stack.Push(new VariableNode(token.Text));
                    break;
                case TokenType.Plus:
                case TokenType.Minus:
                case TokenType.Mul:
                case TokenType.Div:
                case TokenType.Pow:
                    if (stack.Count < 2)
                        throw new InvalidOperationException("некорректное выражение");
                    var right = stack.Pop();
                    var left = stack.Pop();
                    stack.Push(new BinaryNode(token.Type, left, right));
                    break;
                default:
                    throw new InvalidOperationException("неожиданный токен при построении ast");
            }
        }

        return stack.Count == 1
            ? stack.Pop()
            : throw new InvalidOperationException("некорректное выражение");
    }
}

