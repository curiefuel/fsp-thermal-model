'''
Thermal radiator model for FSP heat rejection.

Radiators are the largest mass driver in FSP systems.
This module models radiator sizing, dust degradation,
and performance under lunar/Martian conditions.

References:
- NASA/TM-2012-217117 Space Radiator Design
- Gilmore (2002). Spacecraft Thermal Control Handbook
'''

import numpy as np
from dataclasses import dataclass
from .constants import SIGMA, RADIATOR_PROPERTIES, LUNAR_ENVIRONMENT


@dataclass
class Radiator:
    '''
    Carbon composite space radiator panel.

    Models heat rejection capacity, required area,
    and performance degradation from dust accumulation.
    '''

    rejection_temp_k: float = 400.0
    emissivity: float = 0.90
    areal_mass_kg_m2: float = 3.0
    environment: str = 'lunar'

    # Dust model
    dust_degradation_rate_per_year: float = 0.008

    # Uncertainty
    emissivity_uncertainty: float = 0.02
    temp_uncertainty: float = 5.0

    def heat_rejection_per_m2_w(self, temp_k: float = None,
                                 emissivity: float = None) -> float:
        '''Radiative heat rejection per unit area (W/m²).'''
        T = temp_k or self.rejection_temp_k
        e = emissivity or self.emissivity
        return e * SIGMA * T ** 4

    def area_required_m2(self, waste_heat_kwt: float) -> float:
        '''Area required to reject a given waste heat load.'''
        return (waste_heat_kwt * 1000) / self.heat_rejection_per_m2_w()

    def mass_kg(self, waste_heat_kwt: float) -> float:
        return self.area_required_m2(waste_heat_kwt) * self.areal_mass_kg_m2

    def effective_emissivity(self, elapsed_years: float) -> float:
        '''Emissivity degraded by dust accumulation over time.'''
        return max(0.70,
                   self.emissivity * (1 - self.dust_degradation_rate_per_year) ** elapsed_years)

    def sample_rejection_capacity_w_m2(self, rng: np.random.Generator,
                                         elapsed_years: float = 0.0) -> float:
        e = rng.normal(
            self.effective_emissivity(elapsed_years),
            self.emissivity_uncertainty
        )
        T = rng.normal(self.rejection_temp_k, self.temp_uncertainty)
        e = np.clip(e, 0.5, 0.95)
        T = max(200, T)
        return e * SIGMA * T ** 4

    def efficiency_vs_dust(self, years: np.ndarray) -> np.ndarray:
        '''Radiator efficiency as function of years of dust exposure.'''
        return np.array([
            self.effective_emissivity(y) / self.emissivity
            for y in years
        ])

    def area_sensitivity_to_efficiency(self, waste_heat_kwt: float,
                                        efficiency_range: tuple = (0.15, 0.35),
                                        n_points: int = 50) -> tuple:
        '''
        Shows how radiator area changes with conversion efficiency.
        Key insight: every efficiency point saves significant mass.
        '''
        effs = np.linspace(*efficiency_range, n_points)
        thermal_inputs = waste_heat_kwt / (1 - effs)
        waste_heats = thermal_inputs - waste_heat_kwt
        areas = np.array([self.area_required_m2(w) for w in waste_heats])
        return effs, areas

    def mass_savings_per_efficiency_point(self, electric_output_kwe: float,
                                           base_efficiency: float = 0.25) -> float:
        '''
        kg saved per 1% improvement in Stirling efficiency.
        This is the key design lever claim on the Curiefuel site.
        '''
        def system_radiator_mass(eff):
            thermal = electric_output_kwe / eff
            waste = thermal - electric_output_kwe
            return self.mass_kg(waste)

        mass_at_base = system_radiator_mass(base_efficiency)
        mass_at_base_plus_1 = system_radiator_mass(base_efficiency + 0.01)
        return mass_at_base - mass_at_base_plus_1

    def summary(self, waste_heat_kwt: float) -> dict:
        area = self.area_required_m2(waste_heat_kwt)
        return {
            'rejection_temp_k': self.rejection_temp_k,
            'emissivity_bol': self.emissivity,
            'emissivity_eol_15yr': round(self.effective_emissivity(15), 3),
            'area_required_m2': round(area, 1),
            'mass_kg': round(self.mass_kg(waste_heat_kwt), 1),
            'heat_flux_w_m2': round(self.heat_rejection_per_m2_w(), 1),
        }
