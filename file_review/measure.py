"""Bounded reads of regular files, without following filesystem links."""

import codecs
import hashlib
import os
from pathlib import PurePosixPath
import stat
import time


class ScanLimit(Exception):
    """The scan's time limit has been reached."""


def open_regular(root, relative):
    parts = PurePosixPath(relative).parts
    if not parts or PurePosixPath(relative).is_absolute() or ".." in parts:
        raise ValueError("unsafe file path")
    parent = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            os.close(parent)
            parent = child
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    finally:
        os.close(parent)
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ValueError("not a regular file")
    return os.fdopen(descriptor, "rb")


def measure(root, relative, max_bytes, deadline):
    with open_regular(root, relative) as source:
        before = os.fstat(source.fileno())
        if before.st_size > max_bytes:
            return None, "over read limit"
        decoder = codecs.getincrementaldecoder("utf-8")("strict")
        digest = hashlib.sha256()
        total = lines = longest = current = 0
        previous_cr = False
        last = None
        try:
            while True:
                if time.monotonic() >= deadline:
                    raise ScanLimit()
                chunk = source.read(min(65536, max_bytes + 1 - total))
                if not chunk:
                    break
                total += len(chunk)
                digest.update(chunk)
                if total > max_bytes:
                    return None, "over read limit"
                if b"\0" in chunk:
                    return None, "binary or non-UTF-8"
                decoder.decode(chunk)
                # CRLF is one line ending, even when split between read chunks.
                for byte in chunk:
                    if byte in (10, 13):
                        if byte != 10 or not previous_cr:
                            lines += 1
                        longest = max(longest, current)
                        current = 0
                    else:
                        current += 1
                    previous_cr = byte == 13
                    last = byte
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            return None, "binary or non-UTF-8"
        after = os.fstat(source.fileno())
        identity = lambda item: (item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns, item.st_ctime_ns)
        # Reopen the path as well: an editor may have replaced the original inode.
        with open_regular(root, relative) as current_source:
            current_stat = os.fstat(current_source.fileno())
        if identity(before) != identity(after) or identity(before) != identity(current_stat):
            return None, "changed during scan"
        if last is not None and last not in (10, 13):
            lines += 1
        return {"path": relative, "lines": lines, "bytes": total, "sha256": digest.hexdigest(),
                "longest_line": max(longest, current)}, None
