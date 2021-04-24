import os
from pathlib import Path

LOCAL_STEM = "local_settings"


def set_settings_module():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"core.{LOCAL_STEM}"
        if Path(f"core/{LOCAL_STEM}.py").exists()
        else "core.settings",
    )
