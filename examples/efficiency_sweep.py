'''
Efficiency sweep analysis.

Demonstrates the key Curiefuel thesis:
every 1% of Stirling efficiency = significant mass savings.
'''

import numpy as np
from fsp_thermal.radiator import Radiator
from fsp_thermal.stirling import StirlingConverter

print('=== EFFICIENCY vs SYSTEM MASS ===')
print(f'{"Efficiency":>12} {"Radiator Area":>14} {"Radiator Mass":>14} {"Total Mass":>12} {"F9 Fit":>8}')
print('-' * 65)

radiator = Radiator(rejection_temp_k=400)

for eff in np.arange(0.15, 0.36, 0.01):
    thermal = 40 / eff
    waste = thermal - 40
    area = radiator.area_required_m2(waste)
    rad_mass = radiator.mass_kg(waste)
    fuel = thermal * 15 * 0.08
    total = fuel + fuel*8 + 40*6 + rad_mass + 25 + 200
    fits = 'YES' if total <= 3500 else 'NO'
    print(f'{eff:>11.0%} {area:>13.1f} m² {rad_mass:>12.1f} kg {total:>10.1f} kg {fits:>8}')
