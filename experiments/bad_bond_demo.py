import run
from geometry import xh_bond_lengths, BOND_TOLERANCE, EXPT_BOND

# Stretched water: O-H is about 1.9 A instead of 0.96 A
run.MOLECULES["water_bad"] = """O  0.000  0.000  0.117
H  0.000  1.800 -0.469
H  0.000 -1.800 -0.469"""

# Optimize it. A real optimizer would fix the geometry, so we only
# test the CHECK itself by measuring the geometry we typed in.
atoms = []
for line in run.MOLECULES["water_bad"].splitlines():
    el, x, y, z = line.split()
    import numpy as np
    atoms.append((el, np.array([float(x), float(y), float(z)])))

bonds = xh_bond_lengths(atoms)
mean = sum(bonds) / len(bonds)
ok = abs(mean - EXPT_BOND["water"]) < BOND_TOLERANCE

print("Mean O-H bond:", round(mean, 3), "A")
print("Experimental:", EXPT_BOND["water"], "A")
print("bond_ok:", ok)

