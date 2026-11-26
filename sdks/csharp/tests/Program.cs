using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using B4n1.Notary;

namespace B4n1.Notary.Tests
{
    /// <summary>Offline suite for the b4n1-notary C# SDK (real binary, no network).</summary>
    public static class Program
    {
        private static readonly List<bool> Checks = new List<bool>();

        public static int Main(string[] args)
        {
            var client = new NotaryClient();

            Check("stamp seals a project", () =>
            {
                var dir = Project();
                var res = client.Stamp(dir, "sdk-test");
                if (!res.Ok) throw new InvalidOperationException(res.Stderr);
                ProofOf(dir);
            });

            Check("verify accepts a fresh proof", () =>
            {
                var dir = Project();
                if (!client.Stamp(dir).Ok) throw new InvalidOperationException("stamp failed");
                var res = client.Verify(dir, ProofOf(dir));
                if (!res.Ok) throw new InvalidOperationException(res.Stderr);
            });

            Check("verify detects modified content", () =>
            {
                var dir = Project();
                client.Stamp(dir);
                var proof = ProofOf(dir);
                File.WriteAllText(Path.Combine(dir, "file.txt"), "tampered\n");
                if (client.Verify(dir, proof).Ok) throw new InvalidOperationException("a modified project verified");
            });

            Check("history lists the proof", () =>
            {
                var dir = Project();
                client.Stamp(dir);
                var res = client.History(dir);
                if (!res.Ok || !res.Stdout.Contains("b4n1-proof"))
                    throw new InvalidOperationException(string.IsNullOrEmpty(res.Stderr) ? "no proof in history" : res.Stderr);
            });

            Check("license status is readable JSON", () =>
            {
                var res = client.License("status", null, true);
                if (!res.Ok || !res.Stdout.Contains("community"))
                    throw new InvalidOperationException(res.Stderr);
            });

            var failed = Checks.Count(ok => !ok);
            Console.WriteLine();
            Console.WriteLine($"b4n1-notary csharp SDK: {Checks.Count - failed}/{Checks.Count}");
            return failed == 0 ? 0 : 1;
        }

        private static void Check(string name, Action action)
        {
            try
            {
                action();
                Console.WriteLine($"  ✅ {name}");
                Checks.Add(true);
            }
            catch (Exception e)
            {
                Console.WriteLine($"  ❌ {name}: {e.Message}");
                Checks.Add(false);
            }
        }

        private static string Project()
        {
            var dir = Path.Combine(Path.GetTempPath(), "notary-sdk-cs-" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(dir);
            File.WriteAllText(Path.Combine(dir, "file.txt"), "hello from the csharp sdk suite\n");
            return dir;
        }

        private static string ProofOf(string dir)
        {
            var proofs = Directory.GetFiles(Path.Combine(dir, ".b4n1", "proofs"), "*.b4n1-proof");
            if (proofs.Length == 0) throw new InvalidOperationException("no proof written");
            return proofs[0];
        }
    }
}
