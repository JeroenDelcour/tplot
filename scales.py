from numbers import Number


class Scale:
    def __init__(self):
        pass

    def transform(self, values):
        if isinstance(values, Number):
            return self._transform([values])[0]
        else:
            return self._transform(values)

    def _transform(self, values):
        raise NotImplementedError


class LinearScale(Scale):
    """Transforms real values to real values linearly."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min, target_max):
        original_min = min(values)
        original_max = max(values)
        original_range = original_max - original_min
        target_range = target_max - target_min

        def _transform(values):
            return [target_range * (value - original_min) / original_range + target_min for value in values]
        self._transform = _transform


class NominalScale(Scale):
    """Maps unique values to real values."""

    def __init__(self):
        super().__init__()

    def fit(self, values, target_min=0, target_max=None):
        idxmap = {value: i for i, value in enumerate(sorted(set(values)))}
        if target_max is not None and target_max > len(idxmap):
            scale = LinearScale()
            scale.fit(list(idxmap.values()), target_min, target_max)
            idxmap = {value: scale.transform([i])[0] for value, i in idxmap.items()}

        def _transform(values):
            return [idxmap[value] for value in values]
        self._transform = _transform
