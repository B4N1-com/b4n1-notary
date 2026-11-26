using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace B4n1.Notary
{
    /// <summary>
    /// b4n1-notary SDK — authorship integrity and sealing.
    /// Thin wrapper around the b4n1-notary binary (bundled per platform).
    /// Override the engine with B4N1NOTARY_BIN_PATH.
    /// </summary>
    public sealed class NotaryClient
    {
        public const string SdkVersion = "0.2.1";

        public sealed class Result
        {
            public int ExitCode { get; }
            public string Stdout { get; }
            public string Stderr { get; }
            public bool Ok => ExitCode == 0;

            internal Result(int exitCode, string stdout, string stderr)
            {
                ExitCode = exitCode;
                Stdout = stdout;
                Stderr = stderr;
            }
        }

        private readonly string _binary;

        public NotaryClient() : this(ResolveBinary()) { }

        public NotaryClient(string binaryPath)
        {
            if (string.IsNullOrEmpty(binaryPath))
                throw new InvalidOperationException(
                    "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install the binary.");
            _binary = binaryPath;
        }

        public static string ResolveBinary()
        {
            var exact = Environment.GetEnvironmentVariable("B4N1NOTARY_BIN_PATH");
            if (!string.IsNullOrEmpty(exact) && File.Exists(exact))
                return exact;

            string name = null;
            if (IsWindows())
                name = "b4n1notary-windows-amd64.exe";
            else if (IsMac())
                name = Environment.Is64BitProcess && IsArm() ? "b4n1notary-macos-arm64" : "b4n1notary-macos-x64";
            else
                name = IsArm() ? "b4n1notary-linux-arm64" : "b4n1notary-linux-amd64";

            var bundled = Path.Combine(AppContext.BaseDirectory, "native", name);
            if (File.Exists(bundled))
                return bundled;
            return null;
        }

        private static bool IsWindows() => Environment.OSVersion.Platform == PlatformID.Win32NT;
        private static bool IsMac() => Environment.OSVersion.Platform == PlatformID.Unix &&
                                       Directory.Exists("/System/Library");
        private static bool IsArm() =>
            System.Runtime.InteropServices.RuntimeInformation.ProcessArchitecture.ToString() == "Arm64";

        private static string Quote(string value)
        {
            if (value.Length > 0 && value.IndexOfAny(new[] { ' ', '\t', '"' }) < 0)
                return value;
            var sb = new StringBuilder("\"");
            foreach (var ch in value)
            {
                if (ch == '"') sb.Append('\\');
                sb.Append(ch);
            }
            return sb.Append('"').ToString();
        }

        private Result Run(params string[] args)
        {
            var info = new ProcessStartInfo(_binary)
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            // netstandard2.0 has no ProcessStartInfo.ArgumentList: build the
            // command line with explicit quoting instead.
            info.Arguments = string.Join(" ", Array.ConvertAll(args, Quote));

            using var process = Process.Start(info);
            var stdout = process.StandardOutput.ReadToEnd();
            var stderr = process.StandardError.ReadToEnd();
            process.WaitForExit();
            return new Result(process.ExitCode, stdout, stderr);
        }

        public Result Stamp(string path, string identity = null)
        {
            var args = new List<string> { "stamp", "--path", path };
            if (!string.IsNullOrEmpty(identity))
            {
                args.Add("--identity");
                args.Add(identity);
            }
            return Run(args.ToArray());
        }

        public Result Verify(string path, string proof) =>
            Run("verify", "--path", path, "--proof", proof);

        public Result VerifyOts(string path, string proof, bool checkCalendar = false, string header = null)
        {
            var args = new List<string> { "verify-ots", "--path", path, "--proof", proof };
            if (checkCalendar) args.Add("--check-calendar");
            if (!string.IsNullOrEmpty(header))
            {
                args.Add("--header");
                args.Add(header);
            }
            return Run(args.ToArray());
        }

        public Result History(string path) => Run("history", "--path", path);

        public Result License(string action = null, string key = null, bool json = false)
        {
            var args = new List<string> { "license" };
            if (!string.IsNullOrEmpty(action)) args.Add(action);
            if (!string.IsNullOrEmpty(key)) args.Add(key);
            if (json) args.Add("--json");
            return Run(args.ToArray());
        }
    }
}
