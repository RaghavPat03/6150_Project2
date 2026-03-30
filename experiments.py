"""
experiments.py — Experiment runners for the N-Queens hill-climbing project.

Each function runs a chosen algorithm many times and aggregates the results
into a plain dictionary so they can be printed or saved by the caller.

Functions
---------
run_hill_climbing_experiment      Run standard hill climbing N times.
run_sideways_experiment           Run sideways-move hill climbing N times.
run_random_restart_experiment     Benchmark random-restart (both variants).
get_sample_sequences              Collect h-value sequences for 4 random
                                  starting configurations.
"""

from board import random_state
from algorithms import (
    hill_climbing,
    hill_climbing_sideways,
    random_restart_hill_climbing,
)


def run_hill_climbing_experiment(n, runs_list):
    """
    Run standard hill climbing for each trial count in runs_list.

    Args:
        n         (int)       : Board size.
        runs_list (list[int]) : Trial counts, e.g. [50, 100, 200, 500, 1000, 1500].

    Returns:
        dict: Keyed by trial count.  Each value contains:
            runs             (int)   – number of trials.
            success_rate     (float) – fraction of successful runs.
            failure_rate     (float) – fraction of failed runs.
            avg_steps_success(float) – mean steps when succeeding (0 if never).
            avg_steps_failure(float) – mean steps when failing   (0 if never).
    """
    results = {}
    for runs in runs_list:
        successes, failures = 0, 0
        success_steps, failure_steps = [], []

        for _ in range(runs):
            success, steps, _ = hill_climbing(n)
            if success:
                successes += 1
                success_steps.append(steps)
            else:
                failures += 1
                failure_steps.append(steps)

        results[runs] = {
            'runs':              runs,
            'success_rate':      successes / runs,
            'failure_rate':      failures  / runs,
            'avg_steps_success': sum(success_steps) / len(success_steps) if success_steps else 0.0,
            'avg_steps_failure': sum(failure_steps) / len(failure_steps) if failure_steps else 0.0,
        }
    return results


def run_sideways_experiment(n, runs_list, max_sideways=100):
    """
    Run hill climbing with sideways moves for each trial count in runs_list.

    Args:
        n            (int)       : Board size.
        runs_list    (list[int]) : Trial counts.
        max_sideways (int)       : Sideways-move budget per run (default 100).

    Returns:
        dict: Same structure as run_hill_climbing_experiment.
    """
    results = {}
    for runs in runs_list:
        successes, failures = 0, 0
        success_steps, failure_steps = [], []

        for _ in range(runs):
            success, steps, _ = hill_climbing_sideways(n, max_sideways)
            if success:
                successes += 1
                success_steps.append(steps)
            else:
                failures += 1
                failure_steps.append(steps)

        results[runs] = {
            'runs':              runs,
            'success_rate':      successes / runs,
            'failure_rate':      failures  / runs,
            'avg_steps_success': sum(success_steps) / len(success_steps) if success_steps else 0.0,
            'avg_steps_failure': sum(failure_steps) / len(failure_steps) if failure_steps else 0.0,
        }
    return results


def run_random_restart_experiment(n, trials=100, max_sideways=100):
    """
    Benchmark random-restart hill climbing with and without sideways moves.

    Args:
        n            (int) : Board size.
        trials       (int) : Number of independent random-restart runs
                             to average over (default 100).
        max_sideways (int) : Sideways-move budget (default 100).

    Returns:
        dict with two keys:
            'no_sideways'  – avg_restarts, avg_steps (plain hill climbing).
            'with_sideways'– avg_restarts, avg_steps (sideways variant).
    """
    # --- without sideways ---
    no_sw_restarts, no_sw_steps = [], []
    for _ in range(trials):
        r, s = random_restart_hill_climbing(n, use_sideways=False)
        no_sw_restarts.append(r)
        no_sw_steps.append(s)

    # --- with sideways ---
    sw_restarts, sw_steps = [], []
    for _ in range(trials):
        r, s = random_restart_hill_climbing(n, use_sideways=True, max_sideways=max_sideways)
        sw_restarts.append(r)
        sw_steps.append(s)

    return {
        'no_sideways': {
            'avg_restarts': sum(no_sw_restarts) / trials,
            'avg_steps':    sum(no_sw_steps)    / trials,
        },
        'with_sideways': {
            'avg_restarts': sum(sw_restarts) / trials,
            'avg_steps':    sum(sw_steps)    / trials,
        },
    }


def get_sample_sequences(n, use_sideways=False, max_sideways=100, count=4):
    """
    Collect h-value sequences from several random starting configurations.

    Useful for illustrating the search trajectory in the project report.

    Args:
        n            (int)  : Board size.
        use_sideways (bool) : Use sideways variant when True.
        max_sideways (int)  : Sideways budget (default 100).
        count        (int)  : Number of configurations to sample (default 4).

    Returns:
        list[dict]: Each dict contains:
            initial  (list[int]) – starting state.
            success  (bool)      – whether the run succeeded.
            steps    (int)       – number of moves.
            sequence (list[int]) – h at each step.
    """
    records = []
    for _ in range(count):
        init = random_state(n)
        if use_sideways:
            success, steps, seq = hill_climbing_sideways(n, max_sideways, initial_state=init)
        else:
            success, steps, seq = hill_climbing(n, initial_state=init)

        records.append({
            'initial': init,
            'success': success,
            'steps':   steps,
            'sequence': seq,
        })
    return records