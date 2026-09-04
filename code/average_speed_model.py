"""Average-speed CO2 emission-factor model used in Camera2Carbon.

Input speed is km/h. Returned emission factors are grams CO2 per metre. The
uncertainty value is the absolute difference between two published parameter
sets and was used as a conservative model spread in the original analysis.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


VEHICLES = ("bus", "heavy_truck", "minivan", "sedan", "suv", "light_truck")
ENERGY_TYPES = ("fuel", "electric", "hybrid")


@dataclass(frozen=True)
class Estimate:
    factor_g_per_m: np.ndarray
    uncertainty_g_per_m: np.ndarray


def _paired(speed_kmh, first, second) -> Estimate:
    speed = np.maximum(np.asarray(speed_kmh, dtype=float), 3.0)
    a = first[0] + first[1] / speed
    b = second[0] + second[1] / speed
    return Estimate((a + b) / 2.0, np.abs(a - b))


def _fuel_estimate(vehicle: str, speed_kmh) -> Estimate:
    parameters = {
        "sedan": ((0.134, 3.664), (0.140, 3.874)),
        "suv": ((0.134, 3.664), (0.140, 3.874)),
        "bus": ((0.575, 16.207), (0.521, 16.032)),
        "heavy_truck": ((0.508, 18.460), (0.389, 17.463)),
        "light_truck": ((0.261, 6.017), (0.272, 6.219)),
        "minivan": ((0.162, 4.145), (0.183, 4.058)),
    }
    return _paired(speed_kmh, *parameters[vehicle])


def _electric_estimate(vehicle: str, speed_kmh) -> Estimate:
    shape = np.asarray(speed_kmh, dtype=float)
    factor = 0.676 if vehicle == "bus" else 0.108
    if vehicle not in {"bus", "sedan", "suv"}:
        # The study did not define separate electric factors for these classes.
        return _fuel_estimate(vehicle, speed_kmh)
    return Estimate(np.full_like(shape, factor), np.zeros_like(shape))


def emission_factor(vehicle: str, energy: str, speed_kmh) -> Estimate:
    """Return average-speed emission factor for a public vehicle category."""
    if vehicle not in VEHICLES:
        raise ValueError(f"unknown vehicle class: {vehicle}")
    if energy not in ENERGY_TYPES:
        raise ValueError(f"unknown energy type: {energy}")
    fuel = _fuel_estimate(vehicle, speed_kmh)
    if energy == "fuel":
        return fuel
    electric = _electric_estimate(vehicle, speed_kmh)
    if energy == "electric":
        return electric
    return Estimate(
        (fuel.factor_g_per_m + electric.factor_g_per_m) / 2.0,
        (fuel.uncertainty_g_per_m + electric.uncertainty_g_per_m) / 2.0,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vehicle", required=True, choices=VEHICLES)
    parser.add_argument("--energy", required=True, choices=ENERGY_TYPES)
    parser.add_argument("--speed-kmh", required=True, type=float)
    args = parser.parse_args()
    result = emission_factor(args.vehicle, args.energy, args.speed_kmh)
    print(f"factor_g_per_m={float(result.factor_g_per_m):.8g}")
    print(f"uncertainty_g_per_m={float(result.uncertainty_g_per_m):.8g}")


if __name__ == "__main__":
    main()

