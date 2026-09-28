# Contributing to OpenSynthLab

OpenSynthLab is an early alpha. The current implementation is a small offline template synthesis pipeline; model-driven recipes and agent environments remain on the roadmap.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e . build twine
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell. See [the publishing guide](docs/PUBLISHING.md) for the release process.

## Start with a concrete use case

For substantial changes, open an issue to discuss scope before implementation. Describe:

- The data you want to generate and its downstream use.
- The proposed method and its reference, if applicable.
- Required models, tools, environments, and compute.
- How you would verify correctness and assess usefulness.

Please check existing issues and pull requests to avoid duplicate work.

## Contributions we welcome

- Requirements grounded in real data-synthesis workflows.
- Reproducible method implementations with clear provenance.
- Validators, quality checks, and evaluation recipes.
- Agent environments and outcome verifiers.
- Documentation, examples, and focused bug fixes as the codebase grows.

## Pull requests

Keep changes focused. Explain the problem, resulting behavior, validation performed, and relevant limitations. Link the associated issue when one exists.

Add meaningful tests for new behavior, especially parsing, validation, checkpointing, and environment interactions. Examples should use small inputs and document any external API calls or costs.

Never commit credentials, private datasets, or confidential user traces. Use synthetic fixtures for examples. Clearly distinguish simulated tool responses from actual execution results.

New methods must include appropriate attribution and compatible licensing. Contributions to this repository are provided under its Apache-2.0 license.
