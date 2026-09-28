import json
import tempfile
import unittest
from pathlib import Path

from opensynthlab import generate, write_jsonl
from opensynthlab.cli import main


class GenerationTests(unittest.TestCase):
    def test_expansion_preserves_seed_pairing_and_order(self):
        recipe = {
            "seeds": [{"q": "Q1", "a": "A1"}, {"q": "Q2", "a": "A2"}],
            "variables": {"prefix": ["short", "long"]},
            "templates": {"instruction": "${prefix}: ${q}", "output": "${a}"},
        }
        self.assertEqual(generate(recipe), [
            {"instruction": "short: Q1", "output": "A1"},
            {"instruction": "long: Q1", "output": "A1"},
            {"instruction": "short: Q2", "output": "A2"},
            {"instruction": "long: Q2", "output": "A2"},
        ])

    def test_duplicates_removed_without_reordering(self):
        self.assertEqual(generate({
            "variables": {"x": ["B", "A", "B"]}, "templates": {"text": "${x}"},
        }), [{"text": "B"}, {"text": "A"}])

    def test_bound_applies_before_generation_and_deduplication(self):
        with self.assertRaisesRegex(ValueError, "4 candidates"):
            generate({"variables": {"x": ["x", "x"], "y": ["y", "y"]},
                      "templates": {"text": "${x}${y}"}, "max_records": 3})

    def test_literal_dollars_json_braces_and_unicode(self):
        self.assertEqual(generate({"templates": {"text": '价格 $$5，JSON: {"a": 1}'}}),
                         [{"text": '价格 $5，JSON: {"a": 1}'}])

    def test_invalid_recipes_rejected(self):
        cases = [
            {"templates": {}},
            {"templates": {"text": "${missing}"}},
            {"templates": {"text": "$!"}},
            {"templates": {"text": " "}},
            {"templates": {"text": "ok"}, "required_fields": ["missing"]},
            {"templates": {"text": "ok"}, "max_records": True},
            {"templates": {"text": "ok"}, "max_records": 0},
            {"templates": {"text": "ok"}, "variables": {"x": []}},
            {"templates": {"text": "ok"}, "variables": {"x": [1]}},
            {"templates": {"text": "ok"}, "variables": {"bad-key": ["x"]}},
            {"templates": {"text": "ok"}, "seeds": []},
            {"templates": {"text": "ok"}, "seeds": [{"x": "a"}, {"y": "b"}]},
            {"templates": {"text": "ok"}, "seeds": [{"x": "a"}], "variables": {"x": ["b"]}},
            {"templates": {"text": "ok"}, "typo": "ignored?"},
        ]
        for recipe in cases:
            with self.subTest(recipe=recipe), self.assertRaises(ValueError):
                generate(recipe)

    def test_optional_fields_may_be_blank(self):
        self.assertEqual(generate({"templates": {"instruction": "Q", "input": ""},
                                   "required_fields": ["instruction"]}),
                         [{"instruction": "Q", "input": ""}])


class ExportTests(unittest.TestCase):
    def test_jsonl_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.jsonl"
            records = [{"text": "中文\n第二行"}, {"text": "second"}]
            self.assertEqual(write_jsonl(records, path), 2)
            self.assertEqual([json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()], records)

    def test_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "existing.jsonl"
            path.write_text("keep me", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                write_jsonl([{"text": "new"}], path)
            self.assertEqual(path.read_text(), "keep me")
            self.assertEqual(len(list(Path(folder).iterdir())), 1)

    def test_failed_serialization_leaves_no_partial_file(self):
        for invalid in [object(), float("nan")]:
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as folder:
                with self.assertRaises((TypeError, ValueError)):
                    write_jsonl([{"ok": 1}, {"bad": invalid}], Path(folder) / "output.jsonl")
                self.assertEqual(list(Path(folder).iterdir()), [])

    def test_cli_example_end_to_end(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output.jsonl"
            recipe = Path(__file__).resolve().parents[1] / "examples" / "faq.json"
            self.assertEqual(main(["run", str(recipe), "--output", str(output)]), 0)
            rows = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[0]["output"], "Retrieval-augmented generation.")


if __name__ == "__main__":
    unittest.main()
