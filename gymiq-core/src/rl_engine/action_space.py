# ============================================================
#  Espacio de acciones (recomendación de cambio de peso)
# ============================================================

"""
Primer modelo PG: acciones discretas fijas.



Este espacio es simple y estable para el primer modelo.
"""

ACTION_SPACE_KG = [
    -20, -17.5, -15, -12.5, -10, -7.5 ,-5.0, -2.5,
    0.0,
    20, 17.5, 15, 12.5, 10, 7.5 ,5.0, 2.5,
      ]

N_ACTIONS = len(ACTION_SPACE_KG)


def get_action_delta(action_index: int) -> float:
    """
    Devuelve cuántos kg deben ajustarse según la acción discreta elegida.
    """
    return ACTION_SPACE_KG[action_index]
