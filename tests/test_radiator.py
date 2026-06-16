'''Unit tests for radiator module.'''

import numpy as np
from fsp_thermal.radiator import Radiator


def test_radiator_basic():
    radiator = Radiator(rejection_temp_k=400)
    waste_heat = 100  # kWt
    area = radiator.area_required_m2(waste_heat)
    mass = radiator.mass_kg(waste_heat)
    assert area > 0
    assert mass > 0


def test_heat_rejection_per_m2():
    radiator = Radiator(rejection_temp_k=400, emissivity=0.9)
    heat_flux = radiator.heat_rejection_per_m2_w()
    assert heat_flux > 1000  # Should be ~1-2 kW/m² at 400K


def test_effective_emissivity():
    radiator = Radiator(emissivity=0.9)
    eff_emissivity = radiator.effective_emissivity(elapsed_years=10)
    assert eff_emissivity < 0.9  # Should degrade
    assert eff_emissivity > 0.7  # But not below floor


def test_sample_rejection_capacity():
    rng = np.random.default_rng(42)
    radiator = Radiator(rejection_temp_k=400)
    capacity = radiator.sample_rejection_capacity_w_m2(rng, elapsed_years=5)
    assert capacity > 0


def test_mass_savings_per_efficiency_point():
    radiator = Radiator(rejection_temp_k=400)
    savings = radiator.mass_savings_per_efficiency_point(40, base_efficiency=0.25)
    assert savings > 0  # Should save mass with higher efficiency


if __name__ == '__main__':
    test_radiator_basic()
    test_heat_rejection_per_m2()
    test_effective_emissivity()
    test_sample_rejection_capacity()
    test_mass_savings_per_efficiency_point()
    print('All radiator tests passed.')
