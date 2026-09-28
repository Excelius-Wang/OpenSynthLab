# Roadmap

This is a proposal for implementation, not a release schedule. Milestones may change as concrete use cases are tested. See the README and changelog for available features.

## Initial alpha

- [x] Implement deterministic seed/template expansion with configurable variables.
- [x] Validate required fields and enforce a candidate-count limit.
- [x] Remove exact duplicates and export JSONL without overwriting existing files.
- [x] Provide a Python API, CLI, example recipe, and regression tests.
- [x] Publish the first alpha to PyPI (`0.1.0a1`).

## First usable workflow

- [ ] Define a minimal configuration and record format.
- [ ] Support a model backend and a local dry-run mode.
- [ ] Implement one source-grounded instruction/QA recipe.
- [ ] Add schema checks, exact deduplication, and configurable filtering.
- [ ] Export JSONL with source references and a run summary.
- [ ] Document and test the complete workflow before publishing an alpha package.

## Customization and reproducibility

- [ ] Define extension interfaces for generation, validation, scoring, and export.
- [ ] Add a recipe registry with explicit inputs, outputs, and method references.
- [ ] Support retries, checkpoints, and resuming interrupted runs.
- [ ] Record configuration, model identifiers, and processing decisions.
- [ ] Add recipe examples for instruction expansion, reasoning, and preference data.

## Agent trajectory workflows

- [ ] Define task, tool-call, observation, and outcome records.
- [ ] Integrate an isolated execution environment with reset support.
- [ ] Collect trajectories from actual agent/environment interaction.
- [ ] Add outcome verifiers and checks for incomplete or malformed trajectories.
- [ ] Preserve successful and failed runs with explicit labels.
- [ ] Provide a reproducible task-generation-to-dataset example.

## Broader workflows

- [ ] Extend the record format and recipes for multimodal data.
- [ ] Add comparative evaluations of data recipes on downstream tasks.
- [ ] Improve batch execution, cost reporting, and model-backend coverage.
- [ ] Evaluate a visual interface after the configuration and execution APIs stabilize.

## Proposing a method

Include a paper or implementation reference, intended users, required inputs, expected outputs, validation approach, and a small reproducible example. A method should be evaluated beyond whether it produces syntactically valid data.
