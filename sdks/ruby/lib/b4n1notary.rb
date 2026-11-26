# frozen_string_literal: true

# b4n1-notary SDK — authorship integrity and sealing.
#
# Thin Ruby wrapper around the b4n1-notary binary (bundled per platform).
# Override: B4N1NOTARY_BIN_PATH=/path/to/b4n1-notary
require "open3"

module B4N1Notary
  SDK_VERSION = "0.2.1"

  # Ordered: the FIRST pattern that matches RUBY_PLATFORM wins.
  PLATFORM_BINARIES = [
    [/x86_64-linux/, "b4n1notary-linux-amd64"],
    [/aarch64-linux|arm64-linux/, "b4n1notary-linux-arm64"],
    [/i686-linux/, "b4n1notary-linux-ia32"],
    [/x86_64-darwin/, "b4n1notary-macos-x64"],
    [/arm64-darwin/, "b4n1notary-macos-arm64"],
    [/mingw32|mswin/, "b4n1notary-windows-amd64.exe"]
  ].freeze

  Result = Struct.new(:exit_code, :stdout, :stderr) do
    def ok?
      exit_code.zero?
    end
  end

  def self.platform_binary_name
    match = PLATFORM_BINARIES.find { |pattern, _| RUBY_PLATFORM.match?(pattern) }
    match && match[1]
  end

  def self.binary
    exact = ENV["B4N1NOTARY_BIN_PATH"]
    return exact if exact && File.file?(exact) && File.executable?(exact)

    name = platform_binary_name
    if name
      bundled = File.expand_path(File.join(__dir__, "..", "bin", name))
      return bundled if File.file?(bundled) && File.executable?(bundled)
    end

    ENV.fetch("PATH", "").split(File::PATH_SEPARATOR).each do |dir|
      candidate = File.join(dir, "b4n1-notary")
      return candidate if File.file?(candidate) && File.executable?(candidate)
    end
    nil
  end

  class Client
    def initialize(binary_path = nil)
      @binary = binary_path || B4N1Notary.binary
      raise "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH." unless @binary
    end

    def stamp(path = ".", identity: nil)
      args = ["stamp", "--path", path]
      args += ["--identity", identity] if identity
      run(*args)
    end

    def verify(path, proof)
      run("verify", "--path", path, "--proof", proof)
    end

    def verify_ots(path, proof, check_calendar: false, header: nil)
      args = ["verify-ots", "--path", path, "--proof", proof]
      args << "--check-calendar" if check_calendar
      args += ["--header", header] if header
      run(*args)
    end

    def history(path = ".")
      run("history", "--path", path)
    end

    def license(action = nil, key: nil, json: false)
      args = ["license"]
      args << action if action
      args << key if key
      args << "--json" if json
      run(*args)
    end

    private

    def run(*args)
      stdout, stderr, status = Open3.capture3(@binary, *args)
      Result.new(status.exitstatus || -1, stdout, stderr)
    end
  end
end
