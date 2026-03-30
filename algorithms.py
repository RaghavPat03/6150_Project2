"""
algorithms.py — Hill-climbing algorithms for the N-Queens problem.

Three algorithms are implemented:

    A. hill_climbing              — standard steepest-ascent hill climbing.
    B. hill_climbing_sideways     — hill climbing with sideways moves.
    C. random_restart_hill_climbing — random-restart wrapper for A and B.

All algorithms use the board utilities in board.py.
"""

import random
from board import random_state, heuristic, best_successor


# ─────────────────────────────────────────────────────────────────────────────
# A. Standard Hill-Climbing Search
# ─────────────────────────────────────────────────────────────────────────────

def hill_climbing(n, initial_state=None):
    """
    Standard steepest-ascent hill climbing for the N-Queens problem.

    At each step the algorithm moves to the neighbour with the lowest h
    (fewest attacking pairs).  It stops as soon as no improving neighbour
    exists (local minimum or solution).

    Sideways moves (equal h) are NOT allowed; the search terminates
    immediately if the best neighbour is no better than the current state.

    Args:
        n             (int)       : Board size / number of queens.
        initial_state (list[int]) : Optional starting state.  A random
                                    state is used when None.

    Returns:
        tuple:
            success  (bool)      – True if h == 0 was reached.
            steps    (int)       – Number of moves taken.
            sequence (list[int]) – h value at each step (including start).
    """
    state = initial_state[:] if initial_state else random_state(n)
    current_h = heuristic(state)
    steps = 0
    sequence = [current_h]

    while True:
        best_h, best_states, _, _ = best_successor(state)

        # No improvement available → local minimum (or already a solution)
        if best_h >= current_h:
            return (current_h == 0), steps, sequence

        # Move to a random best successor (breaks ties uniformly)
        state = random.choice(best_states)
        current_h = best_h
        steps += 1
        sequence.append(current_h)

        if current_h == 0:
            return True, steps, sequence


# ─────────────────────────────────────────────────────────────────────────────
# B. Hill-Climbing with Sideways Move
# ─────────────────────────────────────────────────────────────────────────────

def hill_climbing_sideways(n, max_sideways=100, initial_state=None):
    """
    Hill climbing with a limited number of sideways (lateral) moves.

    When the best available neighbour has the same h as the current state
    the algorithm makes a sideways move rather than stopping.  This lets it
    escape some plateaus.  A counter limits consecutive sideways moves to
    avoid infinite loops on flat regions.

    The sideways counter resets to 0 whenever a strictly improving move is
    made.

    Args:
        n             (int)       : Board size / number of queens.
        max_sideways  (int)       : Maximum consecutive sideways moves
                                    allowed (default: 100).
        initial_state (list[int]) : Optional starting state.

    Returns:
        tuple:
            success  (bool)      – True if h == 0 was reached.
            steps    (int)       – Number of moves taken.
            sequence (list[int]) – h value at each step (including start).
    """
    state = initial_state[:] if initial_state else random_state(n)
    current_h = heuristic(state)
    steps = 0
    sideways_count = 0
    sequence = [current_h]

    while True:
        best_h, best_states, equal_states, _ = best_successor(state)

        if best_h > current_h:
            # Strictly worse neighbours only → genuine local minimum
            return False, steps, sequence

        if best_h == current_h:
            # Sideways move
            if sideways_count >= max_sideways:
                return False, steps, sequence   # sideways budget exhausted
            sideways_count += 1
            # Choose uniformly among all equal-h neighbours
            state = random.choice(equal_states if equal_states else best_states)
        else:
            # Strictly improving move
            sideways_count = 0
            state = random.choice(best_states)

        current_h = best_h
        steps += 1
        sequence.append(current_h)

        if current_h == 0:
            return True, steps, sequence


# ─────────────────────────────────────────────────────────────────────────────
# C. Random-Restart Hill-Climbing
# ─────────────────────────────────────────────────────────────────────────────

def random_restart_hill_climbing(n, use_sideways=False, max_sideways=100):
    """
    Random-restart hill climbing.

    Runs hill climbing (with or without sideways moves) from successive
    random initial states until a solution is found.  The number of restarts
    and total steps across all attempts are recorded.

    A "restart" is counted only when an attempt fails; the final (successful)
    attempt is not counted as a restart.

    Args:
        n            (int)  : Board size / number of queens.
        use_sideways (bool) : Use sideways-move variant when True.
        max_sideways (int)  : Sideways-move budget (used only when
                              use_sideways=True, default: 100).

    Returns:
        tuple:
            restarts    (int) – Number of failed attempts before success.
            total_steps (int) – Total moves across all attempts (including
                                the final successful one).
    """
    restarts = 0
    total_steps = 0

    while True:
        if use_sideways:
            success, steps, _ = hill_climbing_sideways(n, max_sideways)
        else:
            success, steps, _ = hill_climbing(n)

        total_steps += steps

        if success:
            return restarts, total_steps

        restarts += 1   # this attempt failed; try again