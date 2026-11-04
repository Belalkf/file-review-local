import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from file_review.measure import ScanLimit, measure, open_regular


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def count(self, content, cap=100000):
        (self.root / "file").write_bytes(content)
        return measure(self.root, "file", cap, time.monotonic() + 5)

    def test_empty_final_line_and_line_endings(self):
        for content, lines, longest in [(b"", 0, 0), (b"a", 1, 1), (b"a\n", 1, 1),
                                         (b"a\r\nb\rc\n\n", 4, 1), (b"\r\n", 1, 0)]:
            with self.subTest(content=content):
                row, reason = self.count(content)
                self.assertIsNone(reason)
                self.assertEqual((row["lines"], row["longest_line"], row["bytes"]), (lines, longest, len(content)))

    def test_multibyte_and_crlf_chunk_boundaries(self):
        content = b"x" * 65534 + b"\r\n" + "é".encode() + b"\n"
        row, reason = self.count(content)
        self.assertIsNone(reason)
        self.assertEqual((row["lines"], row["longest_line"]), (2, 65534))
        row, reason = self.count(b"x" * 65535 + b"\r\n" + b"y")
        self.assertEqual(row["lines"], 2)
        row, reason = self.count(b"x" * 65535 + "é".encode())
        self.assertEqual(row["longest_line"], 65537)

    def test_non_text_and_read_limit_not_treated_as_small_files(self):
        for content in [b"x\0", b"\xff", b"\xc3"]:
            self.assertEqual(self.count(content), (None, "binary or non-UTF-8"))
        self.assertEqual(self.count(b"123", cap=2), (None, "over read limit"))
        self.assertEqual(self.count(b"12", cap=2)[0]["bytes"], 2)

    def test_links_and_parent_escape_are_rejected(self):
        (self.root / "real").mkdir()
        (self.root / "real" / "file").write_text("private")
        (self.root / "link").symlink_to(self.root / "real", target_is_directory=True)
        (self.root / "file").symlink_to(self.root / "real" / "file")
        for path in ["link/file", "file", "../outside", "/etc/passwd", "real"]:
            with self.subTest(path=path), self.assertRaises((OSError, ValueError)):
                open_regular(self.root, path)

    def test_fifo_does_not_wait_for_writer(self):
        os.mkfifo(self.root / "pipe")
        with self.assertRaises(ValueError):
            open_regular(self.root, "pipe")

    def test_replaced_path_during_measurement_is_rejected(self):
        (self.root / "file").write_text("original")
        calls = 0
        real_open = open_regular
        def replacing_open(root, relative):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.root / "replacement").write_text("new")
                os.replace(self.root / "replacement", self.root / "file")
            return real_open(root, relative)
        with patch("file_review.measure.open_regular", side_effect=replacing_open):
            self.assertEqual(measure(self.root, "file", 100, time.monotonic() + 5), (None, "changed during scan"))

    def test_deadline(self):
        (self.root / "file").write_text("x")
        with self.assertRaises(ScanLimit):
            measure(self.root, "file", 100, time.monotonic() - 1)
