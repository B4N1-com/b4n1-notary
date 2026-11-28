<p align="center">
  <img src="https://raw.githubusercontent.com/B4N1-com/b4n1-notary/master/b4n1notary_presentation.png" alt="B4N1 Notary — Prove what you delivered, and when." width="100%">
</p>

<div align="center">

# b4n1-notary

**Prove what you delivered, and when.**

[![License](https://img.shields.io/badge/license-BUSL--1.1-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/b4n1-notary.svg)](https://pypi.org/project/b4n1-notary/)
[![PyPI downloads](https://img.shields.io/pypi/dm/b4n1-notary.svg)](https://pypi.org/project/b4n1-notary/)
[![Pepy downloads](https://img.shields.io/pepy/dt/b4n1-notary.svg)](https://pepy.tech/project/b4n1-notary)
[![npm](https://img.shields.io/npm/v/b4n1-notary.svg)](https://www.npmjs.com/package/b4n1-notary)
[![npm downloads](https://img.shields.io/npm/dm/b4n1-notary.svg)](https://www.npmjs.com/package/b4n1-notary)
[![NuGet](https://img.shields.io/nuget/v/B4n1.Notary.svg)](https://www.nuget.org/packages/B4n1.Notary)
[![NuGet downloads](https://img.shields.io/nuget/dt/B4n1.Notary.svg)](https://www.nuget.org/packages/B4n1.Notary)
[![RubyGems](https://img.shields.io/gem/v/b4n1-notary.svg)](https://rubygems.org/gems/b4n1-notary)
[![Packagist](https://img.shields.io/packagist/v/b4n1/b4n1-notary.svg)](https://packagist.org/packages/b4n1/b4n1-notary)
[![Go Reference](https://pkg.go.dev/badge/github.com/b4n1-com/b4n1-notary/sdks/go.svg)](https://pkg.go.dev/github.com/b4n1-com/b4n1-notary/sdks/go)

**SDK languages:** Python · JavaScript · Java · C# · Ruby · PHP · Go · [b4n1lang](https://b4n1.com/en/products/lang/) — thin wrappers over one native core, plus b4n1lang, our own compiled language for calling B4N1 capabilities directly.

[Manual](docs/src/SUMMARY.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [Deutsch](i18n/README.de.md) · [Italiano](i18n/README.it.md) · [Português](i18n/README.pt-BR.md) · [Русский](i18n/README.ru.md) · [العربية](i18n/README.ar.md) · [हिन्दी](i18n/README.hi.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [中文](i18n/README.zh-CN.md)

</div>

---

b4n1-notary seals a project into **one Merkle root** and writes a portable
proof file. Verify it later — or hand it to a client — and the answer is a
single line: `✅ VERIFIED`, or the first file that no longer matches.

## Why it matters

Version control records what changed. It does not record **what exactly you
delivered on a given day**: a tag can move and an archive can be re-zipped.
A Merkle root over every file, with a timestamp, is evidence that does not
depend on trusting the person who produced it.

## Install

| Language | Command |
|---|---|
| Python | `pip install b4n1-notary` |
| JavaScript | `npm install b4n1-notary` |
| Java | `com.b4n1:b4n1-notary:0.2.1` |
| .NET | `dotnet add package B4n1.Notary` |
| Ruby | `gem install b4n1-notary` |
| PHP | `composer require b4n1/b4n1-notary` |
| Go | `go get github.com/B4N1-com/b4n1-notary/sdks/go` |

Every package carries precompiled binaries for Linux, macOS and Windows — no
compiler is needed, and there is nothing else to install.

## What you can do

- **Seal** a tree: `stamp` prints the file count, the Merkle root and the
  proof path.
- **Verify** later: `verify` recomputes the root and names any mismatch.
- **Anchor** in Bitcoin: `verify-ots --check-calendar` inspects the
  OpenTimestamps receipt, with typed exit codes.
- **Audit history**: `history` lists every proof already sealed.

## Example

```text
$ b4n1-notary stamp --path ./release --identity "team"
🦀 Sealed 214 file(s) · Merkle root: 9f2c…c41a
✅ Authorship sealed in: ./release/.b4n1/proofs/1730….b4n1-proof

$ b4n1-notary verify --path ./release --proof ./release/.b4n1/proofs/1730….b4n1-proof
✅ VERIFIED: Content matches authorship seal.
```

## Documentation

The complete manual lives in [`docs/`](docs/src/SUMMARY.md): quick start, the
proof format, OpenTimestamps anchoring, the command reference and the seven
SDKs. It works offline, next to the packages.

## Licensing

The SDK wrappers are Business Source License 1.1 — see [`LICENSE`](LICENSE).
Every binary is distributed with its own [`EULA.txt`](EULA.txt). Third-party
notices: [`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt).
