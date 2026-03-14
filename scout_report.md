# Astropy Contribution Scout Report

Based on your profile (strong Python, statistics, physics; familiar with ML/sci-Python stack; no deep astronomy instrument knowledge yet), I've scouted the `astropy` issue tracker and curated these 3 "good first issues". All 3 avoid complex astronomy pipelines and lean into your existing Python/SciPy skills.

## Priority 1: Bug - Unnecessary logger info in `CCDData.read` when units match
**Upstream Issue:** #13539

**What's broken:**
When reading a FITS file using `CCDData.read(..., unit='...')`, Astropy logs an `INFO` message saying "using the unit X passed to the FITS reader instead of the unit Y in the FITS file" even if the unit X provided exactly matches the unit Y in the file. This creates noisy logs when it should just silently accept the unit since it matches.

**Exact files to touch:**
- Source: `astropy/nddata/ccddata.py`
- Test: `astropy/nddata/tests/test_ccddata.py`

**Step-by-step implementation approach:**
1. Open `astropy/nddata/ccddata.py`.
2. Locate the `CCDData.read` function (specifically the block handling the `unit` parameter around line ~770).
3. Find the `else` branch that executes when `unit` is not None and logs the message: `log.info(f"using the unit {unit} passed to the FITS reader...")`.
4. Add a conditional check: `if unit != fits_unit_string:` to ensure the message is only logged if the units are actually different.
5. In `astropy/nddata/tests/test_ccddata.py`, locate `test_infol_logged_if_unit_in_fits_header` (or create a new test `test_infol_not_logged_if_unit_matches`).
6. Create a test that passes the exact same unit string to `CCDData.read` that is stored in the header. Use `with log.log_to_list() as log_list:` and assert that the log list is empty.

**Acceptance criteria:**
- The log message is skipped if `unit == fits_unit_string`.
- Existing tests pass.
- A new or updated test verifies that matching units produce no INFO logs.

**What NOT to change:**
- Do not change how invalid units are handled or parsed (e.g., `known_invalid_fits_unit_strings`).
- Do not change the fallback behavior where `unit` overrides `fits_unit_string`.

**Difficulty:** 1/5
**Why tackle this today?** It's a quick win. It's a pure Python logic bug in the `nddata` module, requires zero astronomy knowledge, and lets you quickly familiarize yourself with the astropy PR and test suite process.


## Priority 2: Enhancement - Enable both `quantity_support` and `time_support` in one go
**Upstream Issue:** #8860

**What's broken:**
To plot both `astropy.units.Quantity` (e.g., arrays with physical units) and `astropy.time.Time` objects in matplotlib, users currently have to manually enable two separate context managers or functions: `visualization.quantity_support()` and `visualization.time_support()`. It would be cleaner to have a single helper `astropy_support()` that enables both simultaneously.

**Exact files to touch:**
- Source: `astropy/visualization/__init__.py` and create a new file `astropy/visualization/astropy_support.py` (or add to `time.py` / `units.py`).
- Test: `astropy/visualization/tests/test_units.py` or a new test file.

**Step-by-step implementation approach:**
1. Create a function `astropy_support(**kwargs)` in a relevant visualization module (e.g., `astropy/visualization/units.py` or a new file).
2. The function should use `contextlib.ExitStack` or a custom context manager class.
3. Separate the `kwargs`. `format` can go to `quantity_support()`. `scale`, `format`, and `simplify` can go to `time_support()`.
4. Enter both contexts (`quantity_support` and `time_support`) when `astropy_support` is entered, and exit both when exited.
5. Expose `astropy_support` in `astropy/visualization/__init__.py`.
6. Add a test in `astropy/visualization/tests/` to verify that plotting a `Time` array on the X-axis and a `Quantity` array on the Y-axis works seamlessly under the `astropy_support()` context.

**Acceptance criteria:**
- Users can do `with astropy_support(): plt.plot(time_array, quantity_array)`.
- The new function correctly passes relevant kwargs to the underlying `quantity_support` and `time_support`.
- Full test coverage for the context manager behavior.

**What NOT to change:**
- Do not modify the internals of `quantity_support` or `time_support`. They should remain independent and untouched.
- Do not add matplotlib as a strict runtime dependency (it is an optional dependency).

**Difficulty:** 2/5
**Why tackle this today?** Excellent exercise in Python context managers and API design. It bridges two very common Astropy objects (Quantities and Time) with standard Matplotlib workflows, perfectly aligning with a scientific Python background.


## Priority 3: Feature Request - `scipy.special` functions do not work with Quantities
**Upstream Issue:** #6390

**What's broken:**
When using `scipy.special` functions like `erf(5*u.m / (6*u.m))`, Astropy raises a `TypeError: Unknown ufunc erf` because it doesn't know how to handle the units. Since `erf` and many other `scipy.special` functions operate on dimensionless inputs, Astropy's unit system needs to be taught how to handle these ufuncs via `astropy.units.quantity_helper`.

**Exact files to touch:**
- Source: `astropy/units/quantity_helper/scipy_special.py`
- Test: `astropy/units/tests/test_quantity_ufuncs.py`

**Step-by-step implementation approach:**
1. Open `astropy/units/quantity_helper/scipy_special.py`.
2. Look at the tuple `dimensionless_to_dimensionless_sps_ufuncs`.
3. The issue mentions missing functions like Bessel functions (`jv`, `jn`, `yv`, `yn`, etc.), Legendre functions, and Riemann zeta (`zeta`, `zetac`).
4. Review scipy's documentation to see the expected input/output dimensionality for these functions. Many are two-argument functions where the order is dimensionless (or an integer) and the argument is dimensionless, or one-argument dimensionless functions.
5. Add the missing function names as strings to the appropriate tuples (e.g., `dimensionless_to_dimensionless_sps_ufuncs` or `two_arg_dimensionless_sps_ufuncs`).
6. Update `astropy/units/tests/test_quantity_ufuncs.py`. Add the new functions to `erf_like_ufuncs` or create a new test block so they are parametrized and tested for scalar/array dimensionless inputs.

**Acceptance criteria:**
- Passing a dimensionless `astropy.units.Quantity` (like `1.0 * u.dimensionless_unscaled` or `1 * u.m / u.m`) to `scipy.special.jv` (and others) successfully returns a calculated dimensionless Quantity instead of raising a `TypeError`.
- Tests are added for the newly supported ufuncs.

**What NOT to change:**
- Do not eagerly import `scipy` at the module level in `astropy.units`. `scipy` is an optional dependency, so it must only be imported dynamically when needed (as currently implemented in `quantity_helper`).

**Difficulty:** 2/5
**Why tackle this today?** It heavily leverages your SciPy background! Adding ufunc support in Astropy is mostly a matter of registering the right mathematical operations in the mapping dictionaries, but requires a solid understanding of the math functions involved (which you have).
