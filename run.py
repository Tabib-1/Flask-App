from app import create_app
import importlib.util
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "app"


def load_create_app():
    for candidate in ("__init__.py", "init.py"):
        module_path = APP_DIR / candidate
        if not module_path.exists():
            continue

        spec = importlib.util.spec_from_file_location(
            "app",
            module_path,
            submodule_search_locations=[str(APP_DIR)],
        )
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules["app"] = module
        spec.loader.exec_module(module)

        if hasattr(module, "create_app"):
            return module.create_app

    raise ModuleNotFoundError(
        f"Could not load the Flask app package from {APP_DIR}. "
        "Make sure the app directory is included in your Render deploy."
    )


create_app = load_create_app()
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
