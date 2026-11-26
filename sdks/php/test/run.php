<?php

declare(strict_types=1);

/** Offline suite for the b4n1-notary PHP SDK (real binary, no network). */

require __DIR__ . '/../src/Notary.php';

use B4N1\Notary\Client;

$checks = [];
function check(array &$checks, string $name, callable $fn): void
{
    try {
        $fn();
        echo "  ✅ $name\n";
        $checks[] = true;
    } catch (Throwable $e) {
        echo "  ❌ $name: {$e->getMessage()}\n";
        $checks[] = false;
    }
}

function project(): string
{
    $dir = sys_get_temp_dir() . '/notary-sdk-php-' . bin2hex(random_bytes(6));
    mkdir($dir, 0777, true);
    file_put_contents($dir . '/file.txt', "hello from the php sdk suite\n");
    return $dir;
}

function proofOf(string $dir): string
{
    $proofs = glob($dir . '/.b4n1/proofs/*.b4n1-proof');
    if (!$proofs) {
        throw new RuntimeException('no proof written');
    }
    return $proofs[0];
}

$client = new Client();

check($checks, 'stamp seals a project', function () use ($client): void {
    $dir = project();
    $res = $client->stamp($dir, 'sdk-test');
    if (!$res['ok']) {
        throw new RuntimeException($res['stderr']);
    }
    proofOf($dir);
});

check($checks, 'verify accepts a fresh proof', function () use ($client): void {
    $dir = project();
    $client->stamp($dir);
    $res = $client->verify($dir, proofOf($dir));
    if (!$res['ok']) {
        throw new RuntimeException($res['stderr']);
    }
});

check($checks, 'verify detects modified content', function () use ($client): void {
    $dir = project();
    $client->stamp($dir);
    $proof = proofOf($dir);
    file_put_contents($dir . '/file.txt', "tampered\n");
    if ($client->verify($dir, $proof)['ok']) {
        throw new RuntimeException('a modified project verified');
    }
});

check($checks, 'history lists the proof', function () use ($client): void {
    $dir = project();
    $client->stamp($dir);
    $res = $client->history($dir);
    if (!$res['ok'] || !str_contains($res['stdout'], 'b4n1-proof')) {
        throw new RuntimeException($res['stderr'] ?: 'no proof in history');
    }
});

check($checks, 'license status is readable JSON', function () use ($client): void {
    $res = $client->license('status', null, true);
    if (!$res['ok'] || !str_contains($res['stdout'], 'community')) {
        throw new RuntimeException($res['stderr'] ?: 'unexpected licence output');
    }
});

$failed = count(array_filter($checks, fn ($ok) => !$ok));
echo "\nb4n1-notary php SDK: " . (count($checks) - $failed) . '/' . count($checks) . "\n";
exit($failed === 0 ? 0 : 1);
