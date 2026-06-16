'''
Stirling engine power conversion model for FSP systems.

Models thermodynamic cycle efficiency, mechanical losses,
and performance degradation over mission life.

Physics references:
- Walker (1980). Stirling Engines
- NASA/CR-2005-213913 Stirling Convertor
- Schreiber (2007). Advanced Stirling Convertor
'''

import numpy as np
from dataclasses import dataclass
from .constants import STIRLING_PROPERTIES


@dataclass
class StirlingConverter:
    '''
    Single Stirling power conversion unit.

    Based on NASA Advanced Stirling Convertor (ASC) specifications
    scaled for FSP application.
    '''

    hot_side_temp_k: float = 850.0
    cold_side_temp_k: float = 400.0
    mechanical_efficiency: float = 0.85
    design_power_kwe: float = 6.0

    # Uncertainty
    efficiency_uncertainty: float = 0.02
    degradation_rate_per_year: float = 0.004

    def carnot_efficiency(self) -> float:
        return 1 - (self.cold_side_temp_k / self.hot_side_temp_k)

    def ideal_stirling_efficiency(self) -> float:
        '''Ideal Stirling equals Carnot with perfect regeneration.'''
        return self.carnot_efficiency()

    def actual_efficiency(self) -> float:
        '''
        Actual efficiency accounts for regenerator effectiveness,
        mechanical losses, and heat transfer irreversibilities.
        Empirical correction: ~60-70% of Carnot for real systems.
        '''
        return self.ideal_stirling_efficiency() * self.mechanical_efficiency * 0.65

    def thermal_input_kwt(self) -> float:
        return self.design_power_kwe / self.actual_efficiency()

    def waste_heat_kwt(self) -> float:
        return self.thermal_input_kwt() - self.design_power_kwe

    def efficiency_at_temperature(self, hot_k: float, cold_k: float) -> float:
        '''Efficiency as function of operating temperatures.'''
        carnot = 1 - (cold_k / hot_k)
        return carnot * self.mechanical_efficiency * 0.65

    def sample_efficiency(self, rng: np.random.Generator,
                          elapsed_years: float = 0.0) -> float:
        nominal = self.actual_efficiency()
        degraded = nominal * ((1 - self.degradation_rate_per_year) ** elapsed_years)
        return max(0.05, rng.normal(degraded, degraded * self.efficiency_uncertainty))

    def sample_power_output(self, rng: np.random.Generator,
                            thermal_input_kwt: float,
                            elapsed_years: float = 0.0) -> float:
        eff = self.sample_efficiency(rng, elapsed_years)
        return thermal_input_kwt * eff

    def mass_kg(self) -> float:
        '''Approximate mass: 6 kg/kWe for advanced Stirling.'''
        return self.design_power_kwe * 6.0

    def summary(self) -> dict:
        return {
            'hot_side_temp_k': self.hot_side_temp_k,
            'cold_side_temp_k': self.cold_side_temp_k,
            'carnot_efficiency': round(self.carnot_efficiency(), 3),
            'actual_efficiency': round(self.actual_efficiency(), 3),
            'design_power_kwe': self.design_power_kwe,
            'thermal_input_kwt': round(self.thermal_input_kwt(), 1),
            'waste_heat_kwt': round(self.waste_heat_kwt(), 1),
            'mass_kg': self.mass_kg(),
        }


@dataclass
class StirlingArray:
    '''Array of Stirling converters with redundancy.'''

    n_units: int = 4
    unit: StirlingConverter = None

    def __post_init__(self):
        if self.unit is None:
            self.unit = StirlingConverter()

    @classmethod
    def for_power_output(cls, target_kwe: float,
                         hot_side_temp_k: float = 850.0,
                         cold_side_temp_k: float = 400.0) -> 'StirlingArray':
        unit = StirlingConverter(
            hot_side_temp_k=hot_side_temp_k,
            cold_side_temp_k=cold_side_temp_k,
        )
        n = int(np.ceil(target_kwe / unit.design_power_kwe)) + 1  # +1 redundant
        return cls(n_units=n, unit=unit)

    def total_power_kwe(self) -> float:
        return self.n_units * self.unit.design_power_kwe

    def total_thermal_input_kwt(self) -> float:
        return self.n_units * self.unit.thermal_input_kwt()

    def total_mass_kg(self) -> float:
        return self.n_units * self.unit.mass_kg()

    def sample_total_output(self, rng: np.random.Generator,
                             thermal_input_kwt: float,
                             elapsed_years: float = 0.0) -> float:
        per_unit = thermal_input_kwt / self.n_units
        return sum(
            self.unit.sample_power_output(rng, per_unit, elapsed_years)
            for _ in range(self.n_units)
        )

    def efficiency_curve(self, temp_range_k: tuple = (700, 1000),
                          n_points: int = 50) -> tuple:
        temps = np.linspace(*temp_range_k, n_points)
        effs = [self.unit.efficiency_at_temperature(t, self.unit.cold_side_temp_k)
                for t in temps]
        return temps, np.array(effs)

    def summary(self) -> dict:
        return {
            'n_units': self.n_units,
            'total_power_kwe': self.total_power_kwe(),
            'total_thermal_input_kwt': round(self.total_thermal_input_kwt(), 1),
            'overall_efficiency': round(self.unit.actual_efficiency(), 3),
            'total_mass_kg': self.total_mass_kg(),
        }
