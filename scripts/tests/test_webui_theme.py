"""The overlay must reject drift without touching any checkout."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'apply_webui_theme.py'
spec = importlib.util.spec_from_file_location('webui_theme', SCRIPT)
theme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(theme)


class OverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.overlay, self.target = root / 'overlay', root / 'webui'
        self.overlay.mkdir()
        self.target.mkdir()
        (self.target / 'package.json').write_text('{}')
        (self.target / 'one.vue').write_text('before')
        (self.overlay / 'one.vue').write_text('after')
        (self.overlay / 'new.scss').write_text('style')
        manifest = {
            'one.vue': {'original': theme.digest(self.target / 'one.vue'), 'replacement': theme.digest(self.overlay / 'one.vue')},
            'new.scss': {'original': None, 'replacement': theme.digest(self.overlay / 'new.scss')},
        }
        (self.overlay / 'manifest.json').write_text(json.dumps(manifest))
        self.patcher = patch.object(theme, 'OVERLAY', self.overlay)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_repeat_application_and_check(self):
        self.assertEqual(theme.apply([self.target]), 2)
        self.assertEqual(theme.apply([self.target]), 0)
        self.assertEqual(theme.apply([self.target], check=True), 0)

    def test_drift_in_second_target_leaves_first_unchanged(self):
        import shutil
        second = self.target.parent / 'other'
        shutil.copytree(self.target, second)
        (second / 'one.vue').write_text('local edit')
        with self.assertRaisesRegex(ValueError, 'file changed'):
            theme.apply([self.target, second])
        self.assertEqual((self.target / 'one.vue').read_text(), 'before')
        self.assertFalse((self.target / 'new.scss').exists())

    def test_overlay_corruption_is_rejected(self):
        (self.overlay / 'new.scss').write_text('unexpected')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            theme.apply([self.target])
        self.assertEqual((self.target / 'one.vue').read_text(), 'before')

    def test_check_does_not_apply(self):
        with self.assertRaisesRegex(ValueError, 'not applied'):
            theme.apply([self.target], check=True)
        self.assertEqual((self.target / 'one.vue').read_text(), 'before')


if __name__ == '__main__':
    unittest.main()
