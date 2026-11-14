import re
from pathlib import Path
import numpy as np

# Approximate experimental X-H bond lengths (Angstrom)
EXPT_BOND = {
    "water": 0.958,
    "methane": 1.087,
    "ammonia": 1.012,
}
BOND_TOLERANCE = 0.03


def last_geometry(out_file):
    """Return the final geometry as a list of (element, np.array([x, y, z]))."""
    lines = Path(out_file).read_text().splitlines()
    starts = [i for i, l in enumerate(lines)
              if "Output coordinates in angstroms" in l]
    if not starts:
        return None
    atoms = []
    for line in lines[starts[-1] + 1:]:
        m = re.match(
            r"\s*\d+\s+([A-Za-z]+)\s+[\d.]+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)",
            line,
        )
        if m:
            xyz = np.array([float(m.group(2)), float(m.group(3)), float(m.group(4))])
            atoms.append((m.group(1), xyz))
        elif atoms:
            break
    return atoms if atoms else None


def xh_bond_lengths(atoms):
    """Distances from the heavy atom (first atom) to every H atom."""
    heavy = atoms[0][1]
    return [float(np.linalg.norm(heavy - xyz))
            for el, xyz in atoms[1:] if el.upper() == "H"]


def bond_check(name, out_file):
    """Return (mean bond length, True/False). None if no geometry or no reference."""
    atoms = last_geometry(out_file)
    if atoms is None or name not in EXPT_BOND:
        return None, None
    bonds = xh_bond_lengths(atoms)
    mean = sum(bonds) / len(bonds)
    return mean, abs(mean - EXPT_BOND[name]) < BOND_TOLERANCE


if __name__ == "__main__":
    for name in EXPT_BOND:
        mean, ok = bond_check(name, f"runs/{name}_optimize.out")
        print(name, "mean X-H bond:", round(mean, 4), "A  within tolerance:", ok)
