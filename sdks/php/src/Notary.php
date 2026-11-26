<?php

declare(strict_types=1);

namespace B4N1\Notary;

/**
 * b4n1-notary SDK — authorship integrity and sealing.
 *
 * Thin PHP wrapper around the b4n1-notary binary (bundled per platform).
 * Override: B4N1NOTARY_BIN_PATH=/path/to/b4n1-notary
 */
final class Client
{
    public const SDK_VERSION = '0.2.1';

    private const PLATFORM_BINARIES = [
        'Linux-x86_64' => 'b4n1notary-linux-amd64',
        'Linux-aarch64' => 'b4n1notary-linux-arm64',
        'Darwin-x86_64' => 'b4n1notary-macos-x64',
        'Darwin-arm64' => 'b4n1notary-macos-arm64',
        'Windows-AMD64' => 'b4n1notary-windows-amd64.exe',
    ];

    private string $binary;

    public function __construct(?string $binaryPath = null)
    {
        $binary = $binaryPath ?? self::resolveBinary();
        if ($binary === null) {
            throw new \RuntimeException(
                'b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install the binary.'
            );
        }
        $this->binary = $binary;
    }

    public static function resolveBinary(): ?string
    {
        $exact = getenv('B4N1NOTARY_BIN_PATH');
        if ($exact !== false && $exact !== '' && is_executable($exact)) {
            return $exact;
        }

        $key = PHP_OS_FAMILY . '-' . php_uname('m');
        $name = self::PLATFORM_BINARIES[$key] ?? null;
        if ($name !== null) {
            $bundled = dirname(__DIR__) . '/bin/' . $name;
            if (is_executable($bundled)) {
                return $bundled;
            }
        }

        foreach (explode(PATH_SEPARATOR, (string) getenv('PATH')) as $dir) {
            if ($dir === '') {
                continue;
            }
            $candidate = $dir . '/b4n1-notary';
            if (is_executable($candidate)) {
                return $candidate;
            }
        }
        return null;
    }

    /** @param list<string> $args */
    private function run(array $args): array
    {
        $descriptors = [1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
        $process = proc_open(array_merge([$this->binary], $args), $descriptors, $pipes);
        if (!is_resource($process)) {
            throw new \RuntimeException('could not start b4n1-notary');
        }
        $stdout = stream_get_contents($pipes[1]) ?: '';
        $stderr = stream_get_contents($pipes[2]) ?: '';
        fclose($pipes[1]);
        fclose($pipes[2]);
        $code = proc_close($process);
        return ['exit_code' => $code, 'stdout' => $stdout, 'stderr' => $stderr, 'ok' => $code === 0];
    }

    public function stamp(string $path = '.', ?string $identity = null): array
    {
        $args = ['stamp', '--path', $path];
        if ($identity !== null) {
            $args[] = '--identity';
            $args[] = $identity;
        }
        return $this->run($args);
    }

    public function verify(string $path, string $proof): array
    {
        return $this->run(['verify', '--path', $path, '--proof', $proof]);
    }

    public function verifyOts(string $path, string $proof, bool $checkCalendar = false, ?string $header = null): array
    {
        $args = ['verify-ots', '--path', $path, '--proof', $proof];
        if ($checkCalendar) {
            $args[] = '--check-calendar';
        }
        if ($header !== null) {
            $args[] = '--header';
            $args[] = $header;
        }
        return $this->run($args);
    }

    public function history(string $path = '.'): array
    {
        return $this->run(['history', '--path', $path]);
    }

    public function license(?string $action = null, ?string $key = null, bool $json = false): array
    {
        $args = ['license'];
        if ($action !== null) {
            $args[] = $action;
        }
        if ($key !== null) {
            $args[] = $key;
        }
        if ($json) {
            $args[] = '--json';
        }
        return $this->run($args);
    }
}
