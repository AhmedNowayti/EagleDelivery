import argparse
import csv
from pathlib import Path
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_csv(filename):
    with open(filename, newline="") as source:
        return list(csv.DictReader(source))


def block_curve(folder, field, block):
    # average a training field over blocks of episodes, then over seeds
    summaries = read_csv(Path(folder) / "summary.csv")
    runs = [read_csv(Path(folder) / ("training_seed" + row["seed"] + ".csv"))
            for row in summaries]
    episode_ends = []
    means = []
    for start in range(0, len(runs[0]), block):
        end = min(start + block, len(runs[0]))
        seed_means = [statistics.mean(float(r[field]) for r in run[start:end])
                      for run in runs]
        episode_ends.append(end)
        means.append(statistics.mean(seed_means))
    return episode_ends, means


def main():
    parser = argparse.ArgumentParser(description="Plot training curves from result folders")
    parser.add_argument("folders", nargs="+")
    parser.add_argument("--labels", nargs="+")
    parser.add_argument("--field", default="steps", choices=("steps", "return", "success"))
    parser.add_argument("--block", type=int, default=20)
    parser.add_argument("--last", type=int, default=2000)
    parser.add_argument("--title", default="Training curve")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    labels = args.labels or args.folders

    plt.figure(figsize=(6, 3.5))
    for folder, label in zip(args.folders, labels):
        episode_ends, means = block_curve(folder, args.field, args.block)
        points = [(e, m) for e, m in zip(episode_ends, means) if e <= args.last]
        plt.plot([p[0] for p in points], [p[1] for p in points], label=label)
    plt.xlabel("Training episode")
    plt.ylabel("Mean " + args.field + " per episode (block of "
               + str(args.block) + ", 3 seeds)")
    plt.title(args.title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.output, dpi=150)
    print("Saved", args.output)


if __name__ == "__main__":
    main()
