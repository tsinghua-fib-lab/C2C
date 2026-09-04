# Analysis code

This directory contains the figure notebooks and analysis modules accompanying
the processed-data release.

## Included modules

- `Figure1.ipynb` through `Figure4.ipynb` reproduce the corresponding main
  figure panels from the data in `../data/`.
- `average_speed_model.py` implements the average-speed CO2 emission-factor
  equations and their parameter uncertainty.
- `powerlaw_analysis.py` fits and compares power-law, truncated power-law,
  lognormal, and exponential distributions and produces a CCDF plot.
- `gwr_mgwr_analysis.py` standardizes a spatial table and fits GWR
  and, optionally, MGWR models.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
pip install jupyterlab networkx scipy tqdm
jupyter lab
```

Run these commands from the repository root so that the notebooks can resolve
paths under `data/`.

## Usage

Average-speed model:

```bash
python code/average_speed_model.py \
  --vehicle sedan \
  --energy fuel \
  --speed-kmh 40
```

Heavy-tail analysis:

```bash
python code/powerlaw_analysis.py INPUT.csv \
  --column emission \
  --output results/powerlaw
```

`INPUT.csv` must contain at least ten finite positive observations in the
selected column.

Spatial regression:

```bash
python code/gwr_mgwr_analysis.py GRID.csv \
  --response co2 \
  --predictors population,night_light,bus_stops \
  --output results/gwr \
  --fit-mgwr
```

`GRID.csv` must contain `x`, `y`, the response, and all requested predictor
columns. Coordinates must be projected planar coordinates in consistent
distance units.
