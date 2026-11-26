"""Offline suite for the b4n1-notary Python SDK.

Runs against the real binary (bundled, or the one B4N1NOTARY_BIN_PATH points
at). No network: `stamp` seals locally and reports the OTS step separately.
"""

import glob
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from b4n1notary import NotaryClient, get_b4n1notary_binary  # noqa: E402


class NotarySdkTest(unittest.TestCase):
    def setUp(self):
        self.binary = get_b4n1notary_binary()
        if not self.binary:
            self.skipTest("b4n1-notary binary not available")
        self.client = NotaryClient(self.binary)
        self.tmp = tempfile.mkdtemp(prefix="notary-sdk-")
        with open(os.path.join(self.tmp, "file.txt"), "w", encoding="utf-8") as fh:
            fh.write("hello from the sdk suite\n")

    def test_stamp_seals_project(self):
        result = self.client.stamp(self.tmp, identity="sdk-test")
        self.assertTrue(result.ok, result.stderr)
        proofs = glob.glob(os.path.join(self.tmp, ".b4n1", "proofs", "*.b4n1-proof"))
        self.assertEqual(len(proofs), 1, "stamp must write exactly one proof")

    def test_verify_accepts_fresh_proof(self):
        self.assertTrue(self.client.stamp(self.tmp).ok)
        proof = glob.glob(os.path.join(self.tmp, ".b4n1", "proofs", "*.b4n1-proof"))[0]
        result = self.client.verify(self.tmp, proof)
        self.assertTrue(result.ok, result.stderr)

    def test_verify_detects_modified_content(self):
        self.assertTrue(self.client.stamp(self.tmp).ok)
        proof = glob.glob(os.path.join(self.tmp, ".b4n1", "proofs", "*.b4n1-proof"))[0]
        with open(os.path.join(self.tmp, "file.txt"), "w", encoding="utf-8") as fh:
            fh.write("tampered\n")
        result = self.client.verify(self.tmp, proof)
        self.assertFalse(result.ok, "a modified project must not verify")

    def test_history_lists_the_proof(self):
        self.assertTrue(self.client.stamp(self.tmp).ok)
        result = self.client.history(self.tmp)
        self.assertTrue(result.ok, result.stderr)
        self.assertIn("b4n1-proof", result.stdout)

    def test_license_status_is_readable(self):
        result = self.client.license("status", json=True)
        self.assertTrue(result.ok, result.stderr)
        self.assertIn("community", result.stdout)


if __name__ == "__main__":
    unittest.main()
