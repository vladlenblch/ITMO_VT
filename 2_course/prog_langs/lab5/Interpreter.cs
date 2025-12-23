using System;
using System.Collections.Generic;

namespace Lab5;

internal sealed class Interpreter
{
    private Node? _root;
    private readonly Dictionary<string, long> _variables = new(StringComparer.OrdinalIgnoreCase);

    public void SetExpression(string expression)
    {
        var tokens = Tokenizer.Tokenize(expression);
        var rpn = ShuntingYard.ToRpn(tokens);
        _root = AstBuilder.Build(rpn);
    }

    public void SetVariable(string name, long value) => _variables[name] = value;

    public IEnumerable<string> Evaluate()
    {
        if (_root == null)
            throw new InvalidOperationException("выражение не задано: используйте expr <выражение>");

        foreach (var output in EvaluateNode(_root))
            yield return output;
    }

    private IEnumerable<string> EvaluateNode(Node node)
    {
        switch (node)
        {
            case ConstantNode c:
                c.CachedValue = c.Value;
                yield break;
            case VariableNode v:
            {
                if (!_variables.TryGetValue(v.Name, out var val))
                    throw new InvalidOperationException($"переменная '{v.Name}' не задана");
                v.CachedValue = val;
                yield break;
            }
            case BinaryNode b:
            {
                foreach (var s in EvaluateNode(b.Left))
                    yield return s;
                foreach (var s in EvaluateNode(b.Right))
                    yield return s;

                var leftVal = b.Left.CachedValue ?? throw new InvalidOperationException("внутренняя ошибка вычисления (левый операнд отсутствует)");
                var rightVal = b.Right.CachedValue ?? throw new InvalidOperationException("внутренняя ошибка вычисления (правый операнд отсутствует)");
                b.CachedValue = b.Op switch
                {
                    TokenType.Plus => leftVal + rightVal,
                    TokenType.Minus => leftVal - rightVal,
                    TokenType.Mul => leftVal * rightVal,
                    TokenType.Div => rightVal == 0
                        ? throw new DivideByZeroException("деление на ноль")
                        : leftVal / rightVal,
                    TokenType.Pow => PowChecked(leftVal, rightVal),
                    _ => throw new InvalidOperationException($"неподдерживаемый оператор {b.Op}")
                };

                yield return $"{b.ToInfix()} = {b.CachedValue}";
                yield break;
            }
            default:
                throw new InvalidOperationException("неизвестный узел ast");
        }
    }

    private static long PowChecked(long @base, long exp)
    {
        if (exp < 0)
            throw new InvalidOperationException("отрицательная степень не поддерживается для целых");
        long result = 1;
        var power = @base;
        var e = exp;
        checked
        {
            while (e > 0)
            {
                if ((e & 1) == 1)
                    result *= power;
                e >>= 1;
                if (e > 0)
                    power *= power;
            }
        }
        return result;
    }
}

