from importlib import import_module


def test_workflow_modules_are_importable() -> None:
    modules = (
        "app.workflow.graph",
        "app.workflow.nodes",
        "app.workflow.routing",
        "app.workflow.state",
    )

    for module in modules:
        assert import_module(module) is not None
