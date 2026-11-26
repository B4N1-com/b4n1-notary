package b4n1notary

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func project(t *testing.T) string {
	t.Helper()
	dir := t.TempDir()
	if err := os.WriteFile(filepath.Join(dir, "file.txt"), []byte("hello from the go sdk suite\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	return dir
}

func proofOf(t *testing.T, dir string) string {
	t.Helper()
	matches, err := filepath.Glob(filepath.Join(dir, ".b4n1", "proofs", "*.b4n1-proof"))
	if err != nil || len(matches) == 0 {
		t.Fatalf("no proof written (err=%v)", err)
	}
	return matches[0]
}

func TestStampSealsProject(t *testing.T) {
	dir := project(t)
	res := NewClient().Stamp(dir, "sdk-test")
	if !res.OK() {
		t.Fatalf("stamp failed: %s", res.Stderr)
	}
	proofOf(t, dir)
}

func TestVerifyAcceptsFreshProof(t *testing.T) {
	dir := project(t)
	c := NewClient()
	if res := c.Stamp(dir, ""); !res.OK() {
		t.Fatalf("stamp failed: %s", res.Stderr)
	}
	if res := c.Verify(dir, proofOf(t, dir)); !res.OK() {
		t.Fatalf("verify failed: %s", res.Stderr)
	}
}

func TestVerifyDetectsModifiedContent(t *testing.T) {
	dir := project(t)
	c := NewClient()
	if res := c.Stamp(dir, ""); !res.OK() {
		t.Fatalf("stamp failed: %s", res.Stderr)
	}
	proof := proofOf(t, dir)
	if err := os.WriteFile(filepath.Join(dir, "file.txt"), []byte("tampered\n"), 0o644); err != nil {
		t.Fatal(err)
	}

	if res := c.Verify(dir, proof); res.OK() {
		t.Fatal("a modified project verified")
	}
}

func TestHistoryListsTheProof(t *testing.T) {
	dir := project(t)
	c := NewClient()
	if res := c.Stamp(dir, ""); !res.OK() {
		t.Fatalf("stamp failed: %s", res.Stderr)
	}
	res := c.History(dir)
	if !res.OK() || !strings.Contains(res.Stdout, "b4n1-proof") {
		t.Fatalf("history did not list the proof: %s", res.Stderr)
	}
}

func TestLicenseStatusIsReadable(t *testing.T) {
	res := NewClient().License("status", "", true)
	if !res.OK() || !strings.Contains(res.Stdout, "community") {
		t.Fatalf("licence status unexpected: %s", res.Stderr)
	}
}
