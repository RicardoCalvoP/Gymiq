# 1. Espacio de acciones discretas (cambios en kg)
ACTION_SPACE_KG = [-5.0, -2.5, 0.0, 1.0, 2.5]
N_ACTIONS = len(ACTION_SPACE_KG)


def get_action_delta(action_index: int) -> float:
    """
    Devuelve cuántos kg deben ajustarse según la acción discreta elegida.
    Ejemplo:
        acción 0 → -5.0 kg
        acción 4 → +2.5 kg
    """
    return ACTION_SPACE_KG[action_index]


# ============================================================
# Validación del espacio de acciones (solo modo debug)
# ============================================================
if __name__ == "__main__":
    print("\n========================")
    print("VALIDANDO ESPACIO DE ACCIONES")
    print("========================\n")

    print("Lista de acciones (Δ kg posibles):")
    for idx, delta in enumerate(ACTION_SPACE_KG):
        print(f"  Acción {idx}: {delta} kg")

    print(f"\nTotal de acciones disponibles (N_ACTIONS): {N_ACTIONS}")

    print("\nEjemplos de interpretación:")
    for idx, delta in enumerate(ACTION_SPACE_KG):
        if delta < 0:
            tipo = "Reducir peso"
        elif delta > 0:
            tipo = "Aumentar peso"
        else:
            tipo = "Mantener peso"
        print(f"  Acción {idx}: {delta:+} kg  -> {tipo}")

    print("\n========================\n")
