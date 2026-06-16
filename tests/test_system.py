'''Unit tests for integrated system module.'''

from fsp_thermal.system import FSPThermalSystem


def test_system_basic():
    system = FSPThermalSystem(
        target_electric_kwe=40,
        reactor_temp_k=900,
        cold_side_temp_k=400,
    )
    assert system.thermal_input_kwt > 40
    assert system.waste_heat_kwt > 0


def test_total_mass():
    system = FSPThermalSystem(target_electric_kwe=40)
    mass = system.total_mass_kg()
    assert mass['total_kg'] > 0
    assert mass['radiator_kg'] > 0
    assert mass['stirling_kg'] > 0


def test_falcon9_compatible():
    system = FSPThermalSystem(target_electric_kwe=40)
    result = system.falcon9_compatible()
    assert isinstance(result, bool)


def test_uncertainty_analysis():
    system = FSPThermalSystem(target_electric_kwe=40)
    results = system.run_uncertainty_analysis(n_samples=100, elapsed_years=0)
    assert 'mean_kwe' in results
    assert 'reliability' in results
    assert 0 <= results['reliability'] <= 1


if __name__ == '__main__':
    test_system_basic()
    test_total_mass()
    test_falcon9_compatible()
    test_uncertainty_analysis()
    print('All system tests passed.')
