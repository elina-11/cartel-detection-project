# Replication of a Network-Based Cartel Detection Model

## Objective:

This project replicates the autonomous-agent simulation model from “A Network Approach
to Cartel Detection in Public Auction Markets” (Wachs & Kertész, 2019). The goal is to
study how patterns of interactions between firms in procurement auctions can facilitate
collusion.

## Data:

The analysis uses synthetic auction data generated from a simulation model in which
firms and issuers repeatedly interact in procurement auctions. The simulated market
produces co-bidding networks that can be analyzed to detect groups of firms with
structural properties associated with collusive behavior.

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

- `README.md` Documentation of the project.

```text
src/
└── final_project/
    ├── analysis/
    │   ├── auction_decisions.py              #If collusion is successful, based on firms' actions
    │   ├── auction_framework.py              #Functions for auction and simulation
    │   ├── co_bidding_network.py             #Constructs weighted co-bidding network between firms
    │   ├── contract_generation.py            #Issues contracts randomly in the unit square
    │   ├── create_firms_and_issuers.py       #Places firms and issuers in a unit square
    │   ├── decision_metrics.py               #Memory and familiarity of firms
    │   ├── firm_decision.py                  #Firms decide to collude or compete
    │   ├── firm_participation.py             #Firms decide to participate in auction or not
    │   ├── group_collusion_rate_helpers.py   #Helper function to calculate collusion rates
    │   ├── group_collusion_rate.py           #Calculates collusion rate
    │   ├── group_detection_helpers.py        #Helper functions to detect groups
    │   ├── group_detection.py                #Detects groups
    │   ├── group_features_helpers.py         #Functions to calculate coherence and exclusivity
    │   ├── group_features.py                 #Calculates coherence and exclusivity
    │   ├── interaction_updates.py            #Updates memory and count
    │   ├── task_auction_framework.py         #Runs auctions and produces simulation_state.pickle
    │   ├── task_co_bidding_network.py        #Creates co_bidding_network.pickle
    │   ├── task_collect_figure_data.py       #Creates heamap_data.pickle
    │   ├── task_create_firms_and_issuers.py  #Creates firms.pickle and issuers.pickle
    │   ├── task_group_detection.py           #Creates detected_groups.pickle
    │   └── task_group_features.py            #Creates group_features.pickle
    │
    └── final/
        ├── heatmap_helpers.py                #Bins group features and computes heatmap statistics
        ├── heatmap.py                        #Generates figures for group distribution, collusion
        └── task_heatmap.py                   #Creates figure_a.png and figure_b.png

tests/
└── analysis/
    ├── test_auction_decisions.py
    ├── test_auction_framework.py
    ├── test_co_bidding_network.py
    ├── test_contract_generation.py
    ├── test_create_firms_and_issuers.py
    ├── test_decision_metrics.py
    ├── test_firm_decision.py
    ├── test_firm_participation.py
    ├── test_group_collusion_rate_helpers.py
    ├── test_group_collusion_rate.py
    ├── test_group_detection_helpers.py
    ├── test_group_detection.py
    ├── test_group_features_helpers.py
    ├── test_group_features.py
    └── test_interaction_updates.py
```

The workflow is executed using `pytask`, which automatically runs all tasks in the
correct order based on their dependencies. To keep run time low, ~4 minutes, 
the number of simulations is kept to 100, though the paper used 5,000 simulations. 

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
