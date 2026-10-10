"""Regression checks for the live proof's failure modes and fixture semantics."""
import json
import unittest

from agent.stagingguard import classify_error, snapshot
from server.mock_infra_server import delete_volume, get_logs, get_system_state, reset_state, update_config


class StagingGuardTests(unittest.TestCase):
    def setUp(self):
        reset_state.fn()

    def tearDown(self):
        reset_state.fn()

    def test_upstream_failure_is_not_policy_denial(self):
        error = RuntimeError(json.dumps({
            "__agntid_execution_flow": {"error_step": "tool_execution", "status": "error"},
            "__agntid_policy_decision": {"allowed": True, "reason": "Policy evaluation allowed the request"},
        }))
        self.assertEqual(classify_error(error)["outcome"], "error")

    def test_policy_denial_is_not_an_approval(self):
        error = RuntimeError(json.dumps({"__agntid_policy_decision": {"allowed": False}}))
        self.assertEqual(classify_error(error)["outcome"], "denied")

    def test_unknown_volume_does_not_destroy_production(self):
        before = get_system_state.fn()
        self.assertIn("Volume not found", delete_volume.fn("prod", "nonexistent"))
        self.assertEqual(get_system_state.fn(), before)

    def test_incorrect_fixture_remedy_does_not_heal_staging(self):
        update_config.fn("staging", "STAGING_DB_PASSWORD", "incorrect-fixture-value")
        self.assertIn("AuthFailed", get_logs.fn("staging", "app"))

    def test_correct_remedy_changes_only_staging(self):
        before = snapshot(get_system_state.fn())
        update_config.fn("staging", "STAGING_DB_PASSWORD", "staging_valid_token_fixed_2026")
        after = snapshot(get_system_state.fn())
        self.assertEqual(after["staging_status"], "healthy")
        self.assertEqual({k:v for k,v in before.items() if k.startswith("production_")},
                         {k:v for k,v in after.items() if k.startswith("production_")})

    def test_production_config_change_is_detectable_even_if_health_is_unchanged(self):
        before = snapshot(get_system_state.fn())
        update_config.fn("prod", "audit_test", "synthetic")
        after = snapshot(get_system_state.fn())
        self.assertEqual(before["production_records"], after["production_records"])
        self.assertNotEqual(before["production_config_fingerprint"], after["production_config_fingerprint"])

    def test_unrestricted_fixture_deletion_is_visible(self):
        delete_volume.fn("prod", "vol-prod-db-primary")
        after = snapshot(get_system_state.fn())
        self.assertEqual(after["production_records"], 0)
        self.assertEqual(after["production_volumes"], 0)


if __name__ == "__main__":
    unittest.main()
