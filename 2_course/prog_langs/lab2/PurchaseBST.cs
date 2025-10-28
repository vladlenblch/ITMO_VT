using System.Collections.Generic;
using System.Linq;

namespace lab2;

public class PurchaseBST
{
    private class BSTNode
    {
        public Purchase Data = null!;
        public BSTNode? Left;
        public BSTNode? Right;
    }

    private BSTNode? _root;
    private int _size;

    public int Count => _size;
    public bool IsEmpty => _size == 0;

    public PurchaseBST()
    {
        _root = null;
        _size = 0;
    }

    public void Insert(Purchase purchase)
    {
        if (purchase == null)
            throw new ArgumentNullException(nameof(purchase));

        _root = InsertNode(_root, purchase);
        _size++;
    }

    private BSTNode InsertNode(BSTNode? node, Purchase purchase)
    {
        if (node == null)
        {
            return new BSTNode { Data = purchase };
        }

        int cmp = CompareDates(purchase, node.Data);
        if (cmp < 0)
        {
            node.Left = InsertNode(node.Left, purchase);
        }
        else
        {
            node.Right = InsertNode(node.Right, purchase);
        }

        return node;
    }

    public bool RemoveByIndex(int index)
    {
        int current = 0;
        return RemoveByIndexInternal(ref _root, index, ref current);
    }

    private bool RemoveByIndexInternal(ref BSTNode? node, int targetIndex, ref int current)
    {
        if (node == null)
            return false;

        if (RemoveByIndexInternal(ref node.Left, targetIndex, ref current))
            return true;

        if (current == targetIndex)
        {
            if (node.Left == null)
            {
                node = node.Right;
            }
            else if (node.Right == null)
            {
                node = node.Left;
            }
            else
            {
                var min = node.Right;
                while (min.Left != null)
                    min = min.Left;

                node.Data = min.Data;
                
                int dummy = 0;
                RemoveByIndexInternal(ref node.Right, 0, ref dummy);
            }

            _size--;
            return true;
        }

        current++;
        return RemoveByIndexInternal(ref node.Right, targetIndex, ref current);
    }

    public IEnumerable<Purchase> GetAllInOrder()
    {
        return InOrderTraversal(_root);
    }

    private IEnumerable<Purchase> InOrderTraversal(BSTNode? node)
    {
        if (node == null)
            yield break;

        foreach (var purchase in InOrderTraversal(node.Left))
            yield return purchase;

        yield return node.Data;

        foreach (var purchase in InOrderTraversal(node.Right))
            yield return purchase;
    }

    public IEnumerable<(Purchase Purchase, int Index)> GetInRange(
        int fromDay, int fromMonth, int fromYear,
        int toDay, int toMonth, int toYear)
    {
        var fromDate = new DateTime(fromYear, fromMonth, fromDay);
        var toDate = new DateTime(toYear, toMonth, toDay);

        return GetAllInOrder()
            .Select((p, idx) => (p, idx))
            .Where(x => IsInRange(x.p, fromDate, toDate));
    }

    private static bool IsInRange(Purchase purchase, DateTime from, DateTime to)
    {
        var date = purchase.GetDate();
        return date >= from && date <= to;
    }

    private static int CompareDates(Purchase a, Purchase b)
    {
        if (a.Year != b.Year)
            return a.Year.CompareTo(b.Year);
        if (a.Month != b.Month)
            return a.Month.CompareTo(b.Month);
        return a.Day.CompareTo(b.Day);
    }

    public void Clear()
    {
        _root = null;
        _size = 0;
    }

    public double GetTotalAmount()
    {
        return GetAllInOrder().Sum(p => p.Amount);
    }

    public IEnumerable<Purchase> GetByYear(int year)
    {
        return GetAllInOrder().Where(p => p.Year == year);
    }

    public Purchase? GetMostExpensivePurchase()
    {
        return GetAllInOrder()
            .OrderByDescending(p => p.Amount)
            .FirstOrDefault();
    }

    public bool HasExpensivePurchases(double threshold)
    {
        return GetAllInOrder().Any(p => p.Amount > threshold);
    }
}
