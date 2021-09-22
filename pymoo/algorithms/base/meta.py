from copy import deepcopy

from pymoo.core.algorithm import Algorithm


class MetaAlgorithm(Algorithm):

    def __init__(self,
                 algorithm,
                 copy=False,
                 ):
        super().__init__()

        # if the algorithm object should be copied to keep the original one unmodified
        if copy:
            algorithm = deepcopy(algorithm)

        # store the current algorithm object to be iterated over
        self.algorithm = algorithm

    def _copy_from_orig(self):
        for k, v in self.algorithm.__dict__.items():
            self.__dict__[k] = v

        self.__dict__["display"] = None

    def setup(self, *args, **kwargs):
        self.algorithm.setup(*args, **kwargs)
        self._copy_from_orig()
        self._setup(*args, **kwargs)
        return self

    def _infill(self):
        ret = self.algorithm.infill()
        self._copy_from_orig()
        return ret

    def _initialize_infill(self):
        return self._infill()

    def _initialize_advance(self, infills=None, **kwargs):
        self.algorithm.advance(infills=infills, **kwargs)
        self._copy_from_orig()

    def _advance(self, infills=None, **kwargs):
        self.algorithm.advance(infills=infills, **kwargs)
        self._copy_from_orig()

    def advance(self, infills=None, **kwargs):
        super().advance(infills, **kwargs)
        self._copy_from_orig()

    def _set_optimum(self):
        self.opt = self.algorithm.opt
