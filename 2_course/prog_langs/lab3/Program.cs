using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;

namespace lab3
{
    class Program
    {
        private static readonly ConcurrentQueue<OutputItem> _outputQueue = new();
        private static readonly object _outputLock = new object();
        private static int _activeTasks = 0;

        private class OutputItem
        {
            public long TimestampTicks { get; set; }
            public string Line { get; set; } = string.Empty;
        }

        static async Task Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.Error.WriteLine("Использование: lab3 <путь_к_программе1> [путь_к_программе2] ...");
                Environment.Exit(1);
            }

            var tasks = new List<Task>();

            for (int i = 0; i < args.Length; i++)
            {
                string programPath = args[i];
                tasks.Add(RunProgramAsync(programPath));
            }

            _activeTasks = tasks.Count;

            var outputTask = ProcessOutputQueueAsync();

            await Task.WhenAll(tasks);
            
            await outputTask;
        }

        static async Task RunProgramAsync(string programPath)
        {
            try
            {
                var processInfo = new ProcessStartInfo
                {
                    FileName = programPath,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = false,
                    CreateNoWindow = true
                };

                using var process = new Process { StartInfo = processInfo };
                
                process.Start();

                await ReadOutputAsync(process.StandardOutput);

                await process.WaitForExitAsync();
            }
            catch (Exception ex)
            {
                var errorItem = new OutputItem
                {
                    TimestampTicks = DateTime.UtcNow.Ticks,
                    Line = $"Ошибка при запуске программы '{programPath}': {ex.Message}"
                };
                _outputQueue.Enqueue(errorItem);
            }
            finally
            {
                System.Threading.Interlocked.Decrement(ref _activeTasks);
            }
        }

        static async Task ReadOutputAsync(StreamReader reader)
        {
            string? line;
            while ((line = await reader.ReadLineAsync()) != null)
            {
                var outputItem = new OutputItem
                {
                    TimestampTicks = DateTime.UtcNow.Ticks,
                    Line = line
                };
                _outputQueue.Enqueue(outputItem);
            }
        }

        static async Task ProcessOutputQueueAsync()
        {
            var pendingItems = new List<OutputItem>();

            while (_activeTasks > 0 || !_outputQueue.IsEmpty || pendingItems.Count > 0)
            {
                while (_outputQueue.TryDequeue(out var item))
                {
                    pendingItems.Add(item);
                }

                if (pendingItems.Count > 0)
                {
                    var sortedItems = pendingItems.OrderBy(x => x.TimestampTicks).ToList();
                    lock (_outputLock)
                    {
                        foreach (var item in sortedItems)
                        {
                            Console.WriteLine(item.Line);
                        }
                    }
                    pendingItems.Clear();
                }

                await Task.Delay(5);
            }
        }
    }
}
