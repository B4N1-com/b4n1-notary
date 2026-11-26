"use strict";
/**
 * Offline suite for the b4n1-notary Node SDK.
 * Runs against the real binary (bundled or B4N1NOTARY_BIN_PATH).
 */

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { NotaryClient, getNotaryBinary } = require("../index.js");

const binary = getNotaryBinary();
if (!binary) {
  console.error("b4n1-notary binary not found");
  process.exit(1);
}
const client = new NotaryClient(binary);

function makeProject() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "notary-sdk-node-"));
  fs.writeFileSync(path.join(dir, "file.txt"), "hello from the node sdk suite\n");
  return dir;
}

function proofFile(dir) {
  const proofsDir = path.join(dir, ".b4n1", "proofs");
  const names = fs.readdirSync(proofsDir).filter((n) => n.endsWith(".b4n1-proof"));
  return path.join(proofsDir, names[0]);
}

const checks = [];
function check(name, fn) {
  try {
    fn();
    console.log(`  ✅ ${name}`);
    checks.push(true);
  } catch (err) {
    console.error(`  ❌ ${name}: ${err.message}`);
    checks.push(false);
  }
}

check("stamp seals a project", () => {
  const dir = makeProject();
  const res = client.stamp(dir, "sdk-test");
  assert.ok(res.ok, res.stderr);
  assert.ok(fs.existsSync(proofFile(dir)), "a .b4n1-proof must be written");
});

check("verify accepts a fresh proof", () => {
  const dir = makeProject();
  assert.ok(client.stamp(dir).ok);
  const res = client.verify(dir, proofFile(dir));
  assert.ok(res.ok, res.stderr);
});

check("verify detects modified content", () => {
  const dir = makeProject();
  assert.ok(client.stamp(dir).ok);
  const proof = proofFile(dir);
  fs.writeFileSync(path.join(dir, "file.txt"), "tampered\n");
  const res = client.verify(dir, proof);
  assert.strictEqual(res.ok, false, "a modified project must not verify");
});

check("history lists the proof", () => {
  const dir = makeProject();
  assert.ok(client.stamp(dir).ok);
  const res = client.history(dir);
  assert.ok(res.ok, res.stderr);
  assert.ok(res.stdout.includes("b4n1-proof"));
});

check("license status is readable JSON", () => {
  const res = client.license("status", null, true);
  assert.ok(res.ok, res.stderr);
  assert.ok(res.stdout.includes("community"));
});

const failed = checks.filter((ok) => !ok).length;
console.log(`\nb4n1-notary node SDK: ${checks.length - failed}/${checks.length}`);
process.exit(failed === 0 ? 0 : 1);
