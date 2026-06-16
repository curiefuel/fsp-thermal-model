'''Unit tests for Stirling converter module.'''

import numpy as np
from fsp_thermal.stirling import StirlingConverter, StirlingArray


def test_stirling_converter_basic():
    converter = StirlingConverter(hot_side_temp_k=850, cold_side_temp_k=400)
    assert 0 < converter.actual_efficiency() < 1
    assert converter.thermal_input_kwt() > converter.design_power_kwe
    assert converter.waste_heat_kwt() > 0


def test_carnot_efficiency():
    converter = StirlingConverter(hot_side_temp_k=900, cold_side_temp_k=400)
    carnot = converter.carnot_efficiency()
    assert 0.5 < carnot < 0.6  # ~55% for these temps


def test_stirling_array():
    array = StirlingArray.for_power_output(40, hot_side_temp_k=850)
    assert array.n_units > 0
    assert array.total_power_kwe() >= 40


def test_sample_efficiency():
    rng = np.random.default_rng(42)
    converter = StirlingConverter()
    eff = converter.sample_efficiency(rng, elapsed_years=5)
    assert 0 < eff < 1


def test_efficiency_at_temperature():
    converter = StirlingConverter()
    eff = converter.efficiency_at_temperature(900, 400)
    assert 0 < eff < 1


if __name__ == '__main__':
    test_stirling_converter_basic()
    test_carnot_efficiency()
    test_stirling_array()
    test_sample_efficiency()
    test_efficiency_at_temperature()
    print('All Stirling tests passed.')
