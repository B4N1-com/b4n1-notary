# frozen_string_literal: true

# Offline suite for the b4n1-notary Ruby SDK (real binary, no network).
$LOAD_PATH.unshift(File.expand_path("../lib", __dir__))
require "b4n1notary"
require "fileutils"
require "tmpdir"

client = B4N1Notary::Client.new
checks = []

def check(checks, name)
  yield
  puts "  ✅ #{name}"
  checks << true
rescue StandardError => e
  puts "  ❌ #{name}: #{e.message}"
  checks << false
end

def project
  dir = Dir.mktmpdir("notary-sdk-ruby-")
  File.write(File.join(dir, "file.txt"), "hello from the ruby sdk suite\n")
  dir
end

def proof_of(dir)
  Dir.glob(File.join(dir, ".b4n1", "proofs", "*.b4n1-proof")).first
end

check(checks, "stamp seals a project") do
  dir = project
  res = client.stamp(dir, identity: "sdk-test")
  raise res.stderr unless res.ok?
  raise "no proof written" unless proof_of(dir)
end

check(checks, "verify accepts a fresh proof") do
  dir = project
  raise "stamp failed" unless client.stamp(dir).ok?
  res = client.verify(dir, proof_of(dir))
  raise res.stderr unless res.ok?
end

check(checks, "verify detects modified content") do
  dir = project
  raise "stamp failed" unless client.stamp(dir).ok?
  proof = proof_of(dir)
  File.write(File.join(dir, "file.txt"), "tampered\n")
  raise "modified project verified" if client.verify(dir, proof).ok?
end

check(checks, "history lists the proof") do
  dir = project
  raise "stamp failed" unless client.stamp(dir).ok?
  res = client.history(dir)
  raise res.stderr unless res.ok?
  raise "no proof in history" unless res.stdout.include?("b4n1-proof")
end

check(checks, "license status is readable JSON") do
  res = client.license("status", json: true)
  raise res.stderr unless res.ok?
  raise "not community" unless res.stdout.include?("community")
end

failed = checks.count(false)
puts "\nb4n1-notary ruby SDK: #{checks.size - failed}/#{checks.size}"
exit(failed.zero? ? 0 : 1)
