'''Unit tests for heat pipe module.'''

import numpy as np
from fsp_thermal.heat_pipes import HeatPipe, HeatPipeNetwork


def test_heat_pipe_basic():
    pipe = HeatPipe(working_fluid='sodium', operating_temp_k=900)
    assert pipe.max_heat_transport_w() > 0
    assert pipe.conductance_w_k() > 0
    assert 0 <= pipe.failure_probability(15) <= 1


def test_heat_pipe_network():
    network = HeatPipeNetwork.from_thermal_load(
        thermal_load_kwt=100,
        working_fluid='sodium'
    )
    assert len(network.pipes) > 0
    assert network.total_conductance_w_k() > 0


def test_capillary_limit():
    pipe = HeatPipe(working_fluid='sodium')
    cap_limit = pipe.capillary_limit_w()
    assert cap_limit > 1000  # Should be > 1 kW


def test_vapor_pressure_limit():
    pipe = HeatPipe(working_fluid='sodium')
    vapor_limit = pipe.vapor_pressure_limit_w()
    assert vapor_limit > 1000


def test_sample_conductance():
    rng = np.random.default_rng(42)
    pipe = HeatPipe(working_fluid='sodium')
    conductance = pipe.sample_conductance(rng, elapsed_years=5)
    assert conductance > 0


if __name__ == '__main__':
    test_heat_pipe_basic()
    test_heat_pipe_network()
    test_capillary_limit()
    test_vapor_pressure_limit()
    test_sample_conductance()
    print('All heat pipe tests passed.')
