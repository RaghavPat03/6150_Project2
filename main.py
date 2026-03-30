"""
main.py — Entry point for the N-Queens hill-climbing project.

Usage
-----
    python main.py          # defaults to n=8
    python main.py          # then enter any n when prompted

The script collects n from the user, runs all three experiment groups
(A, B, C) and prints a formatted report to stdout.
"""

from experiments import (
    run_hill_climbing_experiment,
    run_sideways_experiment,
    run_random_restart_experiment,
    get_sample_sequences,
)

# ── Configuration ─────────────────────────────────────────────────────────────
RUNS_LIST    = [50, 100, 200, 500, 1000, 1500]  # trial counts for A and B
RR_TRIALS    = 100                               # independent runs for C
MAX_SIDEWAYS = 100                               # sideways-move budget
# ─────────────────────────────────────────────────────────────────────────────


def _divider(char='─', width=62):
    print(char * width)


def _print_rate_table(results):
    """Print the success/failure rate table for experiments A and B."""
    header = f"{'Runs':>6} | {'Success%':>9} | {'Fail%':>7} | {'AvgSteps(S)':>12} | {'AvgSteps(F)':>12}"
    print(header)
    _divider('-', len(header))
    for runs, r in results.items():
        print(
            f"{runs:>6} | "
            f"{r['success_rate'] * 100:>8.1f}% | "
            f"{r['failure_rate'] * 100:>6.1f}% | "
            f"{r['avg_steps_success']:>12.2f} | "
            f"{r['avg_steps_failure']:>12.2f}"
        )


def _print_sequences(sequences):
    """Print h-value sequences from sample runs."""
    for i, rec in enumerate(sequences, 1):
        outcome = 'SUCCESS' if rec['success'] else 'FAIL'
        seq_str = ' → '.join(str(h) for h in rec['sequence'])
        print(f"  Config {i} [{outcome}]  steps={rec['steps']}")
        print(f"    h sequence: {seq_str}")


def _get_n():
    """Prompt the user for the board size n and validate the input."""
    while True:
        try:
            n = int(input("Enter the number of queens n (e.g. 8): ").strip())
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            print("  Please enter a positive integer.")


def main():
    _divider('═')
    print("  N-Queens Problem — Hill-Climbing Search")
    _divider('═')

    n = _get_n()
    print(f"\nBoard size: {n}×{n}   |   Queens: {n}\n")

    # ── A. Standard Hill Climbing ─────────────────────────────────────────────
    _divider()
    print("A.  Hill-Climbing Search")
    _divider()
    hc_results = run_hill_climbing_experiment(n, RUNS_LIST)
    _print_rate_table(hc_results)

    print("\n  Search sequences from 4 random initial configurations:")
    _print_sequences(get_sample_sequences(n, use_sideways=False))

    # ── B. Hill Climbing with Sideways Move ───────────────────────────────────
    print()
    _divider()
    print(f"B.  Hill-Climbing with Sideways Move  (max_sideways={MAX_SIDEWAYS})")
    _divider()
    sw_results = run_sideways_experiment(n, RUNS_LIST, max_sideways=MAX_SIDEWAYS)
    _print_rate_table(sw_results)

    print("\n  Search sequences from 4 random initial configurations:")
    _print_sequences(get_sample_sequences(n, use_sideways=True, max_sideways=MAX_SIDEWAYS))

    # ── C. Random-Restart Hill Climbing ───────────────────────────────────────
    print()
    _divider()
    print(f"C.  Random-Restart Hill-Climbing  ({RR_TRIALS} independent trials)")
    _divider()
    rr = run_random_restart_experiment(n, trials=RR_TRIALS, max_sideways=MAX_SIDEWAYS)

    no_sw = rr['no_sideways']
    with_sw = rr['with_sideways']

    print(f"  {'Variant':<30} {'Avg restarts':>13} {'Avg total steps':>16}")
    print(f"  {'-'*30} {'-'*13} {'-'*16}")
    print(f"  {'Without sideways move':<30} {no_sw['avg_restarts']:>13.2f} {no_sw['avg_steps']:>16.2f}")
    print(f"  {'With sideways move':<30} {with_sw['avg_restarts']:>13.2f} {with_sw['avg_steps']:>16.2f}")

    _divider('═')
    print("  Done.")
    _divider('═')


if __name__ == '__main__':
    main()