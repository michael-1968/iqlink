from django.test import TestCase
from .fomProgress import FomProgress

class FomProgressTests(TestCase):

    def test_fomProgress(self):
        fomprogress = FomProgress([1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0])
        res = False
        self.assertEqual(fomprogress.fomPerIteration, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        fomprogress.push(0, -1.5)
        self.assertEqual(fomprogress.fomPerIteration, [-1.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        fomprogress.push(0, -2.5)
        self.assertEqual(fomprogress.fomPerIteration, [-2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        fomprogress.push(0, -2.0)
        self.assertEqual(fomprogress.fomPerIteration, [-2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        fomprogress.push(10, -2.0)
        self.assertEqual(fomprogress.fomPerIteration, [-2.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2.0, 0])
        res = fomprogress.compare(0, -2.0)
        self.assertEqual(res, True)
        res = fomprogress.compare(0, -4.0)
        self.assertEqual(res, True)
        res = fomprogress.compare(0, -1.0)
        self.assertEqual(res, True)
        res = fomprogress.compare(0, -0.9)
        self.assertEqual(res, False)
        res = fomprogress.compare(0, +0.9)
        self.assertEqual(res, False)
        res = fomprogress.compare(0, 0)
        self.assertEqual(res, False)
        res = fomprogress.compare(10, -2)
        self.assertEqual(res, True)
        res = fomprogress.compare(10, -1)
        self.assertEqual(res, True)
        res = fomprogress.compare(10, +0.9)
        self.assertEqual(res, False)






