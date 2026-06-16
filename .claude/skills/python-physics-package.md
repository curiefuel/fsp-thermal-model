# Skill: Python Physics Package

Use this skill whenever building a scientific Python package 
for Curiefuel's open source toolchain.

## Package structure
Every package must have exactly this at root:
- `README.md` — engineering document, not marketing
- `setup.py` — with author Curiefuel, url github.com/curiefuel
- `requirements.txt` — pinned major versions
- `LICENSE` — MIT
- `.gitignore` — Python standard plus project-specific

## Code standards

### Docstrings
Every module, class, and public method gets a docstring.
Module docstrings cite physics references.
Class docstrings explain the physical system being modeled.
Method docstrings explain the equation being implemented.

Example:
```python
def capillary_limit_w(self) -> float:
    '''
    Maximum heat transport from capillary pumping limit.
    
    Q_cap = (K * A_w * rho_l * h_fg / mu_l * L) * (2*sigma/r_pore - rho_l*g*L*sin(phi))
    
    Reference: Chi (1976), Heat Pipe Theory and Practice, eq. 3.14
    '''
```

### Units
Always include units in variable names and docstrings.
Use SI throughout: meters, kelvin, watts, kilograms, pascals.
Never mix unit systems.

### Uncertainty
Every physical model must have:
- A `sample_*` method that accepts `rng: np.random.Generator`
- An `elapsed_years` parameter for degradation modeling
- Uncertainty as a fraction of nominal (not absolute)

### Constants
Never hardcode physical constants in methods.
All constants go in `constants.py` with citation.

### Summary methods
Every class gets a `summary() -> dict` method returning
key engineering outputs as a flat dictionary.

## Examples
Every package needs at least one runnable example that:
- Imports from the package using installed path (not relative)
- Prints formatted output
- Runs with zero errors after `pip install -e .`
- Demonstrates the key engineering insight the tool provides

## Testing
pytest tests for every module covering:
- Nominal values match hand calculations
- Sample methods return non-negative values
- Degradation reduces output over time
- Summary methods return dicts with correct keys

## README structure
1. One-line description
2. What this does (3-4 sentences, engineering not marketing)
3. Why it exists (the gap it fills)
4. Installation
5. Quick start (runnable code block)
6. Key outputs
7. Physics models (link to docs/theory.md)
8. Validation (link to docs/validation.md)
9. License
10. Built by Curiefuel
