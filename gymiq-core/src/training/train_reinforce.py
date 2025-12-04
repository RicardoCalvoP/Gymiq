import torch

from src.rl_engine.state_builder import encode_state


def train_policy_gradient(env, policy, optimizer, n_episodes=500, gamma=0.99,
                          device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy.to(device)

    for episode in range(n_episodes):
        state_raw = env.reset()
        log_probs = []
        rewards = []

        done = False
        while not done:
            state_tensor = encode_state(state_raw).to(device)  # clave
            probs = policy(state_tensor.unsqueeze(0))  # [1, n_actions]
            dist = torch.distributions.Categorical(probs=probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)

            next_state_raw, reward, done, info = env.step(int(action.item()))

            log_probs.append(log_prob)
            rewards.append(reward)
            state_raw = next_state_raw

        # calcular returns en el mismo device
        returns = []
        G = 0.0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns, dtype=torch.float32, device=device)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        loss = 0.0
        for log_prob, Gt in zip(log_probs, returns):
            loss += -log_prob * Gt

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (episode + 1) % 10 == 0:
            print(
                f"[RL] Episode {episode+1}/{n_episodes} | Loss: {loss.item():.4f}")
