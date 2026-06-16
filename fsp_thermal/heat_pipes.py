'''
Heat pipe network model for fission surface power systems.

Models sodium or potassium vapor-transport heat pipes connecting
the reactor core to the power conversion unit.

Physics references:
- Chi, S.W. (1976). Heat Pipe Theory and Practice
- Dunn & Reay (1994). Heat Pipes, 4th edition
- NASA/CR-2017-219456 FSP Heat Pipe Design
'''

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from .constants import SODIUM_PROPERTIES, POTASSIUM_PROPERTIES


@dataclass
class HeatPipe:
    '''
    Single heat pipe model.

    Calculates maximum heat transport capacity, thermal resistance,
    and failure probability under uncertainty.
    '''

    length_m: float = 1.5
    outer_diameter_m: float = 0.022
    wall_thickness_m: float = 0.001
    wick_thickness_m: float = 0.002
    working_fluid: str = 'sodium'
    operating_temp_k: float = 900.0
    inclination_deg: float = 0.0  # positive = evaporator above condenser (adverse)

    # Uncertainty parameters
    conductance_uncertainty: float = 0.05
    degradation_rate_per_year: float = 0.003

    def _fluid_props(self) -> dict:
        if self.working_fluid == 'sodium':
            return SODIUM_PROPERTIES
        elif self.working_fluid == 'potassium':
            return POTASSIUM_PROPERTIES
        raise ValueError(f'Unknown fluid: {self.working_fluid}')

    def vapor_core_diameter_m(self) -> float:
        return (self.outer_diameter_m -
                2 * self.wall_thickness_m -
                2 * self.wick_thickness_m)

    def capillary_limit_w(self) -> float:
        '''Maximum heat transport from capillary pumping limit.'''
        props = self._fluid_props()
        r_v = self.vapor_core_diameter_m() / 2

        # Capillary pressure
        r_pore = self.wick_thickness_m / 100  # approx pore radius
        delta_p_cap = 2 * props['surface_tension_n_m'] / r_pore

        # Gravity pressure penalty
        g = 1.62  # lunar gravity
        delta_p_grav = (props['liquid_density_kg_m3'] * g *
                        self.length_m * np.sin(np.radians(self.inclination_deg)))

        effective_pressure = delta_p_cap - delta_p_grav

        # Wick permeability (approximation)
        permeability = (self.wick_thickness_m ** 2) / 150

        a_wick = (np.pi * ((r_v + self.wick_thickness_m)**2 - r_v**2))

        # Capillary limit formula: Q = (K * A * Δp * h_fg * ρ_l) / (μ_l * L)
        return (permeability * a_wick * effective_pressure *
                props['latent_heat_j_kg'] * props['liquid_density_kg_m3'] /
                (props['liquid_viscosity_pa_s'] * self.length_m))

    def vapor_pressure_limit_w(self) -> float:
        '''Sonic limit — maximum axial vapor velocity.'''
        props = self._fluid_props()
        r_v = self.vapor_core_diameter_m() / 2
        a_v = np.pi * r_v ** 2

        # Approximate sonic limit
        gamma = 1.67  # monatomic vapor
        R = 8.314 / 0.023  # sodium molar mass ~23 g/mol
        c_sound = np.sqrt(gamma * R * self.operating_temp_k)

        return (props['vapor_density_kg_m3'] *
                props['latent_heat_j_kg'] *
                a_v * c_sound / 2)

    def max_heat_transport_w(self) -> float:
        return min(self.capillary_limit_w(), self.vapor_pressure_limit_w())

    def thermal_resistance_k_w(self) -> float:
        '''Effective thermal resistance of the heat pipe.'''
        props = self._fluid_props()
        k_wall = 15.0  # stainless steel W/m/K
        r_outer = self.outer_diameter_m / 2
        r_inner = r_outer - self.wall_thickness_m

        # Wall resistance
        r_wall = np.log(r_outer / r_inner) / (2 * np.pi * k_wall * self.length_m)

        # Wick resistance
        r_wick = np.log(r_inner / (r_inner - self.wick_thickness_m)) / (
            2 * np.pi * props['thermal_conductivity_w_mk'] * self.length_m)

        # Vapor resistance (negligible for alkali metals)
        r_vapor = 1e-6

        return r_wall + r_wick + r_vapor

    def conductance_w_k(self) -> float:
        return 1.0 / self.thermal_resistance_k_w()

    def sample_conductance(self, rng: np.random.Generator,
                           elapsed_years: float = 0.0) -> float:
        '''Sample conductance under uncertainty and degradation.'''
        nominal = self.conductance_w_k()
        degraded = nominal * ((1 - self.degradation_rate_per_year) ** elapsed_years)
        return max(0, rng.normal(degraded, degraded * self.conductance_uncertainty))

    def failure_probability(self, elapsed_years: float) -> float:
        '''Weibull failure model. Shape=3, scale=design_life*1.5.'''
        scale = 15 * 1.5
        shape = 3
        return 1 - np.exp(-(elapsed_years / scale) ** shape)

    def summary(self) -> dict:
        return {
            'length_m': self.length_m,
            'outer_diameter_mm': self.outer_diameter_m * 1000,
            'working_fluid': self.working_fluid,
            'operating_temp_k': self.operating_temp_k,
            'max_heat_transport_kw': round(self.max_heat_transport_w() / 1000, 2),
            'thermal_conductance_w_k': round(self.conductance_w_k(), 1),
            'failure_prob_15yr': round(self.failure_probability(15), 4),
        }


@dataclass
class HeatPipeNetwork:
    '''
    Network of parallel heat pipes from reactor to power conversion.
    Models redundancy, partial failure, and total conductance.
    '''

    pipes: list = field(default_factory=list)
    redundancy_factor: float = 1.25  # 25% more pipes than needed

    @classmethod
    def from_thermal_load(cls, thermal_load_kwt: float,
                          working_fluid: str = 'sodium',
                          operating_temp_k: float = 900.0) -> 'HeatPipeNetwork':
        '''Design a heat pipe network for a given thermal load.'''
        pipe = HeatPipe(working_fluid=working_fluid,
                        operating_temp_k=operating_temp_k)
        capacity_per_pipe = pipe.max_heat_transport_w()
        n_pipes_needed = np.ceil(
            (thermal_load_kwt * 1000 * 1.25) / capacity_per_pipe
        )
        pipes = [HeatPipe(working_fluid=working_fluid,
                          operating_temp_k=operating_temp_k)
                 for _ in range(int(n_pipes_needed))]
        return cls(pipes=pipes)

    def total_conductance_w_k(self) -> float:
        return sum(p.conductance_w_k() for p in self.pipes)

    def sample_total_conductance(self, rng: np.random.Generator,
                                  elapsed_years: float = 0.0) -> float:
        conductances = []
        for pipe in self.pipes:
            if rng.random() > pipe.failure_probability(elapsed_years):
                conductances.append(
                    pipe.sample_conductance(rng, elapsed_years)
                )
        return sum(conductances) if conductances else 0.0

    def temperature_drop_k(self, thermal_load_kwt: float) -> float:
        return (thermal_load_kwt * 1000) / self.total_conductance_w_k()

    def summary(self) -> dict:
        return {
            'n_pipes': len(self.pipes),
            'working_fluid': self.pipes[0].working_fluid if self.pipes else None,
            'total_conductance_w_k': round(self.total_conductance_w_k(), 1),
            'max_transport_kwt': round(
                sum(p.max_heat_transport_w() for p in self.pipes) / 1000, 1),
            'single_pipe_failure_15yr': round(
                self.pipes[0].failure_probability(15), 4) if self.pipes else None,
        }
