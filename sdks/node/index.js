"use strict";
/**
 * b4n1-notary SDK — authorship integrity and sealing.
 *
 * Thin Node wrapper around the b4n1-notary binary. The package bundles the
 * engine for every supported platform and resolves the matching one at call
 * time (one binary, N wrappers).
 *
 * Override: B4N1NOTARY_BIN_PATH=/path/to/b4n1-notary
 */

const { spawnSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const SDK_VERSION = "0.2.1";

const PLATFORM_BINARIES = {
  "linux-x64": "b4n1notary-linux-amd64",
  "linux-arm64": "b4n1notary-linux-arm64",
  "linux-ia32": "b4n1notary-linux-ia32",
  "darwin-x64": "b4n1notary-macos-x64",
  "darwin-arm64": "b4n1notary-macos-arm64",
  "win32-x64": "b4n1notary-windows-amd64.exe",
  "win32-ia32": "b4n1notary-windows-ia32.exe",
};

function platformBinaryName() {
  return PLATFORM_BINARIES[`${process.platform}-${process.arch}`] || null;
}

function isExecutable(file) {
  try {
    fs.accessSync(file, fs.constants.X_OK);
    return true;
  } catch (_) {
    return false;
  }
}

function getNotaryBinary() {
  const exact = process.env.B4N1NOTARY_BIN_PATH;
  if (exact && fs.existsSync(exact) && isExecutable(exact)) return exact;

  const name = platformBinaryName();
  if (name) {
    const bundled = path.join(__dirname, "bin", name);
    if (fs.existsSync(bundled) && isExecutable(bundled)) return bundled;
  }

  const onPath = (process.env.PATH || "")
    .split(path.delimiter)
    .filter(Boolean)
    .map((dir) => path.join(dir, process.platform === "win32" ? "b4n1-notary.exe" : "b4n1-notary"))
    .find((candidate) => fs.existsSync(candidate) && isExecutable(candidate));
  return onPath || null;
}

class NotaryClient {
  constructor(binaryPath) {
    this.binary = binaryPath || getNotaryBinary();
    if (!this.binary) {
      throw new Error(
        "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install the binary."
      );
    }
  }

  _run(args, timeoutMs = 120000) {
    const result = spawnSync(this.binary, args, {
      encoding: "utf8",
      timeout: timeoutMs,
    });
    return {
      exitCode: result.status === null ? -1 : result.status,
      stdout: result.stdout || "",
      stderr: result.stderr || "",
      ok: result.status === 0,
    };
  }

  stamp(projectPath = ".", identity = null) {
    const args = ["stamp", "--path", projectPath];
    if (identity) args.push("--identity", identity);
    return this._run(args);
  }

  verify(projectPath, proofPath) {
    return this._run(["verify", "--path", projectPath, "--proof", proofPath]);
  }

  verifyOts(projectPath, proofPath, opts = {}) {
    const args = ["verify-ots", "--path", projectPath, "--proof", proofPath];
    if (opts.checkCalendar) args.push("--check-calendar");
    if (opts.header) args.push("--header", opts.header);
    return this._run(args);
  }

  history(projectPath = ".") {
    return this._run(["history", "--path", projectPath]);
  }

  license(action = null, key = null, json = false) {
    const args = ["license"];
    if (action) args.push(action);
    if (key) args.push(key);
    if (json) args.push("--json");
    return this._run(args);
  }
}

module.exports = {
  SDK_VERSION,
  NotaryClient,
  getNotaryBinary,
  platformBinaryName,
};
