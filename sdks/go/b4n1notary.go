// Package b4n1notary is the Go SDK for b4n1-notary: authorship integrity and
// sealing. It is a thin client of the b4n1-notary binary (bundled under bin/),
// so one fix in the engine reaches every language.
//
// Override the binary with B4N1NOTARY_BIN_PATH.
package b4n1notary

import (
	"bytes"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
)

// SDKVersion is the version of this wrapper.
const SDKVersion = "0.2.1"

// Result is the outcome of one notary command.
type Result struct {
	ExitCode int
	Stdout   string
	Stderr   string
}

// OK reports whether the command exited zero.
func (r Result) OK() bool { return r.ExitCode == 0 }

// BinaryPath resolves the engine: explicit override, bundled binary, PATH.
func BinaryPath() string {
	if p := os.Getenv("B4N1NOTARY_BIN_PATH"); p != "" {
		return p
	}
	name := "b4n1notary-linux-amd64"
	switch runtime.GOOS {
	case "darwin":
		if runtime.GOARCH == "arm64" {
			name = "b4n1notary-macos-arm64"
		} else {
			name = "b4n1notary-macos-x64"
		}
	case "windows":
		name = "b4n1notary-windows-amd64.exe"
	case "linux":
		if runtime.GOARCH == "arm64" {
			name = "b4n1notary-linux-arm64"
		} else if runtime.GOARCH == "386" {
			name = "b4n1notary-linux-ia32"
		}
	}
	bundled := filepath.Join("bin", name)
	if _, err := os.Stat(bundled); err == nil {
		return bundled
	}
	if p, err := exec.LookPath("b4n1-notary"); err == nil {
		return p
	}
	return "b4n1-notary"
}

func run(args ...string) Result {
	cmd := exec.Command(BinaryPath(), args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	if exitErr, ok := err.(*exec.ExitError); ok {
		return Result{ExitCode: exitErr.ExitCode(), Stdout: stdout.String(), Stderr: stderr.String()}
	} else if err != nil {
		return Result{ExitCode: -1, Stdout: stdout.String(), Stderr: err.Error()}
	}
	return Result{ExitCode: 0, Stdout: stdout.String(), Stderr: stderr.String()}
}

// Client is bound to one resolved engine binary.
type Client struct{ Binary string }

// NewClient resolves the engine once.
func NewClient() *Client { return &Client{Binary: BinaryPath()} }

// Stamp seals a project: Merkle root plus a .b4n1-proof file.
func (c *Client) Stamp(path, identity string) Result {
	args := []string{"stamp", "--path", path}
	if identity != "" {
		args = append(args, "--identity", identity)
	}
	return run(args...)
}

// Verify checks a project against a proof file.
func (c *Client) Verify(path, proof string) Result {
	return run("verify", "--path", path, "--proof", proof)
}

// VerifyOts checks the OpenTimestamps receipt of a proof.
func (c *Client) VerifyOts(path, proof string, checkCalendar bool, header string) Result {
	args := []string{"verify-ots", "--path", path, "--proof", proof}
	if checkCalendar {
		args = append(args, "--check-calendar")
	}
	if header != "" {
		args = append(args, "--header", header)
	}
	return run(args...)
}

// History lists the proofs sealed for a project.
func (c *Client) History(path string) Result {
	return run("history", "--path", path)
}

// License exposes the licence surface (status, check, machine, install).
func (c *Client) License(action, key string, jsonOut bool) Result {
	args := []string{"license"}
	if action != "" {
		args = append(args, action)
	}
	if key != "" {
		args = append(args, key)
	}
	if jsonOut {
		args = append(args, "--json")
	}
	return run(args...)
}
