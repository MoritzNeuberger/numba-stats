"""
Poisson distribution.

See Also
--------
scipy.stats.poisson: Scipy equivalent.
"""

import numpy as np
from ._special import gammaincc as _gammaincc
from math import lgamma as _lgamma
from ._util import _jit, _generate_wrappers, _prange, _seed
import numba as nb

_doc_par = """
mu : float
    Expected value.
"""


@_jit(1)
def _logpmf(k, mu):
    T = type(mu)
    r = np.empty(len(k), T)
    for i in _prange(len(r)):
        if mu == 0:
            r[i] = 0.0 if k[i] == 0 else -np.inf
        else:
            r[i] = k[i] * np.log(mu) - _lgamma(k[i] + T(1)) - mu
    return r


@_jit(1)
def _pmf(k, mu):
    return np.exp(_logpmf(k, mu))


@_jit(1, cache=False)
def _cdf(k, mu):
    T = type(mu)
    r = np.empty(len(k), T)
    for i in _prange(len(r)):
        r[i] = _gammaincc(k[i] + T(1), mu)
    return r


@nb.njit(
    nb.int64[:](nb.float32, nb.uint64, nb.optional(nb.uint64)),
    cache=True,
    inline="always",
    error_model="numpy",
)
def _rvs(mu, size, random_state):
    _seed(random_state)
    return np.random.poisson(mu, size)


_generate_wrappers(globals())
