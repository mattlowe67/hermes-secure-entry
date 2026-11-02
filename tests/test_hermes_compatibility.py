"""Compatibility gate plus real native registry schema (no credentials)."""
import inspect
from pathlib import Path
import unittest
import hermes_yaml as yaml
from packaging.specifiers import SpecifierSet
from agent.vault_backends import unlock
from tools import browser_vault_tool  # register the actual native handler
from tools.registry import registry


class HermesCompatibilityTests(unittest.TestCase):
    def test_manifest_accepts_exercised_current_host_and_excludes_next_minor(self):
        manifest = yaml.safe_load((Path(__file__).parents[1] / 'plugin.yaml').read_text(encoding='utf-8'))
        supported = SpecifierSet(manifest['requires_hermes'])
        self.assertIn('0.22.1', supported)
        self.assertIn('0.22.5', supported)
        self.assertNotIn('0.22.6', supported)
        self.assertNotIn('0.23.0', supported)

    def test_actual_registered_native_schema_retains_intercepted_actions(self):
        entry = registry.get_entry('browser_vault')
        self.assertIsNotNone(entry)
        schema = entry.schema
        if 'function' in schema:
            schema = schema['function']
        actions = schema['parameters']['properties']['action']['enum']
        for action in ('list', 'unlock', 'enter_code', 'fill', 'save_login'):
            self.assertIn(action, actions)
        for name in ('set_code_prompt_callback', 'set_unlock_prompt_callback'):
            self.assertEqual(len(inspect.signature(getattr(unlock, name)).parameters), 1)
        for name in ('get_code_prompt_callback', 'get_unlock_prompt_callback'):
            self.assertEqual(len(inspect.signature(getattr(unlock, name)).parameters), 0)
