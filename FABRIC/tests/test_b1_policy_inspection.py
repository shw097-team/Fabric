"""Maker tests of the consumer read-only ceiling, not Native Loaded acceptance."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'fabric/consumers/hgk_policy_consumer.py'
spec = importlib.util.spec_from_file_location('b1_policy_consumer', MODULE)
consumer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(consumer)


class PolicyInspectionTests(unittest.TestCase):
    def test_snapshot_cannot_claim_apply_load_or_ack(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.yaml'
            raw = b'epoch: 1\nprofile: fixture\n'
            path.write_bytes(raw)
            result = consumer.apply_preapproved(path)
            self.assertIs(result['applied'], False)
            self.assertIs(result['loaded'], False)
            self.assertIs(result['consumer_ack'], False)
            self.assertEqual(result['status'], 'INSPECTED_NOT_APPLIED')
            self.assertEqual(path.read_bytes(), raw)

    def test_malformed_yaml_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.yaml'
            path.write_text('epoch: [unterminated')
            with self.assertRaises(ValueError):
                consumer.apply_preapproved(path)

    def test_empty_mapping_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'empty.yaml'
            path.write_text('{}')
            with self.assertRaises(ValueError):
                consumer.apply_preapproved(path)

    def test_duplicate_yaml_key_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'duplicate.yaml'
            path.write_text('epoch: 1\nepoch: 2\n')
            with self.assertRaises(ValueError):
                consumer.apply_preapproved(path)

    def test_unknown_change_class_still_fails_closed(self):
        self.assertEqual(consumer.route_event('UNREGISTERED_B1')['verdict'], 'FAIL_CLOSED')


if __name__ == '__main__':
    unittest.main()
