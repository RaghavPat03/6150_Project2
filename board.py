"""
board.py — N-Queens board representation and core utilities.

State representation:
    A list of length n where state[col] = row of the queen in that column.
    One queen is placed per column by construction, so column conflicts are
    impossible.  Only row and diagonal conflicts need to be checked.

Heuristic:
    h = number of pairs of queens that are directly attacking each other.
    h = 0  →  valid solution (no attacks).
    Lower h is better (this is a minimisation problem).
"""

import random
import math


def random_state(n):
    """
    Generate a random initial board state.

    Places exactly one queen per column at a randomly chosen row.

    Args:
        n (int): Number of queens (and board dimension).

    Returns:
        list[int]: A state list of length n.
    """
    return [random.randint(0, n - 1) for _ in range(n)]


def heuristic(state):
    """
    Compute the heuristic value h for a given state.

    h counts the number of pairs of queens that attack each other —
    either on the same row or on the same diagonal.  Column conflicts
    cannot occur because the representation guarantees one queen per column.

    Args:
        state (list[int]): Current board state.

    Returns:
        int: Number of attacking pairs (0 = solution).
    """
    n = len(state)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:          # same row
                attacks += 1
            if abs(state[i] - state[j]) == abs(i - j):   # same diagonal
                attacks += 1
    return attacks


def best_successor(state):
    """
    Enumerate all single-move successors and return the best ones.

    A single move consists of choosing a column and moving its queen to a
    different row.  This generates n*(n-1) neighbours in total.

    Args:
        state (list[int]): Current board state.

    Returns:
        tuple:
            best_h      (int)       – lowest heuristic value found among neighbours.
            best_states (list)      – all neighbour states achieving best_h.
            equal_states(list)      – all neighbour states with h == current h
                                      (used by the sideways-move variant).
            current_h   (int)       – heuristic of the input state.
    """
    n = len(state)
    current_h = heuristic(state)
    best_h = math.inf
    best_states = []
    equal_states = []

    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue                      # skip the current position

            state[col] = row                  # try the move (in-place)
            h = heuristic(state)

            if h < best_h:
                best_h = h
                best_states = [state[:]]      # new best — reset list
            elif h == best_h:
                best_states.append(state[:])  # tie — add to list

            if h == current_h:
                equal_states.append(state[:]) # lateral neighbour

            state[col] = original_row         # undo the move

    return best_h, best_states, equal_states, current_h