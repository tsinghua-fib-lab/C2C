# Camera2Carbon data and analysis code

This repository contains processed data and analysis code accompanying the
Camera2Carbon study.

## Repository structure

```text
.
├── README.md
├── LICENSE-CODE
├── LICENSE-DATA
├── code/
│   ├── README.md
│   ├── requirements.txt
│   ├── Figure1.ipynb
│   ├── Figure2.ipynb
│   ├── Figure3.ipynb
│   ├── Figure4.ipynb
│   ├── average_speed_model.py
│   ├── powerlaw_analysis.py
│   └── gwr_mgwr_analysis.py
└── data/
    ├── *.csv
    ├── *.pkl
    └── simulation_results/*.txt
```

## Contents

The release contains the processed numerical results and analysis workflows
used for:

1. reproducing Figures 1--4;
2. calculating average-speed CO2 emission factors;
3. fitting heavy-tail distributions to emission patterns; and
4. fitting geographically weighted regression (GWR/MGWR) models for spatial
   associations with urban covariates.

The upstream cross-camera association and trajectory-recovery method is
available in
[tsinghua-fib-lab/Cam-Traj-Rec](https://github.com/tsinghua-fib-lab/Cam-Traj-Rec).

## Data files

| Path | Description | Related analysis |
| --- | --- | --- |
| `data/jn_spatial.pkl` | Processed spatial emission and road-network quantities | Spatial patterns |
| `data/sz_spatial.pkl` | Processed spatial emission and road-network quantities for Shenzhen | Spatial patterns |
| `data/gwr_effects.pkl` | Selected geographically weighted regression effects | GWR summaries |
| `data/bytime_byvehicle_jn_w.csv` | Working-day aggregates by time window and vehicle class | Temporal and fleet composition |
| `data/bytime_byvehicle_jn_nw.csv` | Non-working-day aggregates by time window and vehicle class | Temporal and fleet composition |
| `data/grid_congestion_jn1.pkl` | Gridded congestion and emission quantities for Jinan dataset 1 | Congestion response |
| `data/grid_congestion_jn2.pkl` | Gridded congestion and emission quantities for Jinan dataset 2 | Congestion response |
| `data/jn_road_congestion_speed.pkl` | Road-level congestion, speed, and emission summaries | Congestion response |
| `data/bus_vs_private.pkl` | Processed public-transit/private-vehicle comparison | Per-passenger comparison |
| `data/reduction_spatial.pkl` | Spatial outputs for selected counterfactual scenarios | Scenario analysis |
| `data/depeak.pkl` | Original and temporally redistributed emission profiles | Departure-time scenario |
| `data/simulation_results/*.txt` | Scalar total-emission outputs from production simulation runs | Scenario-response analysis |

The CSV columns are `start_window`, `VehicleType`, `Emission`, `Uncertainty`,
`RoadLength`, and `TravelTime`. `VehicleType` is a categorical class rather than
a persistent vehicle identifier.

The pickle files contain Python objects used by the figure notebooks and require
compatible versions of Python, NumPy, pandas, and NetworkX.

## Code

See [`code/README.md`](code/README.md) for installation and usage. The
Figure notebooks reproduce the main figure panels from the included processed
data. The standalone scripts provide the average-speed, heavy-tail, and
GWR/MGWR analysis workflows.

## Simulation outputs

Files under `data/simulation_results/` are outputs of the IM model. Each text file contains one aggregate emission result.

The filename suffix identifies the intervention and its parameter value:

| Suffix | Manuscript scenario | Meaning |
| --- | --- | --- |
| no suffix | Baseline | Original simulation without an intervention |
| `s<rate>` | P1: Global Flow Restriction | All vehicle classes are randomly sampled at the specified retention rate |
| `e<rate>` | P2: Global Electrification Transition | The specified proportion of fuel-powered vehicles is converted to electric vehicles (`electrify_rate`) |
| `c<rate>` | P3: Modal Shift / Driving Reduction | Only private cars (`types=[3,4]`, sedans and SUVs) are randomly sampled at the specified retention rate; other vehicle classes are retained |
| `t<rate>` | P4: Heavy Asset Restriction | Only heavy trucks (`types=[1]`) are randomly sampled at the specified retention rate; other vehicle classes are retained |

For the sampling scenarios (`s`, `c`, and `t`), `rate` is the fraction retained
in the simulator and the restricted/removed fraction is `1 - rate`. For example,
`s09` retains 90% of all vehicles, whereas `c07` retains 70% of private cars.
The compact numeric encoding omits the decimal point: `005`, `01`, `095`, and
`10` denote 0.05, 0.10, 0.95, and 1.00, respectively.

P5 (Temporal Load Balancing / Departure Time Shifts) does not use an `s`, `e`,
`c`, or `t` filename suffix. Its processed original and redistributed temporal
profiles are stored in `data/depeak.pkl`. In this scenario, departure times are
shifted by no more than 30 minutes to reduce peak congestion without removing
travel demand.

## Citation and license

If you use the Camera2Carbon data or analysis code, please cite the accompanying
article:

> Zhang, Y., Yu, F., Li, S., Li, M., Guan, D. & Li, Y. AI-enhanced sensing of
> instantaneous vehicular carbon flux via city-scale camera networks.
> Manuscript accompanying this repository.

```bibtex
@misc{zhang_camera2carbon,
  author = {Zhang, Yunke and Yu, Fudan and Li, Sibo and Li, Meng and Guan, Dabo and Li, Yong},
  title = {AI-enhanced sensing of instantaneous vehicular carbon flux via city-scale camera networks},
  year = {2026},
  note = {Manuscript accompanying the Camera2Carbon data and analysis-code repository},
  url = {https://github.com/zyk21/C2C}
}
```

If you use the upstream trajectory-recovery implementation, please also cite:

> Yu, F., Ao, W., Yan, H., Zhang, G., Wu, W. & Li, Y. Spatio-Temporal Vehicle
> Trajectory Recovery on Road Network Based on Traffic Camera Video Data.
> Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and
> Data Mining, 4413--4421 (2022).
> https://doi.org/10.1145/3534678.3539186

```bibtex
@inproceedings{yu2022spatiotemporal,
  author = {Yu, Fudan and Ao, Wenxuan and Yan, Huan and Zhang, Guozhen and Wu, Wei and Li, Yong},
  title = {Spatio-Temporal Vehicle Trajectory Recovery on Road Network Based on Traffic Camera Video Data},
  year = {2022},
  publisher = {Association for Computing Machinery},
  doi = {10.1145/3534678.3539186},
  booktitle = {Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
  pages = {4413--4421}
}
```

Unless otherwise noted:

- source code under `code/` is licensed under the
  [MIT License](LICENSE-CODE);
- processed datasets and aggregate simulation outputs under `data/` are
  licensed under the
  [Creative Commons Attribution 4.0 International License](LICENSE-DATA);
- third-party software, data, and linked repositories remain subject to their
  original licenses and terms.

Copyright (c) 2026 Camera2Carbon authors.
