# Eagle Delivery: Project 1 (COSC 461/561)

This project simulates a delivery robot on a grid version of the EMU campus.
The robot carries one package from one building entrance to another.

- **Part A:** plan the route with search (BFS is given, I added A* with the Manhattan heuristic).
- **Part B:** learn the route from experience with tabular Q-learning and epsilon-greedy exploration.
- **Part C:** my own map (`maps/my_campus.txt`) and an experiment on the exploration rate epsilon.

## Requirements

Python 3.9+. `matplotlib` is only needed for `make_plots.py`.

## Files

| File | What it is |
|---|---|
| `agents.py` | BFS (given), plus my `manhattan`, `astar`, `epsilon_greedy`, `q_learning_update` |
| `campus.py` | Map loading, movement and rewards (given) |
| `run_project.py` | Show maps, run search, train and evaluate (given) |
| `summarize_results.py` | Summary stats and `learning_curve.csv` (given) |
| `make_plots.py` | Plots training curves from result folders (added by me) |
| `maps/` | `emu_campus.txt`, `emu_detour.txt`, `my_campus.txt` |
| `results/` | All raw training/evaluation CSVs, summaries, and search outputs |
| `plots/` | Figures used in the report |
| `report.pdf` | Project report |

## Run commands

Tests:

```bash
python3 -m unittest discover -v
```

Part A (search). Repeat for `--start L --goal D` and `--start H --goal P`, and for both maps:

```bash
python3 run_project.py show
python3 run_project.py search --algorithm bfs --start S --goal W
python3 run_project.py search --algorithm astar --start S --goal W
python3 run_project.py search --algorithm astar --map maps/emu_detour.txt --start L --goal D
```

Part B (Q-learning baseline):

```bash
python3 run_project.py train --start S --goal W --output results/baseline_SW
python3 run_project.py train --start L --goal D --output results/baseline_LD
python3 run_project.py train --start H --goal P --output results/baseline_HP
python3 summarize_results.py results/baseline_SW
python3 summarize_results.py results/baseline_LD
python3 summarize_results.py results/baseline_HP
python3 make_plots.py results/baseline_SW results/baseline_LD results/baseline_HP --labels "S->W" "L->D" "H->P" --field steps --last 600 --output plots/baseline_steps.png
```

Part C (custom map and epsilon experiment):

```bash
python3 run_project.py search --map maps/my_campus.txt --algorithm bfs
python3 run_project.py search --map maps/my_campus.txt --algorithm astar
python3 run_project.py train --map maps/my_campus.txt --epsilon 0.05 --output results/custom_e005
python3 run_project.py train --map maps/my_campus.txt --epsilon 0.2 --output results/custom_e020
python3 run_project.py train --map maps/my_campus.txt --epsilon 0.5 --output results/custom_e050
python3 summarize_results.py results/custom_e005
python3 summarize_results.py results/custom_e020
python3 summarize_results.py results/custom_e050
python3 make_plots.py results/custom_e005 results/custom_e020 results/custom_e050 --labels "epsilon=0.05" "epsilon=0.2" "epsilon=0.5" --field steps --last 600 --output plots/custom_epsilon_steps.png
```

Note: `run_project.py train` refuses to write into a folder that already has CSVs,
so use a new `--output` folder for any rerun.

## Experiment settings

| Setting | Part B baseline | Part C experiment |
|---|---|---|
| Map | `emu_campus.txt` | `my_campus.txt` |
| Tasks | S->W, L->D, H->P | S->W |
| Training episodes | 2000 per seed | 2000 per seed |
| Evaluation episodes | 100 per seed (epsilon = 0, frozen Q) | same |
| Seeds | 0, 1, 2 | 0, 1, 2 for each setting |
| Max actions per episode | 200 | 200 |
| alpha | 0.3 | 0.3 |
| gamma | 0.95 | 0.95 |
| epsilon | 0.2 | **0.05, 0.2, 0.5** (the factor changed) |
| slip | 0.0 | 0.0 |

## Main results

- A* and BFS found routes of the same length on all six tasks; A* expanded fewer or equal nodes.
- Q-learning reached 100% evaluation success with the optimal route length on all baseline tasks and seeds.
- On my map, every epsilon setting gave the same final greedy route (22 steps), but larger epsilon
  made training episodes longer.
