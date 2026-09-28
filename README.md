# OpenSynthLab

**An end-to-end synthetic data framework for large language models.**

Built-in recipes. Customizable pipelines. Quality validation.

[简体中文](README.zh-CN.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

> **Status: project initialization.** This repository currently contains the project direction and roadmap. There is no runnable framework or published Python package yet. All capabilities below describe the intended scope, not released features.

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

Implementation has not started. Follow the [roadmap](ROADMAP.md) for the proposed milestones or [open an issue](https://github.com/Excelius-Wang/OpenSynthLab/issues) with a concrete use case.

The intended Python package name is `opensynthlab`. It has **not** been published or reserved on PyPI.

## Contributing

We welcome discussions about real data-generation needs, reproducible methods, and quality evaluation. See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes.

## License

[Apache License 2.0](LICENSE).
