from importlib import import_module


def test_tool_modules_are_importable() -> None:
    modules = (
        "app.tools.analysis",
        "app.tools.astronomy",
        "app.tools.data",
        "app.tools.literature",
        "app.tools.verification",
    )

    for module in modules:
        assert import_module(module) is not None
