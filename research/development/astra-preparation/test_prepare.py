"""Offline boundary and scoring checks with public toy material only."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from prepare import ROOT, prepare, private_path, score


def fixture():
    items = []
    for i in range(12):
        items.append({"id": f"P{i + 1:02}", "repository": "netbox" if i < 6 else "httpx",
                      "kind": "source" if i % 2 == 0 else "control", "pair": str(i // 2),
                      "excerpt": f"def example_{i}():\n    # [MASK]\n    return None",
                      "answer": f"Seven hidden words kept only inside scoring key {i}",
                      "source": {"private_metadata": "MUST_NOT_ENTER_REQUEST"}})
    return {"version": 1, "seed": 73, "items": items}


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.settings = json.loads(Path(__file__).with_name("settings.json").read_text())
        self.spec = fixture()

    def test_allowlisted_requests_and_fixed_order(self):
        packets, key = prepare(self.spec, self.settings)
        self.assertEqual(len(packets), 24)
        self.assertEqual((packets, key), prepare(self.spec, self.settings))
        for p in packets:
            text = json.dumps(p["body"])
            self.assertNotIn("MUST_NOT_ENTER_REQUEST", text)
            self.assertNotIn("Seven hidden words", text)
            self.assertEqual(p["body"]["tools"], [])
            self.assertFalse(p["body"]["store"])
            self.assertNotIn("previous_response_id", p["body"])

    def test_rejects_visible_answer_and_extra_fields(self):
        for mutate in (lambda x: x["items"][0].update(excerpt="[MASK] " + x["items"][0]["answer"]),
                       lambda x: x["items"][0].update(extra="unexpected"),
                       lambda x: x["items"][0].update(excerpt="no mask"),
                       lambda x: x["items"][0].update(id="P02"),
                       lambda x: x["items"][0].update(pair="different")):
            spec = deepcopy(self.spec)
            mutate(spec)
            with self.assertRaises(ValueError):
                prepare(spec, self.settings)

    def test_rejects_oversize_and_unbalanced(self):
        spec = deepcopy(self.spec)
        spec["items"][0]["excerpt"] = "[MASK]" + "a" * 9000
        with self.assertRaises(ValueError):
            prepare(spec, self.settings)
        spec = deepcopy(self.spec)
        spec["items"][0]["kind"] = "control"
        with self.assertRaises(ValueError):
            prepare(spec, self.settings)

    def test_forbids_private_pack_in_public_checkout(self):
        with self.assertRaises(ValueError):
            private_path(ROOT / "local-runs" / "sealed")

    def test_scoring_preserves_missing_and_invalid(self):
        packets, key = prepare(self.spec, self.settings)
        responses = {"P01_R1": {"completion": "  " + key[0]["answer"] + "\n"},
                     "P01_R2": {"completion": key[0]["answer"].upper()},
                     "P02_R1": {"completion": key[1]["answer"], "unexpected": True}}
        rows = {r["id"]: r for r in score(packets, key, responses)["rows"]}
        self.assertTrue(rows["P01_R1"]["exact_match"])
        self.assertFalse(rows["P01_R2"]["exact_match"])
        self.assertEqual(rows["P02_R1"]["status"], "invalid")
        self.assertEqual(rows["P02_R2"]["status"], "missing")
        with self.assertRaises(ValueError):
            score(packets, key, {"unknown": {}})

    def test_budget_arithmetic(self):
        s = self.settings
        rates = s["reservation_rates_usd_per_million"]
        for stage in ("screening", "qualification"):
            cfg = s[stage]
            per_call = (cfg["max_input_tokens"] * rates["input"] + cfg["max_output_tokens"] * rates["output"]) / 1e6
            count = cfg.get("max_calls", cfg.get("max_calls_including_connection_check"))
            self.assertLessEqual(per_call * count, cfg["proposed_ceiling_usd"])
        self.assertEqual(4 * 6 * 3 * 2, s["qualification"]["max_calls"])
        self.assertEqual(sum(s[k]["proposed_ceiling_usd"] for k in ("screening", "qualification", "development"))
                         + s["unallocated_reserve_usd"], s["proposed_preparation_total_usd"])


if __name__ == "__main__":
    unittest.main()
