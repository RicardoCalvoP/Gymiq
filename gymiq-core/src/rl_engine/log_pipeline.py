from typing import Dict, Any


def ingest_log_entry(log_entry: Dict[str, Any]) -> None:
    # Aquí luego:
    # - Lo transformaremos a estados RL
    # - Guardaremos transiciones (state, action, reward, done)
    print("[RL_ENGINE] Workout log received:", log_entry)
