"""DIAGNOSTIC ONLY (never merged): count search_files errors for the #104696 bounded files-lane repro."""
import json
import time

import pytest

pytestmark = pytest.mark.platforms("macos")


def test_eperm_probe(tmp_path):
    from tools.file_tools import search_tool
    from tools.terminal_tool_lifecycle import cleanup_vm
    d = tmp_path / "tree"
    d.mkdir()
    for i in range(500):
        (d / f"f_{i:03d}.py").write_text("x\n")
    done, errs, i = 0, {}, 0
    deadline = time.monotonic() + 40
    try:
        while time.monotonic() < deadline:
            i += 1
            r = json.loads(search_tool("*", target="files", path=str(d), limit=2 + (i % 50), task_id="t-eperm"))
            done += 1
            if r.get("error") or not r.get("files"):
                k = str(r.get("error"))[:80]
                errs[k] = errs.get(k, 0) + 1
    finally:
        cleanup_vm("t-eperm")
    pytest.fail(f"EPERMCOUNTS done={done} errs={errs}")
