package com.b4n1.notary;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Offline suite for the b4n1-notary Java SDK (real binary, no network). */
public final class NotaryTest {

    private static final List<Boolean> CHECKS = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        NotaryClient client = new NotaryClient();

        check("stamp seals a project", () -> {
            Path dir = project();
            NotaryClient.Result res = client.stamp(dir.toString(), "sdk-test");
            if (!res.ok()) {
                throw new IllegalStateException(res.stderr);
            }
            proofOf(dir);
        });

        check("verify accepts a fresh proof", () -> {
            Path dir = project();
            if (!client.stamp(dir.toString(), null).ok()) {
                throw new IllegalStateException("stamp failed");
            }
            NotaryClient.Result res = client.verify(dir.toString(), proofOf(dir).toString());
            if (!res.ok()) {
                throw new IllegalStateException(res.stderr);
            }
        });

        check("verify detects modified content", () -> {
            Path dir = project();
            client.stamp(dir.toString(), null);
            Path proof = proofOf(dir);
            Files.writeString(dir.resolve("file.txt"), "tampered\n");
            if (client.verify(dir.toString(), proof.toString()).ok()) {
                throw new IllegalStateException("a modified project verified");
            }
        });

        check("history lists the proof", () -> {
            Path dir = project();
            client.stamp(dir.toString(), null);
            NotaryClient.Result res = client.history(dir.toString());
            if (!res.ok() || !res.stdout.contains("b4n1-proof")) {
                throw new IllegalStateException(res.stderr.isEmpty() ? "no proof in history" : res.stderr);
            }
        });

        check("license status is readable JSON", () -> {
            NotaryClient.Result res = client.license("status", null, true);
            if (!res.ok() || !res.stdout.contains("community")) {
                throw new IllegalStateException(res.stderr);
            }
        });

        long failed = CHECKS.stream().filter(ok -> !ok).count();
        System.out.println();
        System.out.println("b4n1-notary java SDK: " + (CHECKS.size() - failed) + "/" + CHECKS.size());
        if (failed > 0) {
            System.exit(1);
        }
    }

    private interface Check {
        void run() throws Exception;
    }

    private static void check(String name, Check check) {
        try {
            check.run();
            System.out.println("  ✅ " + name);
            CHECKS.add(true);
        } catch (Exception e) {
            System.out.println("  ❌ " + name + ": " + e.getMessage());
            CHECKS.add(false);
        }
    }

    private static Path project() throws Exception {
        Path dir = Files.createTempDirectory("notary-sdk-java-");
        Files.writeString(dir.resolve("file.txt"), "hello from the java sdk suite\n");
        return dir;
    }

    private static Path proofOf(Path dir) throws Exception {
        try (var stream = Files.list(dir.resolve(".b4n1").resolve("proofs"))) {
            return stream.filter(p -> p.toString().endsWith(".b4n1-proof")).findFirst()
                    .orElseThrow(() -> new IllegalStateException("no proof written"));
        }
    }
}
