from parse import parse_output
from check import check_all


def test_water_energy_is_correct():
    r = parse_output("runs/water_energy.out")
    assert r["finished"]
    assert abs(r["energy"] - (-76.4087)) < 0.001


def test_water_has_no_imaginary_frequencies():
    r = parse_output("runs/water_freq.out")
    assert r["no_imaginary"] is True
    assert len(r["frequencies"]) == 9


def test_all_calculations_pass_qa():
    df = check_all()
    assert len(df) == 9
    assert (df["overall"] == "PASS").all()
