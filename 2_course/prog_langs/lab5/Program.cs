using System;
using System;
using System.Globalization;

namespace Lab5;

internal static class Program
{
    private const string Prompt = "> ";

    public static void Main()
    {
        var interpreter = new Interpreter();

        while (true)
        {
            Console.Write(Prompt);
            var line = Console.ReadLine();
            if (line == null)
                break;

            line = line.Trim();
            if (line.Length == 0)
                continue;

            try
            {
                if (line.StartsWith("expr ", StringComparison.OrdinalIgnoreCase))
                {
                    var exprText = line.Substring(5);
                    interpreter.SetExpression(exprText);
                    Console.WriteLine("выражение установлено");
                }
                else if (line.StartsWith("set ", StringComparison.OrdinalIgnoreCase))
                {
                    var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                    if (parts.Length != 3)
                        throw new InvalidOperationException("формат: set <имя> <значение>");

                    var name = parts[1];
                    if (!long.TryParse(parts[2], NumberStyles.Integer, CultureInfo.InvariantCulture, out var value))
                        throw new InvalidOperationException("значение должно быть 64-битным целым");

                    interpreter.SetVariable(name, value);
                    Console.WriteLine($"{name} = {value}");
                }
                else if (string.Equals(line, "do", StringComparison.OrdinalIgnoreCase))
                {
                    foreach (var result in interpreter.Evaluate())
                        Console.WriteLine(result);
                }
                else if (string.Equals(line, "exit", StringComparison.OrdinalIgnoreCase))
                {
                    break;
                }
                else
                {
                    Console.WriteLine("неизвестная команда: используйте expr|set|do|exit");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"ошибка: {ex.Message}");
            }
        }
    }
}
