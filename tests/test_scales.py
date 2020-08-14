import unittest
import numpy as np
import tplot


class TestScales(unittest.TestCase):

    def test_linear(self):
        data = [-1, 3, -0.5, 4]
        scale = tplot.scales.LinearScale()
        scale.fit(data, target_min=-1, target_max=1)
        self.assertEqual(scale.transform(4), 1)
        self.assertEqual(scale.transform(-1), -1)
        self.assertEqual(scale.transform(1.5), 0)
        self.assertEqual(scale.transform([4, -1, 1.5]), [1, -1, 0])
        np.testing.assert_array_equal(scale.transform(np.array([4, -1, 1.5])), np.array([1, -1, 0]))

    def test_linear_inverted(self):
        data = [-1, 3, -0.5, 4]
        scale = tplot.scales.LinearScale()
        scale.fit(data, target_min=1, target_max=-1)
        self.assertEqual(scale.transform(4), -1)
        self.assertEqual(scale.transform(-1), 1)

    def test_linear_single_value(self):
        scale = tplot.scales.LinearScale()
        scale.fit([1], target_min=0, target_max=1)
        self.assertEqual(scale.transform(1), 0.5)

    def test_categorical(self):
        data = ["eggs", 42, "bacon", "spam", "spam", "spam", "bacon", "spam", "eggs"]
        scale = tplot.scales.CategoricalScale()
        scale.fit(data)
        # should return index of lexically sorted string representation of unique values
        self.assertEqual(scale.transform(42), 0)
        self.assertEqual(scale.transform("42"), 0)
        self.assertEqual(scale.transform("bacon"), 1)
        self.assertEqual(scale.transform("eggs"), 2)
        self.assertEqual(scale.transform("spam"), 3)
        self.assertEqual(scale.transform(["42", "bacon", "eggs", "spam"]), [0, 1, 2, 3])
        np.testing.assert_array_equal(scale.transform(
            np.array(["42", "bacon", "eggs", "spam"])), np.array(([0, 1, 2, 3])))
