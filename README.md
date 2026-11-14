# Automated Quantum Chemistry Calculation and QA Validation

A small Python pipeline that runs NWChem calculations on water, methane
and ammonia, then automatically checks whether each result is trustworthy.

## Workflow

generate input -> run NWChem -> parse output -> QA checks -> CSV report

## Files

- run.py       writes NWChem inputs and runs them (energy, optimize, freq)
- parse.py     reads outputs: energy, convergence, frequencies
- geometry.py  reads the optimized geometry and measures X-H bond lengths
- check.py     runs the QA checks and builds the results table
- report.py    saves the table to reports/results.csv

## QA checks

1. Finished normally (NWChem printed its final timing line)
2. SCF converged
3. Geometry optimization converged
4. No imaginary frequencies (true minimum)
5. Energy within 0.001 Hartree of a reference value
6. X-H bond length within 0.03 A of the experimental value

## Method

DFT, B3LYP functional, 6-31G* basis set.

## How to run

    source .venv/bin/activate
    python run.py        # runs 9 calculations
    python report.py     # checks them and writes reports/results.csv

## Limitations

- Energy references come from our own runs, so that check only detects
  changes, not chemical errors. Bond lengths are compared to experiment.
- Only three small molecules and one method are covered.
- No spin contamination or open-shell checks.

## Ideas for the future

- Add more molecules and basis sets
- Compare vibrational frequencies to experiment
- Add regression tests with pytest
- Generate geometries from SMILES using RDKit
