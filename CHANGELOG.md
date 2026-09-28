# Changelog

## 0.1.0a1

Initial alpha with a small, offline template-based data synthesis workflow:

- Expand seed rows over configurable variable combinations.
- Render output fields using `${variable}` templates.
- Validate recipes and required fields; reject oversized candidate sets.
- Remove exact duplicate records while preserving order.
- Export UTF-8 JSONL without overwriting existing files or leaving partial output.
- Provide a Python API, CLI, runnable FAQ example, and tests.

This release does not call language models or implement agent environments.
Model-based synthesis methods, quality scoring, and agent trajectories remain on the roadmap.
