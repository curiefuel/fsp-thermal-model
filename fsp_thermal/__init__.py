'''
fsp-thermal-model: Thermal system model for fission surface power

Reactor → Heat Pipes → Stirling Converters → Radiators → Electric Output

Modules:
- constants: Physical constants and material properties
- heat_pipes: Sodium/potassium heat pipe network modeling
- stirling: Stirling engine power conversion
- radiator: Space radiator heat rejection and sizing
- system: Integrated FSP system with uncertainty quantification
'''

__version__ = '0.1.0'

from .heat_pipes import HeatPipe, HeatPipeNetwork
from .stirling import StirlingConverter, StirlingArray
from .radiator import Radiator
from .system import FSPThermalSystem

__all__ = [
    'HeatPipe',
    'HeatPipeNetwork',
    'StirlingConverter',
    'StirlingArray',
    'Radiator',
    'FSPThermalSystem',
]
