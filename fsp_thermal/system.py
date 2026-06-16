'''
Integrated FSP thermal system model.

Combines heat pipe network, Stirling conversion, and radiator
into a complete system with mass budget and uncertainty analysis.
'''

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from .heat_pipes import HeatPipeNetwork, HeatPipe
from .stirling import StirlingArray, StirlingConverter
from .radiator import Radiator


@dataclass
class FSPThermalSystem:
    '''
    Complete fission surface power thermal system.

    Reactor → Heat Pipes → Stirling Converters → Radiators → Electric Output
    '''

    target_electric_kwe: float = 40.0
    reactor_temp_k: float = 900.0
    cold_side_temp_k: float = 400.0
    working_fluid: str = 'sodium'
    environment: str = 'lunar'
    design_life_years: float = 15.0

    def __post_init__(self):
        self.stirling = StirlingArray.for_power_output(
            self.target_electric_kwe,
            hot_side_temp_k=self.reactor_temp_k,
            cold_side_temp_k=self.cold_side_temp_k,
        )
        self.thermal_input_kwt = self.stirling.total_thermal_input_kwt()
        self.heat_pipes = HeatPipeNetwork.from_thermal_load(
            self.thermal_input_kwt,
            working_fluid=self.working_fluid,
            operating_temp_k=self.reactor_temp_k,
        )
        self.radiator = Radiator(
            rejection_temp_k=self.cold_side_temp_k,
            environment=self.environment,
        )
        self.waste_heat_kwt = self.stirling.unit.waste_heat_kwt() * self.stirling.n_units

    def total_mass_kg(self) -> dict:
        fuel_kg = self.thermal_input_kwt * self.design_life_years * 0.08
        reactor_structure_kg = fuel_kg * 8
        stirling_kg = self.stirling.total_mass_kg()
        radiator_kg = self.radiator.mass_kg(self.waste_heat_kwt)
        heat_pipe_kg = len(self.heat_pipes.pipes) * 2.5
        overhead_kg = 200

        return {
            'fuel_kg': round(fuel_kg, 1),
            'reactor_structure_kg': round(reactor_structure_kg, 1),
            'stirling_kg': round(stirling_kg, 1),
            'radiator_kg': round(radiator_kg, 1),
            'heat_pipe_kg': round(heat_pipe_kg, 1),
            'overhead_kg': overhead_kg,
            'total_kg': round(
                fuel_kg + reactor_structure_kg + stirling_kg +
                radiator_kg + heat_pipe_kg + overhead_kg, 1
            ),
        }

    def falcon9_compatible(self) -> bool:
        return self.total_mass_kg()['total_kg'] <= 3500

    def run_uncertainty_analysis(self, n_samples: int = 10000,
                                  elapsed_years: float = 0.0) -> dict:
        rng = np.random.default_rng(42)
        outputs = []

        for _ in range(n_samples):
            conductance = self.heat_pipes.sample_total_conductance(rng, elapsed_years)
            if conductance == 0:
                outputs.append(0)
                continue
            power = self.stirling.sample_total_output(
                rng, self.thermal_input_kwt, elapsed_years
            )
            outputs.append(power)

        outputs = np.array(outputs)
        return {
            'mean_kwe': round(float(np.mean(outputs)), 2),
            'std_kwe': round(float(np.std(outputs)), 2),
            'p10_kwe': round(float(np.percentile(outputs, 10)), 2),
            'p90_kwe': round(float(np.percentile(outputs, 90)), 2),
            'reliability': round(float(np.mean(outputs >= self.target_electric_kwe * 0.9)), 3),
        }

    def summary(self) -> None:
        mass = self.total_mass_kg()
        print(f'\n=== CURIEFUEL FSP THERMAL SYSTEM ===')
        print(f'Target output:        {self.target_electric_kwe} kWe')
        print(f'Thermal input:        {self.thermal_input_kwt:.1f} kWt')
        print(f'Conversion efficiency:{self.stirling.unit.actual_efficiency():.1%}')
        print(f'Waste heat:           {self.waste_heat_kwt:.1f} kWt')
        print(f'Radiator area:        {self.radiator.area_required_m2(self.waste_heat_kwt):.1f} m²')
        print(f'\nMASS BUDGET')
        for k, v in mass.items():
            print(f'  {k:<25} {v:>8} kg')
        print(f'\nFalcon 9 compatible:  {self.falcon9_compatible()}')

        savings = self.radiator.mass_savings_per_efficiency_point(self.target_electric_kwe)
        print(f'\nKEY INSIGHT')
        print(f'  Mass saved per 1% efficiency gain: {savings:.1f} kg')
