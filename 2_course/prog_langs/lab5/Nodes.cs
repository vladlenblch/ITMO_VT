using System.Globalization;

namespace Lab5;

internal abstract class Node
{
    public long? CachedValue { get; set; }
    public abstract string ToInfix();
}

internal sealed class ConstantNode(long value) : Node
{
    public long Value { get; } = value;
    public override string ToInfix() => Value.ToString(CultureInfo.InvariantCulture);
}

internal sealed class VariableNode(string name) : Node
{
    public string Name { get; } = name;
    public override string ToInfix() => Name;
}

internal sealed class BinaryNode(TokenType op, Node left, Node right) : Node
{
    public TokenType Op { get; } = op;
    public Node Left { get; } = left;
    public Node Right { get; } = right;

    public override string ToInfix()
    {
        var leftStr = Left is BinaryNode lb && Precedence(lb.Op) < Precedence(Op)
            ? $"({Left.ToInfix()})"
            : Left.ToInfix();
        var rightNeedsParens = Right is BinaryNode rb &&
                               (Precedence(rb.Op) < Precedence(Op) ||
                               (Precedence(rb.Op) == Precedence(Op) && Op == TokenType.Pow));
        var rightStr = rightNeedsParens ? $"({Right.ToInfix()})" : Right.ToInfix();
        var opStr = Op switch
        {
            TokenType.Plus => "+",
            TokenType.Minus => "-",
            TokenType.Mul => "*",
            TokenType.Div => "/",
            TokenType.Pow => "**",
            _ => "?"
        };
        return $"{leftStr}{opStr}{rightStr}";
    }

    private static int Precedence(TokenType t) => t switch
    {
        TokenType.Plus or TokenType.Minus => 1,
        TokenType.Mul or TokenType.Div => 2,
        TokenType.Pow => 3,
        _ => 0
    };
}

