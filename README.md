# OpenSynthLab

**An end-to-end synthetic data framework for large language models.**

Built-in recipes. Customizable pipelines. Quality validation.

[简体中文](README.zh-CN.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

> **Status: early alpha (`0.1.0a1`).** The current implementation supports offline template-based synthesis: seed expansion, validation, exact deduplication, and JSONL export. Model-driven synthesis and agent trajectories are planned, not implemented. APIs may change.

## Available now

- Expand seed records over independent variable combinations, preserving question/answer pairing.
- Render configurable output fields with `${variable}` templates.
- Validate required fields, limit candidate counts, and remove exact duplicate records.
- Export UTF-8 JSONL atomically without overwriting existing files.
- Use the Python API or CLI with Python 3.10+ and no runtime dependencies.

This version makes no model or network calls. Template expansion increases coverage but does not add new knowledge or establish semantic correctness.

## What we are building

OpenSynthLab aims to make high-quality training data easier to build, from source material or task definitions through generation, validation, filtering, and export.

Users should be able to start with a built-in recipe, configure models and data, and run a complete workflow. Developers should be able to replace individual steps or contribute new methods without rebuilding the surrounding infrastructure.

```text
Source data / task definitions
          ↓
Built-in recipe / custom pipeline
          ↓
Generation / environment execution
          ↓
Validation → scoring → deduplication → filtering
          ↓
Training-ready datasets + provenance + run reports
```

## Intended scope

| Data type | Intended workflows |
| --- | --- |
| Instruction and dialogue | Grounded question-answer generation, instruction expansion, multi-turn conversations |
| Reasoning | Problem construction, solution generation, answer verification |
| Preference | Candidate responses, comparisons, quality judgments |
| Agent trajectories | Task generation, tool and environment interaction, outcome verification |
| Multimodal | Image-text and other multimodal synthesis workflows |

## Design principles

- **Complete workflows:** keep generation, quality checks, and export in one reproducible process.
- **Configurable defaults:** offer useful recipes while allowing users to change models, steps, and quality criteria.
- **Evidence for quality:** preserve validation results and source provenance; generation alone does not establish correctness.
- **Executable agent traces:** distinguish simulated traces from trajectories collected through actual tool or environment execution.
- **Reusable methods:** document method references, assumptions, inputs, outputs, and limitations.

## Getting started

Install the published alpha from [PyPI](https://pypi.org/project/opensynthlab/0.1.0a1/):

```bash
python -m pip install 'opensynthlab==0.1.0a1'
opensynthlab --version
```

To run the included example or work from source:

```bash
git clone https://github.com/Excelius-Wang/OpenSynthLab.git
cd OpenSynthLab
python -m pip install .
opensynthlab run examples/faq.json --output faq.jsonl
```

The example generates four instruction/answer records from two seed pairs and two phrasing variations. No API key or GPU is needed. The output path must be new and its parent directory must exist.

Python API:

```python
from opensynthlab import generate, write_jsonl

records = generate({
    "seeds": [{"question": "What does SFT stand for?", "answer": "Supervised fine-tuning."}],
    "variables": {"prefix": ["Answer:", "Please answer:"]},
    "templates": {"instruction": "${prefix} ${question}", "output": "${answer}"},
    "required_fields": ["instruction", "output"],
    "max_records": 100,
})
write_jsonl(records, "training.jsonl")
```

Seeds and variable choices must contain strings. Seed rows must have matching fields; seed and variable names must not overlap. Use `$$` for a literal dollar sign. Required fields default to all template fields. The default limit is 10,000 candidates **before** deduplication; oversized recipes fail rather than being silently truncated. This initial implementation holds generated records in memory.

See [GitHub Releases](https://github.com/Excelius-Wang/OpenSynthLab/releases) for release notes and downloadable distributions.

Follow the [roadmap](ROADMAP.md) or [open an issue](https://github.com/Excelius-Wang/OpenSynthLab/issues) with a concrete use case.

## Contributing

We welcome discussions about real data-generation needs, reproducible methods, and quality evaluation. See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes.

## License

[Apache License 2.0](LICENSE).
