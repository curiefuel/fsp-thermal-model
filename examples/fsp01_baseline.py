'''
FSP-01 Baseline System Analysis
Curiefuel fsp-thermal-model example

40 kWe system for lunar south pole base.
Validates Falcon 9 rideshare compatibility.
'''

from fsp_thermal.system import FSPThermalSystem

print('=== FSP-01 BASELINE ANALYSIS ===')
system = FSPThermalSystem(
    target_electric_kwe=40,
    reactor_temp_k=900,
    cold_side_temp_k=400,
    working_fluid='sodium',
    environment='lunar',
    design_life_years=15,
)

system.summary()

print('\n=== UNCERTAINTY ANALYSIS (Year 0) ===')
bol = system.run_uncertainty_analysis(n_samples=10000, elapsed_years=0)
for k, v in bol.items():
    print(f'  {k}: {v}')

print('\n=== UNCERTAINTY ANALYSIS (Year 10) ===')
eol = system.run_uncertainty_analysis(n_samples=10000, elapsed_years=10)
for k, v in eol.items():
    print(f'  {k}: {v}')

print('\n=== HEAT PIPE NETWORK ===')
for k, v in system.heat_pipes.summary().items():
    print(f'  {k}: {v}')

print('\n=== STIRLING ARRAY ===')
for k, v in system.stirling.summary().items():
    print(f'  {k}: {v}')

print('\n=== RADIATOR ===')
for k, v in system.radiator.summary(system.waste_heat_kwt).items():
    print(f'  {k}: {v}')
