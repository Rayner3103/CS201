# CS201 Project — Text Search

Quick guide to pull this repository, create a Python virtual environment, install dependencies, and run the experiments.

## Repository files of interest
- [experiment.py](experiment.py) — main experiment runner (contains `Array_BKTree` and `Linked_BKTree`).
- [BKTree_array.py](BKTree_array.py) — array-based BK-Tree implementation (`Array_BKTree`).
- [BKTree_link.py](BKTree_link.py) — linked BK-Tree implementation (`Linked_BKTree`).
- [dataLoader.py](dataLoader.py) — CSV parsing / dataset helpers.
- [requirements.txt](requirements.txt) — Python dependencies.
- datasets/ — sample CSVs used by the experiments (e.g. [datasets/airline.csv](datasets/airline.csv)).

## Prerequisites
- Git installed
- Python 3.8+ installed (https://www.python.org/downloads/)

## Clone or update the repo
```bash
# Clone (first time)
git clone <repository-url>
cd CS201

# Or, if you already have it
git pull origin main
```

## Create and activate a virtual environment
Windows (PowerShell)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows (cmd)
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Files referenced: [`requirements.txt`](requirements.txt)

## Run the experiments
Ensure you are in the repository root (where `experiment.py` is).

```bash
# Run the main experiment script
python experiment.py
```

Files referenced: [`experiment.py`](experiment.py), [`dataLoader.py`](dataLoader.py), [datasets/airline.csv](datasets/airline.csv)

## Notes
- The experiment uses the CSV datasets in the `datasets/` directory. Confirm the files (e.g. [datasets/airline.csv](datasets/airline.csv)) are present.
- To inspect BK-Tree implementations:
  - [`Array_BKTree`](BKTree_array.py) in [BKTree_array.py](BKTree_array.py)
  - [`Linked_BKTree`](experiment.py) in [experiment.py](experiment.py)

If anything fails, check Python version, virtual environment activation, and that dependencies listed in [`requirements.txt`](requirements.txt) installed successfully.

Should you require assistance, you may contact the repository owner or reach me at raynersimzhiheng@gmail.com