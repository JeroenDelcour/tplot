from typing import Iterable

import numpy as np


class Scale:
    """Base `Scale` class."""

    def __init__(self):
        pass

    def transform(self, values):
        if isinstance(values, np.ndarray):
            if isinstance(self, CategoricalScale):
                return np.vectorize(self._transform)(values)
            else:
                return self._transform(values)
        elif isinstance(values, str):
            return self._transform(values)
        elif isinstance(values, Iterable):
            return [self._transform(v) for v in values]
        else:
            return self._transform(values)

    def _transform(self, value):
        raise NotImplementedError


class LinearScale(Scale):
    """Transform numerical values linearly."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min, target_max):
        """Fit transform to linearly scale `values` to `target_min` and `target_max`."""
        original_min = min(tuple(values))
        original_max = max(tuple(values))
        if original_min == original_max:
            original_min -= 1
            original_max += 1
        original_range = original_max - original_min
        target_range = target_max - target_min

        def _transform(value):
            return target_range * (value - original_min) / original_range + target_min

        self._transform = _transform


class CategoricalScale(Scale):
    """Transform arbitrary values (e.g. strings) to numerical values."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min=0, target_max=None):
        """Fit transform to map `values` to numbers evenly spaced from `target_min` to `target_max`."""
        values = [str(v) for v in values]
        idxmap = {value: i for i, value in enumerate(sorted(set(values)))}
        if target_min == 0 and target_max is None:
            target_max = len(idxmap) - 1
        scale = LinearScale()
        scale.fit(list(idxmap.values()), target_min, target_max)
        idxmap = {value: scale.transform([i])[0] for value, i in idxmap.items()}

        def _transform(value):
            return idxmap[str(value)]

        self._transform = _transform
