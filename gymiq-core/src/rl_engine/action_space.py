# ============================================================
#  Espacio de acciones (recomendación de cambio de peso)
# ============================================================

"""
Primer modelo PG: acciones discretas fijas.

Acciones:
    0 → -5.0 kg
    1 → -2.5 kg
    2 →  0.0 kg   (mantener)
    3 → +1.0 kg
    4 → +2.5 kg

Este espacio es simple y estable para el primer modelo.
"""

ACTION_SPACE_KG = [-5.0, -2.5, 0.0, 1.0, 2.5]
N_ACTIONS = len(ACTION_SPACE_KG)


def get_action_delta(action_index: int) -> float:
    """
    Devuelve cuántos kg deben ajustarse según la acción discreta elegida.
    """
    return ACTION_SPACE_KG[action_index]
