# ruff: noqa: E402
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from lia.config import Config


def test_env_override(tmp_path, monkeypatch):
    cfg_file = tmp_path / "c.yaml"
    cfg_file.write_text("pv_access_key: 'filekey'\n")
    monkeypatch.setenv("PV_ACCESS_KEY", "envkey")
    cfg = Config(str(cfg_file))
    assert cfg.PV_ACCESS_KEY == "envkey"
