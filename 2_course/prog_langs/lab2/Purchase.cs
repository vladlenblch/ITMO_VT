namespace lab2;

public class Purchase
{
    public string Name { get; set; } = string.Empty;
    public string Comment { get; set; } = string.Empty;
    public double Amount { get; set; }
    public int Day { get; set; }
    public int Month { get; set; }
    public int Year { get; set; }

    public Purchase() { }

    public Purchase(string name, string comment, double amount, int day, int month, int year)
    {
        Name = name;
        Comment = comment;
        Amount = amount;
        Day = day;
        Month = month;
        Year = year;
    }

    public DateTime GetDate()
    {
        return new DateTime(Year, Month, Day);
    }

    public string ToFileString()
    {
        return $"{Name}|{Comment}|{Amount}|{Day}|{Month}|{Year}";
    }

    public static Purchase FromFileString(string line)
    {
        var parts = line.Split('|');
        if (parts.Length != 6)
            throw new FormatException("invalid file format");

        return new Purchase(
            parts[0],
            parts[1],
            double.Parse(parts[2]),
            int.Parse(parts[3]),
            int.Parse(parts[4]),
            int.Parse(parts[5])
        );
    }

    public void Print(int index)
    {
        Console.WriteLine($"{index}. {Name} | {Comment} | {Amount:F2} | {Day:D2}.{Month:D2}.{Year:D4}");
    }
}
