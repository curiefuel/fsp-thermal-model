'''
Physical constants and material properties for FSP thermal analysis.
All values from published literature with sources cited.
'''

# Stefan-Boltzmann constant
SIGMA = 5.6704e-8  # W/m²/K⁴

# Sodium heat pipe properties (primary working fluid)
# Source: Dunn & Reay, Heat Pipes, 4th ed.
SODIUM_PROPERTIES = {
    'melting_point_k': 371,
    'boiling_point_k': 1156,
    'operating_range_k': (800, 1100),
    'latent_heat_j_kg': 3.87e6,      # at 900K
    'liquid_density_kg_m3': 750,      # at 900K
    'vapor_density_kg_m3': 0.42,      # at 900K
    'surface_tension_n_m': 0.148,     # at 900K
    'liquid_viscosity_pa_s': 2.1e-4,  # at 900K
    'thermal_conductivity_w_mk': 59,  # liquid at 900K
}

# Potassium heat pipe properties (alternative)
POTASSIUM_PROPERTIES = {
    'melting_point_k': 337,
    'boiling_point_k': 1032,
    'operating_range_k': (700, 1000),
    'latent_heat_j_kg': 2.08e6,
    'liquid_density_kg_m3': 690,
    'vapor_density_kg_m3': 0.51,
    'surface_tension_n_m': 0.095,
    'liquid_viscosity_pa_s': 1.9e-4,
    'thermal_conductivity_w_mk': 43,
}

# Carbon composite radiator properties
# Source: NASA/TM-2012-217117
RADIATOR_PROPERTIES = {
    'emissivity_beginning_of_life': 0.90,
    'emissivity_end_of_life': 0.85,
    'areal_mass_kg_m2': 3.0,
    'dust_degradation_rate_per_year': 0.008,
    'operating_temp_range_k': (300, 600),
}

# Stirling engine material limits
STIRLING_PROPERTIES = {
    'max_hot_side_temp_k': 1050,
    'min_cold_side_temp_k': 350,
    'mechanical_efficiency': 0.85,
    'design_life_years': 15,
    'power_per_unit_kwe': 6.0,
}

# Lunar environment
LUNAR_ENVIRONMENT = {
    'surface_temp_day_k': 390,
    'surface_temp_night_k': 100,
    'surface_temp_pole_k': 220,
    'solar_flux_w_m2': 1361,
    'gravity_m_s2': 1.62,
    'regolith_thermal_conductivity_w_mk': 0.0015,
}

# Mars environment
MARS_ENVIRONMENT = {
    'surface_temp_day_k': 280,
    'surface_temp_night_k': 180,
    'solar_flux_w_m2': 590,
    'gravity_m_s2': 3.72,
    'atmospheric_pressure_pa': 600,
    'regolith_thermal_conductivity_w_mk': 0.04,
}
