from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_nine_model_protocol_exists():
    path = ROOT / "protocols" / "nine-model-observation-v0.1.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for model in [
        "Landscape", "Language Protocol", "Context", "Evidence",
        "Human Judgment", "AI Runtime", "FSM", "DAG / Agent Runtime",
        "Durable Execution",
    ]:
        assert model in text


def test_unknown_is_explicitly_supported():
    schema = (ROOT / "context" / "nine-model-observation.schema.yaml").read_text(
        encoding="utf-8"
    )
    assert "UNKNOWN" in schema
    assert "causal_relationship" in schema
    assert "architecture_authorship" in schema
