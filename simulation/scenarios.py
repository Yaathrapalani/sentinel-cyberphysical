import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from utils.config import (
    ATTACK_START, ATTACK_DURATION, SPOOF_VALUE
)


def generate_normal(n: int = 300) -> tuple:
    """
    Simulate normal infrastructure operation.
    Cyber and physical scores are naturally correlated.
    Low anomaly scores with small natural variation.
    """
    np.random.seed(42)
    base = np.random.normal(0.15, 0.05, n).clip(0, 1)
    noise_cyber    = np.random.normal(0, 0.03, n)
    noise_physical = np.random.normal(0, 0.03, n)

    # Natural coupling: physical responds to cyber with small lag
    cyber    = (base + noise_cyber).clip(0, 1)
    physical = (base + noise_physical).clip(0, 1)

    return cyber, physical


def generate_cyber_only(n: int = 300) -> tuple:
    """
    Simulate a simple network intrusion with no physical spoofing.
    Cyber anomaly rises. Physical rises too because
    the attacker has not hidden their tracks.
    Standard IDS catches this. SENTINEL also catches it.
    Used as baseline comparison in demo.
    """
    np.random.seed(42)
    cyber, physical = generate_normal(n)

    # Inject cyber anomaly in attack window
    attack_end = ATTACK_START + ATTACK_DURATION
    cyber[ATTACK_START:attack_end] = np.random.normal(
        0.75, 0.08, ATTACK_DURATION
    ).clip(0, 1)

    # Physical also shows anomaly — attacker not hiding
    physical[ATTACK_START:attack_end] = np.random.normal(
        0.65, 0.08, ATTACK_DURATION
    ).clip(0, 1)

    return cyber, physical


def generate_compound_attack(n: int = 300) -> tuple:
    """
    Simulate a compound cyber-physical attack.
    This is what SENTINEL catches that standard IDS misses.

    Attack mechanics:
      1. Attacker gains access to network (cyber anomaly rises)
      2. Attacker simultaneously replays old sensor readings
         to hide physical manipulation (physical score stays low)
      3. The natural coupling between cyber and physical breaks
      4. SENTINEL detects the decoupling as a compound signature

    Standard IDS behavior on this scenario:
      - Sees high cyber anomaly score: raises alert
      - Sees low physical anomaly score: lowers confidence
      - Result: confused, issues low-confidence or no alert

    SENTINEL behavior:
      - Measures correlation between cyber and physical
      - Detects decoupling: these two should move together
      - Issues CRITICAL alert regardless of physical score
    """
    np.random.seed(42)
    cyber, physical = generate_normal(n)

    attack_end = ATTACK_START + ATTACK_DURATION

    # Cyber anomaly spikes — real intrusion happening
    cyber[ATTACK_START:attack_end] = np.random.normal(
        0.82, 0.06, ATTACK_DURATION
    ).clip(0, 1)

    # Physical spoofed to look normal — this is the compound part
    # Attacker replays historical sensor readings
    # Physical score stays LOW while cyber score is HIGH
    physical[ATTACK_START:attack_end] = np.random.normal(
        SPOOF_VALUE, 0.02, ATTACK_DURATION
    ).clip(0, 1)

    return cyber, physical


def generate_all_scenarios(n: int = 300) -> dict:
    """Return all three scenarios for comparison evaluation."""
    return {
        'normal':         generate_normal(n),
        'cyber_only':     generate_cyber_only(n),
        'compound_attack': generate_compound_attack(n)
    }