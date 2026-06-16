'''
Radiator dust degradation analysis.

Shows how lunar dust accumulation degrades radiator performance
over the 15-year mission lifetime.
'''

import numpy as np
from fsp_thermal.radiator import Radiator

print('=== RADIATOR DUST DEGRADATION ANALYSIS ===')
print('Lunar environment, 15-year mission\n')

radiator = Radiator(
    rejection_temp_k=400,
    emissivity=0.90,
    areal_mass_kg_m2=3.0,
    environment='lunar',
    dust_degradation_rate_per_year=0.008,
)

years = np.array([0, 1, 3, 5, 7, 10, 12, 15])
waste_heat_kwt = 100.0  # Example system

print(f'{"Year":>5} {"Emissivity":>11} {"Degradation":>12} {"Area Req":>10} {"Mass":>10}')
print('-' * 60)

for year in years:
    eff_emissivity = radiator.effective_emissivity(year)
    degradation_pct = (1 - eff_emissivity / radiator.emissivity) * 100

    # Create a temporary radiator with degraded emissivity to calculate area
    degraded_radiator = Radiator(
        rejection_temp_k=radiator.rejection_temp_k,
        emissivity=eff_emissivity,
        areal_mass_kg_m2=radiator.areal_mass_kg_m2,
    )
    area = degraded_radiator.area_required_m2(waste_heat_kwt)
    mass = degraded_radiator.mass_kg(waste_heat_kwt)

    print(f'{year:>5} {eff_emissivity:>11.3f} {degradation_pct:>10.1f}% {area:>9.1f} m² {mass:>9.1f} kg')

print('\n=== KEY INSIGHT ===')
bol_area = radiator.area_required_m2(waste_heat_kwt)
eol_emissivity = radiator.effective_emissivity(15)
eol_radiator = Radiator(rejection_temp_k=400, emissivity=eol_emissivity)
eol_area = eol_radiator.area_required_m2(waste_heat_kwt)
area_margin = (eol_area - bol_area) / bol_area * 100

print(f'Beginning-of-life area: {bol_area:.1f} m²')
print(f'End-of-life area:       {eol_area:.1f} m²')
print(f'Required margin:        {area_margin:.1f}%')
print('\nRadiators must be oversized by ~13% to maintain performance through dust accumulation.')
