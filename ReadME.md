# CS201 Project — Text Search

Quick guide to pull this repository, create a Python virtual environment, install dependencies, and run the experiments.

## Directory Structure
```
CS201
├── datasets
│   └── airline.csv
│   └── airport.csv
│   └── lounge.csv
│   └── seat.csv
├── data_structures
│   ├── Array_BKTree.py
│   └── Linked_BKTree.py
├── experiment.py
├── dataLoader.py
├── utils.py
├── requirements.txt
└── README.md
```

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

Files referenced: [`experiment.py`](experiment.py), [`utils.py`](utils.py), [datasets/airline.csv](datasets/airline.csv)

## Notes
- The experiment uses the CSV datasets in the `datasets/` directory. Confirm the files (e.g. [datasets/airline.csv](datasets/airline.csv)) are present.
- To inspect BK-Tree implementations:
  - `Array_BKTree` in [data_structures/Array_BKTree.py](data_structures/Array_BKTree.py)
  - `Linked_BKTree` in [data_structures/Linked_BKTree.py](data_structures/Linked_BKTree.py)

If anything fails, check Python version, virtual environment activation, and that dependencies listed in [`requirements.txt`](requirements.txt) installed successfully.

Should you require assistance, you may contact the repository owner or reach me at raynersimzhiheng@gmail.com