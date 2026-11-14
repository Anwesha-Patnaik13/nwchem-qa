import re
from pathlib import Path


def parse_output(out_file):
    text = Path(out_file).read_text()

    result = {}

    # 1. Did NWChem finish normally?
    result["finished"] = "Total times" in text

    # 2. Final energy (last "Total DFT energy" line)
    energies = re.findall(r"Total DFT energy\s*=\s*(-?\d+\.\d+)", text)
    result["energy"] = float(energies[-1]) if energies else None

    # 3. Did the SCF converge?
    result["scf_converged"] = (
        "Calculation failed to converge" not in text and len(energies) > 0
    )

    # 4. Did the geometry optimization converge?
    #    None means this run was not an optimization.
    if "Optimization converged" in text:
        result["opt_converged"] = True
    elif "Geometry Optimization" in text or "NWChem Geometry Optimization" in text:
        result["opt_converged"] = False
    else:
        result["opt_converged"] = None

    # 5. Frequencies: use only the LAST projected table
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines)
              if "Normal Eigenvalue" in l and "Projected" in l]
    freqs = []
    if starts:
        for line in lines[starts[-1] + 1:]:
            m = re.match(r"\s*\d+\s+(-?\d+\.\d+)\s*\|\|", line)
            if m:
                freqs.append(float(m.group(1)))
            elif freqs and not line.strip():
                break
    result["frequencies"] = freqs if freqs else None

    # 6. Any imaginary frequency? (more negative than -20 cm-1)
    #    None means this run had no frequency data.
    if freqs:
        result["no_imaginary"] = min(freqs) > -20.0
    else:
        result["no_imaginary"] = None

    return result


if __name__ == "__main__":
    print(parse_output("runs/water.out"))
