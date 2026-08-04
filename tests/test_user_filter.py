import importlib.util
import os
import pathlib
import sys
import types

os.environ.setdefault("SUPABASE_URL", "https://example.com")
os.environ.setdefault("SUPABASE_SECRET_KEY", "dummy-key")

sys.modules["supabase"] = types.SimpleNamespace(create_client=lambda *args, **kwargs: None)

app_path = pathlib.Path(__file__).resolve().parents[1] / "app.py"
module_code = app_path.read_text(encoding="utf-8")
module_code = module_code.replace("init_admin()\n", "")
module_code = module_code.replace("app: Flask = Flask(__name__)\n", "app: Flask = Flask(__name__)\n")

spec = importlib.util.spec_from_loader("app_module", loader=None)
module = importlib.util.module_from_spec(spec)
module.__dict__["__file__"] = str(app_path)
exec(compile(module_code, str(app_path), "exec"), module.__dict__)


def test_childonly_is_hidden_for_holiday_and_workday():
    users = {
        "childonly_user": {"role": "childonly", "child_name": "太郎"},
        "normal_user": {"role": "user", "child_name": "花子"},
    }

    filtered = module.filter_users_for_display(users, "holiday")
    assert [username for username, _ in filtered] == ["normal_user"]


def test_childday_skips_users_without_child_name():
    users = {
        "no_child": {"role": "user"},
        "with_child": {"role": "user", "child_name": "花子"},
    }

    filtered = module.filter_users_for_display(users, "childday")
    assert [username for username, _ in filtered] == ["with_child"]
