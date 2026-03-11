# Project Topic

## Objective:

This project aims to detect potential collusion between firms in procurement markets.

## Data:

The analysis uses synthetic auction data simulating multiple firms across repeated
auctions.

## Method:

A network-based approach is implemented, where firms are represented as nodes and
co-bidding behavior as weighted edges, and collusion likelihood is quantified using
metrics such as network coherence and exclusivity, complemented by visualizations of
suspicious firm interactions.

## Project Structure:

- `src/` Contains the code and the task files that define the individual steps of the
  workflow.

- `bld/` Contains all generated outputs, including simulated datasets and the final
  plots. This ensures that results are reproducible and automatically regenerated when
  tasks are rerun.

- `pyproject.toml` Defines the reproducile environment with all required dependencies.

- `config.py` Stores parameters and settings that are used across multiple tasks to
  avoid duplication and make project easier to maintain.

- `README.md` Documentation of the project. Also read "ProjectProcedure.md" for more
  in-depth documentation of procedure.

The workflow is executed using `pytask`, which automatically runs all tasks in the
correct order based on their dependencies.

## Usage

### Prerequisites

You need to have `pixi` installed on your system.

### Running the Project

1. **Install dependencies:**

```console
pixi install
```

2. **Run the full workflow:**

```console
pixi run pytask
```

This executes all tasks and generates intermediate results and final outputs as needed.

### Viewing Results

- The final figures are generated and saved in: bld/figures/
- The datasets used for generating the figures are stored in the bld directory.
