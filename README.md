# Eagle Delivery - Project 1

Ahmed Nowayti - COSC 461/561

## Introduction

A robot delivers a package between buildings on a grid map of the EMU campus.
In Part A it finds the route with A* search, in Part B it learns the route with Q-learning,
and in Part C I made my own map (`maps/my_campus.txt`) and tested different epsilon values.
The report is in `report.pdf`.

## How to run

Use Python 3.9 or newer (on Windows, use `py` instead of `python3`).

```
python3 -m unittest discover -v
python3 run_project.py search --algorithm astar --start S --goal W
python3 run_project.py train --start S --goal W --output results/baseline_SW
python3 run_project.py train --map maps/my_campus.txt --epsilon 0.05 --output results/custom_e005
python3 summarize_results.py results/baseline_SW
```

Change `--start`, `--goal`, `--map` and `--epsilon` for the other runs.
Use a new `--output` folder each time.

## Experiment settings

- 2000 training episodes and 100 evaluation episodes per seed
- Seeds 0, 1, 2
- alpha = 0.3, gamma = 0.95, slip = 0, max 200 steps
- Part B: epsilon = 0.2, tasks S->W, L->D, H->P on `emu_campus.txt`
- Part C: epsilon = 0.05, 0.2, 0.5, task S->W on `my_campus.txt`
