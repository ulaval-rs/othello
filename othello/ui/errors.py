class LessThenTwoCriteriaError(ValueError):
    pass


class EmptyNewCriterionNameError(ValueError):
    pass


class DuplicateNewCriterionNamesError(ValueError):
    pass


class WeightIsNotAFloatError(ValueError):
    pass


class SumOfWeightNotEqualsToOneError(ValueError):
    pass
