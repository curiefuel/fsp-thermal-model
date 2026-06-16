# Skill: Physics Documentation

Use this skill when writing docs/theory.md for any 
Curiefuel open source physics package.

## Structure of theory.md

Every theory.md must have these sections:

### 1. Overview
One paragraph explaining what physical system is being modeled
and what questions the tool answers.

### 2. Governing equations
For each major model in the package, write:
- The physical phenomenon being modeled
- The governing equation in LaTeX notation
- Definition of every variable with units
- Assumptions and their validity range
- The reference where the equation comes from

Example format:
```
## Radiator Heat Rejection

Space radiators reject waste heat by thermal radiation. 
The Stefan-Boltzmann law gives heat flux per unit area:

    q = ε · σ · T⁴

Where:
- q = heat flux [W/m²]
- ε = emissivity (0.90 for carbon composite BOL)
- σ = Stefan-Boltzmann constant = 5.6704 × 10⁻⁸ [W/m²/K⁴]
- T = radiator surface temperature [K]

Valid for: gray body, vacuum environment, no view factor constraints.
Reference: Gilmore (2002), Spacecraft Thermal Control Handbook, Ch. 3
```

### 3. Uncertainty sources
For each model, list:
- What physical parameters are uncertain and why
- Typical uncertainty ranges from published data
- How uncertainty compounds across the system
- Why Monte Carlo is the right tool (not worst-case stacking)

### 4. Key insights
2-3 paragraphs on the non-obvious engineering insights
the tool surfaces. These should be citable claims that
distinguish Curiefuel's analysis from back-of-envelope estimates.

Example:
```
## The Efficiency Lever

The single most impactful design parameter in an FSP system is 
Stirling conversion efficiency. This is counterintuitive — most 
engineers focus on reactor thermal output. But because radiator 
mass scales with waste heat, and waste heat is (1-η) × Q_thermal,
a 1% improvement in η reduces radiator area by approximately X m²
and system mass by approximately Y kg for a 40 kWe system.

This compounds: a lighter radiator means a lighter structure,
which means more margin for payload or fuel. The sensitivity
is nonlinear above 30% efficiency.
```

### 5. Validation
Compare model outputs against at least one published reference:
- NASA technical report
- Peer-reviewed journal paper
- Published mission data

Show a table: model output vs published value vs % error.

### 6. References
Full citations in this format:
Author, A.A. (Year). Title. Publisher/Journal. 
NASA/TM-XXXX or DOI if available.

## Writing standards
- No marketing language
- Every claim has a number behind it
- Every number has a unit
- Every equation has a reference
- Write as if a NASA engineer will review it
- Use past tense for established physics
- Use present tense for model behavior
