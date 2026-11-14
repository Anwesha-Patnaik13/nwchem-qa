import subprocess
from pathlib import Path

RUNS = Path("runs")

MOLECULES = {
    "water": """O  0.000  0.000  0.117
H  0.000  0.757 -0.469
H  0.000 -0.757 -0.469""",
    "methane": """C  0.000  0.000  0.000
H  0.629  0.629  0.629
H -0.629 -0.629  0.629
H -0.629  0.629 -0.629
H  0.629 -0.629 -0.629""",
    "ammonia": """N  0.000  0.000  0.116
H  0.000  0.939 -0.271
H  0.813 -0.470 -0.271
H -0.813 -0.470 -0.271""",
}


def make_input(name, geometry, task="energy"):
    return f"""start {name}_{task}
title "{name} {task}"
geometry units angstrom
{geometry}
end
basis
  * library 6-31G*
end
dft
  xc b3lyp
end
task dft {task}
"""


def run_nwchem(name, task="energy"):
    RUNS.mkdir(exist_ok=True)
    label = f"{name}_{task}"
    nw_file = RUNS / f"{label}.nw"
    out_file = RUNS / f"{label}.out"

    nw_file.write_text(make_input(name, MOLECULES[name], task))

    with open(out_file, "w") as f:
        subprocess.run(
            ["mpirun", "--oversubscribe", "-np", "2", "nwchem", nw_file.name],
            stdout=f,
            stderr=subprocess.DEVNULL,
            cwd=RUNS,
        )
    return out_file


def run_all(tasks=("energy", "optimize", "freq")):
    for name in MOLECULES:
        for task in tasks:
            print("Running", name, task, "...")
            run_nwchem(name, task)


if __name__ == "__main__":
    run_all()
    print("All done.")
