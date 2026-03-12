# Scout Report: Good First Issues in astropy

I have reviewed the available "good first issue" candidates in the astropy codebase matching the profile requirements (Python/stats/math background, familiarity with scientific Python, low deep astronomy knowledge needed).

Here are the top 3 recommended issues for the day:

### 1. Issue #13539: Avoid logger info in CCDData.read when unit specifies matches that in FITS file
- **What's broken:** When reading a FITS file with `CCDData.read`, if you explicitly provide a `unit` argument (e.g., `unit=u.adu`) and the FITS file's `BUNIT` header already has the same unit (e.g., `'adu'`), a confusing log message is emitted: `"INFO:astropy:using the unit adu passed to the FITS reader instead of the unit adu in the FITS file."` This is redundant and should only log if the units are actually different.
- **Exact files to touch:**
  - Source: `astropy/nddata/ccddata.py`
  - Tests: `astropy/nddata/tests/test_ccddata.py`
- **Step-by-step implementation approach:**
  1. Open `astropy/nddata/ccddata.py`.
  2. Locate the `fits_ccddata_reader` function (around line 770).
  3. Change the `else:` block where `log.info(...)` is called. Currently it looks like:
     ```python
     else:
         log.info(
             f"using the unit {unit} passed to the FITS reader instead "
             f"of the unit {fits_unit_string} in the FITS file."
         )
     ```
  4. Update the code to first evaluate `fits_unit_string` into a `u.Unit` (if it isn't one already), and then compare `u.Unit(unit) != u.Unit(fits_unit_string)`. If they are different, only then emit the log. Catch `ValueError` in case `fits_unit_string` is unparseable (in which case they aren't equal, so we should log).
  5. Open `astropy/nddata/tests/test_ccddata.py` and write/modify a test that checks reading a FITS file with matching unit does not emit the warning (using `pytest.warns` or `caplog`).
- **Acceptance criteria:** When reading a FITS file with a unit passed that is physically equivalent to the FITS file's unit, no `INFO` log message is emitted. The tests pass.
- **What NOT to change:** Do not change how units are parsed or handled when they *do* differ, and do not change how the data is loaded.
- **Difficulty:** 1/5
- **Priority:** 1 - This is an excellent, extremely isolated bug fix that deals directly with core Python standard logging and astropy's Unit equality, making it very accessible.

---

### 2. Issue #6390: multiple functions from scipy.special do not work with quantities
- **What's broken:** Astropy allows variables with physical units (`Quantity` objects) to be passed into Numpy ufuncs. It also tries to support SciPy's special functions (like error functions, Bessel functions, etc.), but many of them raise a `TypeError: Unknown ufunc` when a Quantity is passed to them.
- **Exact files to touch:**
  - Source: `astropy/units/quantity_helper/scipy_special.py`
  - Tests: `astropy/units/tests/test_quantity_ufuncs.py`
- **Step-by-step implementation approach:**
  1. Look at `astropy/units/quantity_helper/scipy_special.py`.
  2. There is a tuple `dimensionless_to_dimensionless_sps_ufuncs` and others like `two_arg_dimensionless_sps_ufuncs`.
  3. Compare the list of ufuncs in this file to the missing ones mentioned in the issue or available in `scipy.special` (e.g., Bessel functions `jv`, `yv`, Gamma functions, Legendre functions). Note: some of these may have been added since the issue was opened (as seen in `dimensionless_to_dimensionless_sps_ufuncs` which already contains `erf`, `gamma`, `j0`, etc).
  4. Identify any remaining missing `scipy.special` ufuncs. Add their string names to the relevant tuples (e.g., `two_arg_dimensionless_sps_ufuncs`).
  5. In `astropy/units/tests/test_quantity_ufuncs.py`, add the newly supported functions to the test parameters (e.g., `erf_like_ufuncs` tuple) so they are tested for array inputs and invalid units.
- **Acceptance criteria:** Passing a dimensionless `Quantity` (like `5 * u.m / (5 * u.m)`) to the newly added `scipy.special` ufuncs correctly evaluates the function and returns a dimensionless Quantity or float without raising a `TypeError`.
- **What NOT to change:** Do not rewrite the core `get_scipy_special_helpers` registration framework. Just extend the list of registered functions.
- **Difficulty:** 2/5
- **Priority:** 2 - Great issue for a scientific Python developer, getting into how Astropy Units map to SciPy functions. It's a bit older, so some functions are already supported, but expanding coverage is always appreciated.

---

### 3. Issue #6038: LinearLSQFitter cannot fit compound models
- **What's broken:** `LinearLSQFitter` crashes with an unhelpful error or `TypeError: 'NoneType' object is not callable` when trying to fit a compound model (e.g. `Chebyshev1D(2) | Chebyshev1D(2)`). `LinearLSQFitter` relies on solving a Vandermonde matrix, which it currently cannot construct for compound models.
- **Exact files to touch:**
  - Source: `astropy/modeling/fitting.py`
  - Tests: `astropy/modeling/tests/test_fitting.py`
- **Step-by-step implementation approach:**
  1. Open `astropy/modeling/fitting.py` and locate `LinearLSQFitter.__call__`.
  2. Add a check near the beginning of `__call__` to see if the `model` is a compound model (e.g., `isinstance(model, CompoundModel)` or checking if it has a `_is_dynamic` or composite nature).
  3. If it is a compound model, raise a clear `ModelLinearityError` explaining that "LinearLSQFitter cannot currently fit compound models. Please use a non-linear fitter."
  4. Check the `astropy/modeling/fitting.py` docstring for `LinearLSQFitter` and ensure it documents that compound models are not supported.
  5. Add a test in `astropy/modeling/tests/test_fitting.py` that asserts fitting a compound model with `LinearLSQFitter` raises the expected `ModelLinearityError`.
- **Acceptance criteria:** Attempting to fit a compound model with `LinearLSQFitter` gracefully raises a `ModelLinearityError` with a clear message, rather than a cryptic `TypeError`. The limitation is documented.
- **What NOT to change:** Do not attempt to actually implement the math to construct a Vandermonde matrix for compound models; the issue specifically states just adding an error and documentation is acceptable as a first step or to fix the crash.
- **Difficulty:** 1.5/5
- **Priority:** 3 - A solid issue in `astropy.modeling` that is very well-suited to someone with math/fitting background, but requires less deep modeling knowledge since the fix is mostly raising a clean error message and updating docs.
