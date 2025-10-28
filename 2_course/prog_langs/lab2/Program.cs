using lab2;

class Program
{
    static bool IsValidDate(int day, int month, int year)
    {
        if (year < 1 || month < 1 || month > 12 || day < 1)
            return false;

        int[] daysInMonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
        bool isLeapYear = (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0));

        if (isLeapYear && month == 2)
        {
            if (day > 29) return false;
        }
        else
        {
            if (day > daysInMonth[month - 1]) return false;
        }

        return true;
    }

    static void PrintMenu()
    {
        Console.WriteLine();
        Console.WriteLine("menu:");
        Console.WriteLine("1. add purchase");
        Console.WriteLine("2. remove purchase by an index");
        Console.WriteLine("3. print purchases in date range");
        Console.WriteLine("4. print all purchases");
        Console.WriteLine("0. exit");
        Console.Write("choose: ");
    }

    static void Main()
    {
        var manager = new PurchaseManager();

        while (true)
        {
            PrintMenu();
            
            if (!int.TryParse(Console.ReadLine(), out int choice))
            {
                Console.WriteLine("enter a number\n");
                continue;
            }

            switch (choice)
            {
                case 0:
                    Console.WriteLine("\nexiting...\n");
                    return;

                case 1:
                    AddPurchase(manager);
                    break;

                case 2:
                    RemovePurchase(manager);
                    break;

                case 3:
                    PrintPurchasesInRange(manager);
                    break;

                case 4:
                    manager.PrintAllPurchases();
                    break;

                default:
                    Console.WriteLine("invalid choice - please try again\n");
                    break;
            }
        }
    }

    static void AddPurchase(PurchaseManager manager)
    {
        Console.Write("name: ");
        string? name = Console.ReadLine()?.Trim();
        if (string.IsNullOrEmpty(name))
        {
            Console.WriteLine("name cannot be empty\n");
            return;
        }

        Console.Write("comment: ");
        string? comment = Console.ReadLine()?.Trim();
        if (string.IsNullOrEmpty(comment))
        {
            Console.WriteLine("comment cannot be empty\n");
            return;
        }

        Console.Write("amount: ");
        if (!double.TryParse(Console.ReadLine(), out double amount))
        {
            Console.WriteLine("invalid amount\n");
            return;
        }

        int day, month, year;
        do
        {
            Console.Write("date (dd mm yyyy): ");
            string? dateInput = Console.ReadLine();
            var parts = dateInput?.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            
            if (parts == null || parts.Length != 3 ||
                !int.TryParse(parts[0], out day) ||
                !int.TryParse(parts[1], out month) ||
                !int.TryParse(parts[2], out year) ||
                !IsValidDate(day, month, year))
            {
                Console.WriteLine("incorrect date\n");
            }
            else
            {
                break;
            }
        } while (true);

        var purchase = new Purchase(name, comment, amount, day, month, year);
        manager.AddPurchase(purchase);
        Console.WriteLine("purchase added");
    }

    static void RemovePurchase(PurchaseManager manager)
    {
        Console.Write("enter a purchase index for removing: ");
        
        if (!int.TryParse(Console.ReadLine(), out int index))
        {
            Console.WriteLine("invalid index\n");
            return;
        }

        if (!manager.RemovePurchase(index - 1))
        {
            Console.WriteLine("no purchase with this index\n");
        }
        else
        {
            Console.WriteLine("purchase removed\n");
        }
    }

    static void PrintPurchasesInRange(PurchaseManager manager)
    {
        int fromDay, fromMonth, fromYear;
        do
        {
            Console.Write("enter a start of an interval (dd mm yyyy): ");
            string? input = Console.ReadLine();
            var parts = input?.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            
            if (parts == null || parts.Length != 3 ||
                !int.TryParse(parts[0], out fromDay) ||
                !int.TryParse(parts[1], out fromMonth) ||
                !int.TryParse(parts[2], out fromYear) ||
                !IsValidDate(fromDay, fromMonth, fromYear))
            {
                Console.WriteLine("incorrect date\n");
            }
            else
            {
                break;
            }
        } while (true);

        int toDay, toMonth, toYear;
        do
        {
            Console.Write("enter an end of an interval (dd mm yyyy): ");
            string? input = Console.ReadLine();
            var parts = input?.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            
            if (parts == null || parts.Length != 3 ||
                !int.TryParse(parts[0], out toDay) ||
                !int.TryParse(parts[1], out toMonth) ||
                !int.TryParse(parts[2], out toYear) ||
                !IsValidDate(toDay, toMonth, toYear))
            {
                Console.WriteLine("incorrect date\n");
            }
            else
            {
                break;
            }
        } while (true);

        manager.PrintPurchasesInRange(fromDay, fromMonth, fromYear, toDay, toMonth, toYear);
    }
}

