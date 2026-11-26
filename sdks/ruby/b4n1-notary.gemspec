# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = "b4n1-notary"
  spec.version = "0.2.1"
  spec.authors = ["Bani Montoya"]
  spec.email = ["banimontoya@gmail.com"]

  spec.summary = "Authorship integrity and sealing: stamp, verify and list the proofs of a project."
  spec.description = "Thin Ruby wrapper around the b4n1-notary engine, with precompiled binaries bundled per platform. No compiler needed."
  spec.homepage = "https://github.com/B4N1-com/b4n1-notary"
  spec.license = "BUSL-1.1"
  spec.required_ruby_version = ">= 2.7"

  spec.files = Dir["lib/**/*.rb", "bin/*", "README.md", "LICENSE", "EULA.txt"]
  spec.require_paths = ["lib"]

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = spec.homepage
end
