"""Behavior checks. Generate examples/make_example.py before running unittest."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('renderer', ROOT/'.agents/skills/wise-product-video/scripts/render.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RendererTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.movie = module.Movie(ROOT/'examples/generated/storyboard.json')

    def test_loop_boundary_matches(self):
        m = self.movie
        self.assertTrue(np.array_equal(m.frame(0), m.frame(m.duration-1/m.fps)))

    def test_background_stays_solid(self):
        m = self.movie
        for t in np.linspace(0, m.duration-1/m.fps, 20):
            pixels = np.array(m.frame(t))
            self.assertTrue(np.all(pixels[:, :m.x] == [159,232,112]))
            self.assertTrue(np.all(pixels[:, m.x+m.w:] == [159,232,112]))

    def test_gif_actually_changes(self):
        m = self.movie
        a = np.array(m.scene_image(4, .04))[350:420,160:230]
        self.assertTrue(any(not np.array_equal(a, np.array(m.scene_image(4,t))[350:420,160:230]) for t in (.2,.4,.8)))

    def test_bundled_video_decodes_and_animates(self):
        m = self.movie
        overlay = {'file':'@celebration-forest-green.mp4', 'box':[100,250,180,180], 'fps':60, 'max_duration':2, 'loop':False}
        m.load_media(overlay)
        frames, times = m.media[module.json.dumps(overlay, sort_keys=True)]
        self.assertGreater(len(frames), 60)
        self.assertFalse(np.array_equal(frames[0], frames[60]))

    def test_bad_transition_fails_before_render(self):
        config = module.json.loads((ROOT/'examples/generated/storyboard.json').read_text())
        for screen in config['screens'].values():
            screen['file'] = str(ROOT/'examples/generated'/screen['file'])
        config['scenes'][1]['transition']['type'] = 'typo'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'storyboard.json'
            path.write_text(module.json.dumps(config))
            with self.assertRaisesRegex(ValueError, 'Unknown transition'):
                module.Movie(path)


if __name__ == '__main__':
    unittest.main()
