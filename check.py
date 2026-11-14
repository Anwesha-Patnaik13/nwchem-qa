
import pandas as pd
from parse import parse_output
from geometry import bond_check

REFERENCE = {
    "water": -76.4087,
    "methane": -40.5183,
    "ammonia": -56.5479,
}
TOLERANCE = 0.001
TASKS = ("energy", "optimize", "freq")


def check(name, task, out_file):
    r = parse_output(out_file)
    checks = {}
    checks["finished"] = r["finished"]
    checks["scf_converged"] = r["scf_converged"]
    if r["opt_converged"] is not None:
        checks["opt_converged"] = r["opt_converged"]
    if r["no_imaginary"] is not None:
        checks["no_imaginary"] = r["no_imaginary"]
    if task == "optimize":
        mean_bond, bond_ok = bond_check(name, out_file)
        r["bond"] = mean_bond
        checks["bond_ok"] = bool(bond_ok)
    if r["energy"] is not None and name in REFERENCE:
        diff = abs(r["energy"] - REFERENCE[name])
        checks["energy_ok"] = diff < TOLERANCE
    else:
        checks["energy_ok"] = False
    return r, checks


def check_all():
    rows = []
    for name in REFERENCE:
        for task in TASKS:
            r, checks = check(name, task, f"runs/{name}_{task}.out")
            rows.append({
                "molecule": name,
                "task": task,
                "energy": r["energy"],
                "bond_A": r.get("bond"),
                **checks,
                "overall": "PASS" if all(checks.values()) else "FAIL",
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(check_all().to_string(index=False))
