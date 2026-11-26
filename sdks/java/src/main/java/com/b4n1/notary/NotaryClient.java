package com.b4n1.notary;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * b4n1-notary SDK — authorship integrity and sealing.
 *
 * <p>Thin Java wrapper around the b4n1-notary binary (bundled per platform).
 * Override the engine with {@code B4N1NOTARY_BIN_PATH}.
 */
public final class NotaryClient {

    public static final String SDK_VERSION = "0.2.1";

    /** Outcome of one notary command. */
    public static final class Result {
        public final int exitCode;
        public final String stdout;
        public final String stderr;

        Result(int exitCode, String stdout, String stderr) {
            this.exitCode = exitCode;
            this.stdout = stdout;
            this.stderr = stderr;
        }

        public boolean ok() {
            return exitCode == 0;
        }
    }

    private final String binary;

    public NotaryClient() {
        this(resolveBinary());
    }

    public NotaryClient(String binaryPath) {
        if (binaryPath == null) {
            throw new IllegalStateException(
                    "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install the binary.");
        }
        this.binary = binaryPath;
    }

    /** Resolves the engine: explicit override, bundled binary, then PATH. */
    public static String resolveBinary() {
        String exact = System.getenv("B4N1NOTARY_BIN_PATH");
        if (exact != null && new File(exact).canExecute()) {
            return exact;
        }
        String os = System.getProperty("os.name").toLowerCase(Locale.ROOT);
        String arch = System.getProperty("os.arch").toLowerCase(Locale.ROOT);
        String name = null;
        if (os.contains("linux")) {
            name = arch.contains("aarch64") ? "b4n1notary-linux-arm64" : "b4n1notary-linux-amd64";
        } else if (os.contains("mac")) {
            name = arch.contains("aarch64") ? "b4n1notary-macos-arm64" : "b4n1notary-macos-x64";
        } else if (os.contains("win")) {
            name = "b4n1notary-windows-amd64.exe";
        }
        if (name != null) {
            File bundled = new File("native", name);
            if (bundled.canExecute()) {
                return bundled.getAbsolutePath();
            }
        }
        for (String dir : System.getenv().getOrDefault("PATH", "").split(File.pathSeparator)) {
            if (dir.isEmpty()) {
                continue;
            }
            File candidate = new File(dir, "b4n1-notary");
            if (candidate.canExecute()) {
                return candidate.getAbsolutePath();
            }
        }
        return null;
    }

    private Result run(List<String> args) {
        List<String> command = new ArrayList<>();
        command.add(binary);
        command.addAll(args);
        try {
            Process process = new ProcessBuilder(command).start();
            String stdout = readAll(process.getInputStream());
            String stderr = readAll(process.getErrorStream());
            int code = process.waitFor();
            return new Result(code, stdout, stderr);
        } catch (Exception e) {
            return new Result(-1, "", e.getMessage());
        }
    }

    private static String readAll(InputStream in) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int read;
        while ((read = in.read(buffer)) != -1) {
            out.write(buffer, 0, read);
        }
        return out.toString(StandardCharsets.UTF_8);
    }

    public Result stamp(String path, String identity) {
        List<String> args = new ArrayList<>(List.of("stamp", "--path", path));
        if (identity != null) {
            args.add("--identity");
            args.add(identity);
        }
        return run(args);
    }

    public Result verify(String path, String proof) {
        return run(List.of("verify", "--path", path, "--proof", proof));
    }

    public Result verifyOts(String path, String proof, boolean checkCalendar, String header) {
        List<String> args = new ArrayList<>(List.of("verify-ots", "--path", path, "--proof", proof));
        if (checkCalendar) {
            args.add("--check-calendar");
        }
        if (header != null) {
            args.add("--header");
            args.add(header);
        }
        return run(args);
    }

    public Result history(String path) {
        return run(List.of("history", "--path", path));
    }

    public Result license(String action, String key, boolean json) {
        List<String> args = new ArrayList<>();
        args.add("license");
        if (action != null) {
            args.add(action);
        }
        if (key != null) {
            args.add(key);
        }
        if (json) {
            args.add("--json");
        }
        return run(args);
    }
}
