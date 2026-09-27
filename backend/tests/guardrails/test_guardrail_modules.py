from importlib import import_module


def test_guardrail_modules_are_importable() -> None:
    modules = (
        "app.guardrails.evidence",
        "app.guardrails.input",
        "app.guardrails.loop_control",
        "app.guardrails.permissions",
        "app.guardrails.scientific_claims",
        "app.guardrails.tool_validation",
    )

    for module in modules:
        assert import_module(module) is not None
