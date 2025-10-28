using System.IO;
using System.Linq;

namespace lab2;

public class PurchaseManager
{
    private static readonly string DataFileName = "purchases.txt";
    private PurchaseBST _bst;

    public PurchaseManager()
    {
        _bst = new PurchaseBST();
        LoadFromFile();
    }

    public void AddPurchase(Purchase purchase)
    {
        _bst.Insert(purchase);
        SaveToFile();
    }

    public bool RemovePurchase(int index)
    {
        bool result = _bst.RemoveByIndex(index);
        if (result)
        {
            SaveToFile();
        }
        return result;
    }

    public void PrintAllPurchases()
    {
        var purchases = _bst.GetAllInOrder().ToList();
        Console.WriteLine("\nall purchases:");
        
        if (purchases.Count == 0)
        {
            Console.WriteLine("no purchases");
            return;
        }

        foreach (var (purchase, index) in purchases.Select((p, i) => (p, i + 1)))
        {
            purchase.Print(index);
        }
    }

    public void PrintPurchasesInRange(int fromDay, int fromMonth, int fromYear,
                                        int toDay, int toMonth, int toYear)
    {
        var purchasesInRange = _bst.GetInRange(fromDay, fromMonth, fromYear, toDay, toMonth, toYear).ToList();
        
        Console.WriteLine("\npurchases in selected interval:");
        
        if (purchasesInRange.Count == 0)
        {
            Console.WriteLine("no purchases in selected interval");
            return;
        }

        foreach (var (purchase, index) in purchasesInRange.Select(x => (x.Purchase, x.Index + 1)))
        {
            purchase.Print(index);
        }
    }

    public void SaveToFile()
    {
        try
        {
            var purchases = _bst.GetAllInOrder().ToList();
            
            string fullPath = Path.GetFullPath(DataFileName);
            
            var lines = purchases.Select(p => p.ToFileString());
            File.WriteAllLines(fullPath, lines);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"error saving to file: {ex.Message}");
        }
    }

    public void LoadFromFile()
    {
        try
        {
            string fullPath = Path.GetFullPath(DataFileName);
            
            if (!File.Exists(fullPath))
            {
                Console.WriteLine("data file not found - starting with empty database");
                return;
            }

            _bst.Clear();
            
            var lines = File.ReadAllLines(fullPath);
            
            var validPurchases = lines
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line =>
                {
                    try
                    {
                        return Purchase.FromFileString(line);
                    }
                    catch (FormatException ex)
                    {
                        Console.WriteLine($"warning: skipping invalid line - {ex.Message}");
                        return (Purchase?)null;
                    }
                })
                .Where(p => p != null);

            foreach (var purchase in validPurchases)
            {
                _bst.Insert(purchase!);
            }

            if (_bst.Count > 0)
            {
                Console.WriteLine($"loaded {_bst.Count} purchases from file");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"error loading from file - {ex.Message}");
        }
    }
}
