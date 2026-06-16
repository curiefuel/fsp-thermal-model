# fsp-thermal-model

**Thermal system model for fission surface power (FSP) systems**

Reactor → Heat Pipes → Stirling Converters → Radiators → Electric Output

## Overview

This package models the complete thermal chain for a fission surface power system designed for lunar or Martian surface deployment. It includes:

- **Heat pipe network**: Sodium/potassium vapor-transport heat pipes with capillary and sonic limits
- **Stirling power conversion**: Thermodynamic cycle efficiency, mechanical losses, degradation
- **Thermal radiators**: Stefan-Boltzmann heat rejection, dust degradation, mass optimization
- **System integration**: Complete mass budget, uncertainty quantification, reliability analysis

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from fsp_thermal.system import FSPThermalSystem

system = FSPThermalSystem(
    target_electric_kwe=40,
    reactor_temp_k=900,
    cold_side_temp_k=400,
    working_fluid='sodium',
    environment='lunar',
)

system.summary()
```

## Examples

Run the baseline system analysis:

```bash
python examples/fsp01_baseline.py
```

Run the efficiency sweep (demonstrates radiator mass sensitivity):

```bash
python examples/efficiency_sweep.py
```

## Key Insight

**Every 1% improvement in Stirling efficiency saves ~100 kg of radiator mass.**

This is the fundamental design lever for FSP systems. The efficiency sweep example demonstrates this relationship with physics-based calculations.

## Physics References

- Chi, S.W. (1976). *Heat Pipe Theory and Practice*
- Walker, G. (1980). *Stirling Engines*
- Dunn & Reay (1994). *Heat Pipes*, 4th edition
- Gilmore (2002). *Spacecraft Thermal Control Handbook*
- NASA/TM-2012-217117: Space Radiator Design
- NASA/CR-2005-213913: Stirling Convertor
- NASA/CR-2017-219456: FSP Heat Pipe Design

## License

MIT License — see LICENSE file for details.

## Author

**Curiefuel**  
https://curiefuel.com  
hello@curiefuel.com
# fsp-thermal-model
