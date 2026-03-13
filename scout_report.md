# Good First Issues for Low-Experience Contributor

Here are 3-5 great issues that match the profile:

## 1. multiple functions from scipy.special do not work with quantities (Issue 6390)

**What's broken in plain English:**
Astropy's `Quantity` objects (numbers with physical units attached) should behave naturally when passed to mathematical functions. Many common functions from `numpy` and `scipy.special` are supported, but some like `erf` (error function) or `zeta` throw errors when you pass a unit-less `Quantity` to them (like `5m / 6m`).

**Exact files to touch:**
- `astropy/units/quantity_helper/scipy_special.py` (Source)
- `astropy/units/tests/test_quantity_ufuncs.py` (Test file)

**Step-by-step implementation approach:**
1. Open `astropy/units/quantity_helper/scipy_special.py`.
2. Find the tuple `dimensionless_to_dimensionless_sps_ufuncs`.
3. Add the missing functions mentioned in the issue: `zeta`, `zetac`, etc. Ensure we add missing functions from Error functions, Bessel functions, Gamma functions, Legendre functions.
4. If there are functions that take two arguments, add them to `two_arg_dimensionless_sps_ufuncs`.
5. Run the existing tests in `test_quantity_ufuncs.py` (specifically `test_scipy_special`).
6. Ensure the newly added functions pass the tests.

**Acceptance criteria:**
- The added `scipy.special` functions work when given dimensionless `Quantity` inputs.
- Tests pass.

**What NOT to change:**
- Do not change the core `Quantity` implementation or other `quantity_helper` logic. Just update the supported function lists.

**Difficulty:** 1/5

**Priority:** 1 (Highest priority - clear scope, easy to verify, matches profile perfectly).

---

## 2. Provide a way to enable both quantity_support and time_support in one go (Issue 8860)

**What's broken in plain English:**
Astropy provides two context managers/functions to enable nice plotting with matplotlib: `quantity_support()` (for unit-aware plotting) and `time_support()` (for time-aware plotting). Currently, users have to enable both separately. Users want a single function (e.g., `astropy_support()`) that enables both at once.

**Exact files to touch:**
- `astropy/visualization/units.py` (or similar file where these supports are defined, likely `astropy/visualization/__init__.py` or `astropy/visualization/support.py`)
- `astropy/visualization/tests/test_units.py` (or similar test file)

**Step-by-step implementation approach:**
1. Locate where `quantity_support` and `time_support` are defined (likely in `astropy.visualization`).
2. Create a new function `astropy_support()`.
3. Inside `astropy_support`, call both `quantity_support()` and `time_support()`. Return a combined context manager (similar to how `quantity_support` works).
4. Write a simple test to verify that calling `astropy_support()` enables both correctly.

**Acceptance criteria:**
- Calling `astropy_support()` correctly sets up plotting for both Quantities and Times.
- It can be used as a context manager (`with astropy_support():`).

**What NOT to change:**
- Do not modify how `quantity_support` or `time_support` work individually.

**Difficulty:** 2/5

**Priority:** 2

---

## 3. convolve_fft defaults and documentation (Issue 8426)

**What's broken in plain English:**
The default behavior of `convolve_fft` in the `astropy.convolution` module was changed at some point, causing backwards compatibility issues for users who expected the old defaults (specifically regarding how NaNs are handled and whether the kernel is normalized). The documentation and examples don't reflect these new defaults, leading to confusion.

**Exact files to touch:**
- `astropy/convolution/convolve.py` (Docstring and defaults)
- `docs/convolution/index.rst` (or related doc files)

**Step-by-step implementation approach:**
1. Open `astropy/convolution/convolve.py` and find `convolve_fft`.
2. Update the docstring to clearly explain the current defaults for `nan_treatment` and `normalize_kernel`, explicitly noting when they changed (check `git blame` or the issue history if needed, though mostly just documenting the current state is the goal).
3. Fix the examples in the docstrings to show the correct output based on the new defaults.
4. Build the docs locally to verify changes.

**Acceptance criteria:**
- The docstring for `convolve_fft` accurately describes the current defaults.
- The examples in the documentation produce the output stated.

**What NOT to change:**
- Do not change the actual code logic or default values of `convolve_fft`. This is purely a documentation/example fix.

**Difficulty:** 1.5/5

**Priority:** 3 (Bumping down slightly as it's an older issue and mostly documentation, but still a great first PR).
