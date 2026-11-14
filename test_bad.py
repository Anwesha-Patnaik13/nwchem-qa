import run
from check import check

# A distorted water molecule: the H atoms are placed far from the O atom
run.MOLECULES["bad_water"] = """O  0.000  0.000  0.117
H  0.000  1.800 -0.469
H  0.000 -1.800 -0.469"""

out = run.run_nwchem("bad_water")
r, checks = check("water", out)

print("Energy:", r["energy"])
for label, passed in checks.items():
    print(("PASS" if passed else "FAIL"), "-", label)
print("OVERALL:", "PASS" if all(checks.values()) else "FAIL")
