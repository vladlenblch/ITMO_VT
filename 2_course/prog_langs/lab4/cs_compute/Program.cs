using System.Buffers.Binary;
using System.Net;
using System.Net.Sockets;

namespace Compute;

internal static class Program
{
    // Balanced quality/perf for ~10 FPS.
    private const int Width = 480;
    private const int Height = 480;
    private const int Iterations = 56;
    private const float EscapeRadius = 8.0f;
    private const float EscapeRadiusSq = EscapeRadius * EscapeRadius;
    private const int Port = 5001;
    private const int TileRows = 16;
    private static readonly float[] XOffsets = BuildOffsets(Width);
    private static readonly float[] YOffsets = BuildOffsets(Height);

    private static void Main()
    {
        Console.CancelKeyPress += (_, args) =>
        {
            args.Cancel = true;
            Environment.Exit(0);
        };

        var listener = new TcpListener(IPAddress.Loopback, Port);
        listener.Start();
        Console.WriteLine($"Waiting for Python viewer on 127.0.0.1:{Port} ...");

        using var client = listener.AcceptTcpClient();
        Console.WriteLine("Viewer connected, streaming frames.");
        using var stream = client.GetStream();

        // We send iteration counts (1 byte/pixel) to shrink payload; Python applies palette/upscale.
        var frameBuffer = new byte[Width * Height]; // iteration counts (1 byte/pixel)
        var headerBuffer = new byte[12]; // width, height, payload

        float scale = 3.0f;
        float targetRe = -0.25f;
        float targetIm = 0.0f;
        var rng = new Random(0);

        while (true)
        {
            RenderFrame(frameBuffer, targetRe, targetIm, scale);
            // slower zoom to linger on details
            scale *= 0.9975f; // slower zoom to linger on details
            if (scale < 0.4f)
            {
                scale = 2.2f;
                targetRe += (float)((rng.NextDouble() - 0.5) * 0.6);
                targetIm += (float)((rng.NextDouble() - 0.5) * 0.6);
            }

            BinaryPrimitives.WriteInt32LittleEndian(headerBuffer.AsSpan(0, 4), Width);
            BinaryPrimitives.WriteInt32LittleEndian(headerBuffer.AsSpan(4, 4), Height);
            BinaryPrimitives.WriteInt32LittleEndian(headerBuffer.AsSpan(8, 4), frameBuffer.Length);

            stream.Write(headerBuffer, 0, headerBuffer.Length);
            stream.Write(frameBuffer, 0, frameBuffer.Length);
        }
    }

    private static void RenderFrame(byte[] buffer, float centerRe, float centerIm, float scale)
    {
        var dx = scale / (Width / 2.0f);
        var dy = scale / (Height / 2.0f);

        var tiles = (Height + TileRows - 1) / TileRows;
        Parallel.For(0, tiles, tile =>
        {
            var yStart = tile * TileRows;
            var yEnd = Math.Min(Height, yStart + TileRows);

            for (var y = yStart; y < yEnd; y++)
            {
                var imag = centerIm + YOffsets[y] * dy;
                var localOffset = y * Width;
                for (var x = 0; x < Width; x++)
                {
                    var real = centerRe + XOffsets[x] * dx;
                    var zr = real;
                    var zi = imag;
                    var iter = 0;

                    while (iter < Iterations)
                    {
                        var magSq = zr * zr + zi * zi;
                        if (magSq > EscapeRadiusSq)
                            break;

                        (zr, zi) = CollatzStep(zr, zi);
                        iter++;
                    }

                    buffer[localOffset++] = IterationToByte(zr, zi, iter);
                }
            }
        });
    }

    private static (float re, float im) CollatzStep(float re, float im)
    {
        // Optimized Collatz map: (1 + 4z - (1 + 2z) * cos(pi z)) / 4
        var piRe = MathF.PI * re;
        var piIm = MathF.PI * im;

        var cosRe = MathF.Cos(piRe) * MathF.Cosh(piIm);
        var cosIm = -MathF.Sin(piRe) * MathF.Sinh(piIm);

        var aRe = 1.0f + 2.0f * re;
        var aIm = 2.0f * im;

        var mulRe = aRe * cosRe - aIm * cosIm;
        var mulIm = aRe * cosIm + aIm * cosRe;

        var outRe = 0.25f * (1.0f + 4.0f * re - mulRe);
        var outIm = 0.25f * (4.0f * im - mulIm);
        return (outRe, outIm);
    }

    private static byte IterationToByte(float zr, float zi, int iter)
    {
        if (iter >= Iterations)
        {
            return 255; // marker for interior / max iteration
        }

        var magSq = zr * zr + zi * zi;
        var mag = MathF.Sqrt(magSq);
        var smooth = iter - MathF.Log(Math.Max(1e-9f, MathF.Log(mag))) / MathF.Log(2.0f);
        var norm = Math.Clamp(smooth / Iterations, 0.0f, 1.0f);
        return (byte)Math.Min(254, (int)(norm * 254.0f));
    }

    private static float[] BuildOffsets(int count)
    {
        var offsets = new float[count];
        var half = count / 2.0f;
        for (var i = 0; i < count; i++)
        {
            offsets[i] = i - half;
        }
        return offsets;
    }
}
