# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Quantity helpers for the scipy.special ufuncs.

Available ufuncs in this module are at
https://docs.scipy.org/doc/scipy/reference/special.html
"""

from astropy.units.core import dimensionless_unscaled
from astropy.units.errors import UnitsError, UnitTypeError

from . import UFUNC_HELPERS
from .helpers import (
    get_converter,
    helper_cbrt,
    helper_dimensionless_to_dimensionless,
    helper_two_arg_dimensionless,
)

dimensionless_to_dimensionless_sps_ufuncs = (
    "erf", "erfc", "erfcx", "erfi", "erfinv", "erfcinv",
    "gamma", "gammaln", "loggamma", "gammasgn", "psi", "rgamma", "digamma",
    "wofz", "dawsn", "entr", "exprel", "expm1", "log1p", "exp2", "exp10",
    "j0", "j1", "y0", "y1", "i0", "i0e", "i1", "i1e",
    "k0", "k0e", "k1", "k1e", "itj0y0", "it2j0y0", "iti0k0", "it2i0k0",
    "ndtr", "ndtri",
    # Kelvin functions
    "bei", "beip", "ber", "berp",
    "kei", "keip", "ker", "kerp",
    # Elliptic integrals (single argument)
    "ellipe", "ellipk", "ellipkm1",
    # Exponential / logarithm integrals
    "exp1", "expi",
    # Logistic / related
    "expit", "log_expit", "logit",
    # Struve integrals
    "it2struve0", "itmodstruve0", "itstruve0",
    # Kolmogorov distribution
    "kolmogi", "kolmogorov",
    # Normal-distribution helpers
    "log_ndtr", "ndtri_exp",
    # Miscellaneous
    "cosm1", "round", "spence", "wrightomega", "zetac",
)  # fmt: skip


scipy_special_ufuncs = dimensionless_to_dimensionless_sps_ufuncs
# ufuncs that require input in degrees and give dimensionless output.
degree_to_dimensionless_sps_ufuncs = ("cosdg", "sindg", "tandg", "cotdg")
scipy_special_ufuncs += degree_to_dimensionless_sps_ufuncs
two_arg_dimensionless_sps_ufuncs = (
    "jv", "jn", "jve", "yn", "yv", "yve", "kn", "kv", "kve", "iv", "ive",
    "hankel1", "hankel1e", "hankel2", "hankel2e",
    # Arithmetic-geometric mean
    "agm",
    # Beta function
    "beta", "betaln",
    # Binomial coefficient
    "binom",
    # Box-Cox transforms
    "boxcox", "boxcox1p", "inv_boxcox", "inv_boxcox1p",
    # Chi-squared distribution
    "chdtr", "chdtrc", "chdtri", "chdtriv",
    # Elliptic integrals (two arguments)
    "ellipeinc", "ellipkinc", "elliprc",
    # Orthogonal polynomial evaluation (order + x)
    "eval_chebyc", "eval_chebys", "eval_chebyt", "eval_chebyu",
    "eval_hermite", "eval_hermitenorm",
    "eval_laguerre", "eval_legendre",
    "eval_sh_chebyt", "eval_sh_chebyu", "eval_sh_legendre",
    # Exponential integral
    "expn",
    # Incomplete gamma functions
    "gammainc", "gammaincc", "gammainccinv", "gammaincinv",
    # Loss / divergence functions
    "huber", "pseudo_huber", "kl_div", "rel_entr",
    # Hypergeometric (two arguments)
    "hyp0f1",
    # Mathieu characteristic values
    "mathieu_a", "mathieu_b",
    # Modified Struve function
    "modstruve",
    # Owen's T function
    "owens_t",
    # Poisson distribution
    "pdtr", "pdtrc", "pdtri", "pdtrik",
    # Pochhammer / power-minus-1
    "poch", "powm1",
    # Smirnov distribution
    "smirnov", "smirnovi",
    # Student t distribution
    "stdtr", "stdtridf", "stdtrit",
    # Struve function
    "struve",
    # Tukey-Lambda distribution
    "tklmbda",
    # Cross-entropy helpers
    "xlogy", "xlog1py",
)  # fmt: skip
scipy_special_ufuncs += two_arg_dimensionless_sps_ufuncs

three_arg_dimensionless_sps_ufuncs = (
    # Binomial distribution
    "bdtr", "bdtrc", "bdtri", "bdtrik", "bdtrin",
    # Bessel polynomial weighted integral
    "besselpoly",
    # Incomplete beta functions
    "betainc", "betaincc", "betainccinv", "betaincinv",
    # Beta distribution inverse
    "btdtria", "btdtrib",
    # Noncentral chi-squared distribution
    "chndtr", "chndtridf", "chndtrinc", "chndtrix",
    # Elliptic integrals (three arguments)
    "elliprd", "elliprf", "elliprg",
    # Orthogonal polynomial evaluation (three arguments)
    "eval_gegenbauer", "eval_genlaguerre",
    # F distribution
    "fdtr", "fdtrc", "fdtri", "fdtridfd",
    # Gamma distribution
    "gdtr", "gdtrc", "gdtria", "gdtrib", "gdtrix",
    # Hypergeometric (three arguments)
    "hyp1f1", "hyperu",
    # Wright Bessel (log variant)
    "log_wright_bessel",
    # Associated Legendre function
    "lpmv",
    # Negative binomial distribution
    "nbdtr", "nbdtrc", "nbdtri", "nbdtrik", "nbdtrin",
    # Noncentral t distribution
    "nctdtr", "nctdtridf", "nctdtrinc", "nctdtrit",
    # Normal distribution (mean / std inverses)
    "nrdtrimn", "nrdtrisd",
    # Spheroidal wave characteristic values
    "obl_cv", "pro_cv",
    # Voigt profile
    "voigt_profile",
    # Wright Bessel function
    "wright_bessel",
)  # fmt: skip
scipy_special_ufuncs += three_arg_dimensionless_sps_ufuncs

four_arg_dimensionless_sps_ufuncs = (
    # Elliptic integral (four arguments)
    "elliprj",
    # Orthogonal polynomial evaluation (four arguments)
    "eval_jacobi", "eval_sh_jacobi",
    # Gauss hypergeometric function
    "hyp2f1",
    # Noncentral F distribution
    "ncfdtr", "ncfdtri", "ncfdtridfd", "ncfdtridfn", "ncfdtrinc",
)  # fmt: skip
scipy_special_ufuncs += four_arg_dimensionless_sps_ufuncs

# ufuncs handled as special cases
scipy_special_ufuncs += ("cbrt", "radian")


def helper_degree_to_dimensionless(f, unit):
    from astropy.units.si import degree

    try:
        return [get_converter(unit, degree)], dimensionless_unscaled
    except UnitsError:
        raise UnitTypeError(
            f"Can only apply '{f.__name__}' function to quantities with angle units"
        )


def helper_degree_minute_second_to_radian(f, unit1, unit2, unit3):
    from astropy.units.si import arcmin, arcsec, degree, radian

    try:
        return [
            get_converter(unit1, degree),
            get_converter(unit2, arcmin),
            get_converter(unit3, arcsec),
        ], radian
    except UnitsError:
        raise UnitTypeError(
            f"Can only apply '{f.__name__}' function to quantities with angle units"
        )


def helper_three_arg_dimensionless(f, unit1, unit2, unit3):
    """Helper for ufuncs that require three dimensionless inputs."""
    try:
        converter1 = (
            get_converter(unit1, dimensionless_unscaled) if unit1 is not None else None
        )
        converter2 = (
            get_converter(unit2, dimensionless_unscaled) if unit2 is not None else None
        )
        converter3 = (
            get_converter(unit3, dimensionless_unscaled) if unit3 is not None else None
        )
    except UnitsError:
        raise UnitTypeError(
            f"Can only apply '{f.__name__}' function to dimensionless quantities"
        )
    return ([converter1, converter2, converter3], dimensionless_unscaled)


def helper_four_arg_dimensionless(f, unit1, unit2, unit3, unit4):
    """Helper for ufuncs that require four dimensionless inputs."""
    try:
        converters = [
            get_converter(unit, dimensionless_unscaled) if unit is not None else None
            for unit in (unit1, unit2, unit3, unit4)
        ]
    except UnitsError:
        raise UnitTypeError(
            f"Can only apply '{f.__name__}' function to dimensionless quantities"
        )
    return (converters, dimensionless_unscaled)


def get_scipy_special_helpers():
    import scipy.special as sps

    SCIPY_HELPERS = {}
    for name in dimensionless_to_dimensionless_sps_ufuncs:
        ufunc = getattr(sps, name, None)
        if ufunc is not None:
            SCIPY_HELPERS[ufunc] = helper_dimensionless_to_dimensionless

    for name in degree_to_dimensionless_sps_ufuncs:
        ufunc = getattr(sps, name, None)
        if ufunc is not None:
            SCIPY_HELPERS[ufunc] = helper_degree_to_dimensionless

    for name in two_arg_dimensionless_sps_ufuncs:
        ufunc = getattr(sps, name, None)
        if ufunc is not None:
            SCIPY_HELPERS[ufunc] = helper_two_arg_dimensionless

    for name in three_arg_dimensionless_sps_ufuncs:
        ufunc = getattr(sps, name, None)
        if ufunc is not None:
            SCIPY_HELPERS[ufunc] = helper_three_arg_dimensionless

    for name in four_arg_dimensionless_sps_ufuncs:
        ufunc = getattr(sps, name, None)
        if ufunc is not None:
            SCIPY_HELPERS[ufunc] = helper_four_arg_dimensionless

    # ufuncs handled as special cases
    SCIPY_HELPERS[sps.cbrt] = helper_cbrt
    SCIPY_HELPERS[sps.radian] = helper_degree_minute_second_to_radian
    return SCIPY_HELPERS


UFUNC_HELPERS.register_module(
    "scipy.special", scipy_special_ufuncs, get_scipy_special_helpers
)
