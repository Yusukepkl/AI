import os
import tempfile
import types
import sys

# Stub opentelemetry dependency used in logger
opentelemetry = types.ModuleType("opentelemetry")
opentelemetry.trace = types.SimpleNamespace(get_tracer=lambda name: None)
sys.modules.setdefault("opentelemetry", opentelemetry)
sys.modules.setdefault("opentelemetry.trace", opentelemetry.trace)

# Ensure project root is on path so we can import plugins.loader
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from plugins.loader import load_plugins


def test_load_plugins_filters_invalid_modules():
    with tempfile.TemporaryDirectory() as plugin_dir:
        valid_path = os.path.join(plugin_dir, "valid.py")
        with open(valid_path, "w", encoding="utf-8") as f:
            f.write(
                """name = 'valid'\n
def handle(text: str):\n    return 'ok'\n"""
            )

        invalid_path = os.path.join(plugin_dir, "invalid.py")
        with open(invalid_path, "w", encoding="utf-8") as f:
            f.write("x = 1\n")

        plugins = load_plugins(plugin_dir)

        assert len(plugins) == 1
        assert plugins[0].name == 'valid'
