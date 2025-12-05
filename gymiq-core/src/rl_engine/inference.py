from typing import Dict, Any
from .config import MODELS_DIR

import torch

from .state_builder import encode_state
from .policy_net import PolicyNetwork
from .action_space import ACTION_SPACE_KG


class PolicyService:
    """
    Wrapper sencillo alrededor de PolicyNetwork para uso en backend.
    Se encarga de:
      - cargar el modelo (por ahora en blanco o con pesos entrenados),
      - recibir un state_raw,
      - devolver la recomendación de cambio de peso.
    """

    def __init__(self, model: PolicyNetwork | None = None, weights_name: str = "policy_teacher.pt") -> None:
        if model is not None:
            self.policy = model
        else:
            self.policy = PolicyNetwork()
            weights_path = MODELS_DIR / weights_name
            if weights_path.exists():
                self.policy.load_state_dict(
                    torch.load(weights_path, map_location="cpu"))
                print(f"[POLICY] Loaded weights from {weights_path}")
            else:
                print(
                    f"[POLICY] No weights file found at {weights_path}, using random init.")
        self.policy.eval()

    def recommend_weight_delta(self, state_raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        state_raw: dict como el que consume encode_state (edad, imc, sexo, etc.)
        Devuelve:
          - action_index
          - delta_kg
          - action_probs (para debug)
        """
        with torch.no_grad():
            state_vec = encode_state(state_raw)          # tensor [D_STATE]
            probs = self.policy(state_vec)               # [1, n_actions]
            probs_np = probs.squeeze(0).cpu().numpy()

            # Elegimos acción greedy por ahora (argmax)
            action_idx = int(probs.argmax(dim=-1).item())
            delta_kg = ACTION_SPACE_KG[action_idx]

        return {
            "action_index": action_idx,
            "delta_kg": delta_kg,
            "action_probs": probs_np.tolist(),
        }
