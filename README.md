# Spacetime diagrams - simultaneity, time dilation, causal structure

The file figures.tex contains numerous spacetime diagrams used in an accompanying paper "Diagrammatic approaches to teaching special and general relativity".

The diagrams can be used to teach relativity of simultaneity, time dilation and visualizing curvature through the causal structure of the Schwarzschild spacetime.

The python script generates **radial free-fall trajectories** (“worldlines”) and **lightcone anchor points** and writes them to CSV files. The CSV outputs are intended to be plotted with LaTeX using TikZ/PGFPlots (see `figures.tex`).

The goal is reproducible spacetime diagrams: the curves and cone positions are computed numerically (not sketched) and then rendered in LaTeX. Parameters of the diagrams, worldlines and the light cones can be adjusted.

---

## What the Python script does

The Python script integrates an ODE for radial motion (starting from rest at several initial radii) and produces two datasets:

### Set A: “planet diagrams” (smaller Schwarzschild radius)
- `data_pg/traj_1.csv ... data_pg/traj_N.csv`
- `data_pg/cone_points.csv`

### Set B: black hole (larger Schwarzschild radius; includes inside/outside horizon)
- `data_pg/traj_bh_1.csv ... data_pg/traj_bh_N_bh.csv`
- `data_pg/cone_points_bh.csv`

Both sets are generated in a single run.

---

## Requirements

### Python
- Python 3.x
- `numpy`
- `scipy`

## LaTeX

To compile figures.tex you need a LaTeX distribution with:
- tikz
- pgfplots
- pgfplotstable
- csvsimple

## Usage

1. (Optional) Adjust parameters in `worldlines.py`
   - Schwarzschild radii (`rS`, `rS_bh`)
   - Number of trajectories (`N`, `N_bh`)
   - Integration ranges (`tmax`, etc.)
   - Cone placement (`cone_times`)

2. If you changed `rS` values, ensure the same values are set in `figures.tex`
   (e.g. `\pgfmathsetmacro{\rs}{...}`).

3. Generate the CSV data:
   ```bash
   python worldlines.py

4. Compile the figures
latexmk -pdf figures.tex
